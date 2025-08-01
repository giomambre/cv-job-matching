from pdfminer.high_level import extract_text
import re
import sys
import os
import json
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity 
from typing import List, Dict
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.train_model import preprocess_text

# Use environment variable to determine which model to use
USE_BERT = os.getenv('USE_BERT', 'false').lower() == 'true'

MODEL_PATH = 'model/tfidf_vectorizer.pkl'
VECTORS_PATH = 'model/job_ads_tfidf_vectors.pkl' 
ORIGINAL_DATA_PATH = 'model/job_ads_8k.csv'

# Global variables
loaded_vectorizer_tf = None
loaded_job_ads_df = None
loaded_tfidf_vectors = None

# BERT-specific variables (only loaded if USE_BERT=true)
model = None
job_ads_embeddings = None

def load_models():
    """Load models and data based on USE_BERT flag"""
    global loaded_vectorizer_tf, loaded_job_ads_df, loaded_tfidf_vectors, model, job_ads_embeddings
    
    # Always load TF-IDF components
    if loaded_vectorizer_tf is None:
        try:
            with open(MODEL_PATH, 'rb') as f:
                loaded_vectorizer_tf = pickle.load(f)
            print("TF-IDF vectorizer loaded successfully")
        except FileNotFoundError:
            print(f"Warning: {MODEL_PATH} not found")
    
    if loaded_job_ads_df is None:
        try:
            loaded_job_ads_df = pd.read_csv(ORIGINAL_DATA_PATH)
            print(f"Job ads data loaded: {len(loaded_job_ads_df)} records")
        except FileNotFoundError:
            print(f"Error: {ORIGINAL_DATA_PATH} not found")
            raise
    
    # Load TF-IDF vectors for deployment (lighter option)
    if not USE_BERT and loaded_tfidf_vectors is None:
        try:
            with open(VECTORS_PATH, 'rb') as f:
                loaded_tfidf_vectors = pickle.load(f)
            print("TF-IDF vectors loaded successfully")
        except FileNotFoundError:
            print(f"Warning: {VECTORS_PATH} not found, will compute on-the-fly")
    
    # Only load BERT if USE_BERT=true (for GitHub version)
    if USE_BERT:
        if model is None:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
            print("Sentence transformer model loaded")
        
        if job_ads_embeddings is None:
            job_descriptions = loaded_job_ads_df['Description'].astype(str).tolist()
            print(f"Computing embeddings for {len(job_descriptions)} job descriptions...")
            job_ads_embeddings = model.encode(job_descriptions, batch_size=32, show_progress_bar=True)
            print("Job ads embeddings computed successfully")

# Initialize on import
try:
    load_models()
except Exception as e:
    print(f"Error during model loading: {e}")
    exit()
    
    
def extract_pdf_text(pdf_source):
    """Extract and preprocess text from PDF source"""
    try:
        text = extract_text(pdf_source)
        text = text.lower()
        text = preprocess_text(text)
        return text
    except Exception as e:
        print(f"Error in text extraction: {e}")
        return ""
def find_top_matches(cv_text: str, k: int = 6):
    global job_ads_embeddings, loaded_job_ads_df, model, loaded_vectorizer_tf, loaded_tfidf_vectors
    
    print(f"DEBUG: find_top_matches called with k={k}, USE_BERT={USE_BERT}")
    
    if USE_BERT:
        # BERT-based matching (GitHub version)
        if job_ads_embeddings is None or loaded_job_ads_df is None or model is None:
            load_models()
        
        cv_vector = model.encode([cv_text])
        similarities = cosine_similarity(cv_vector, job_ads_embeddings).flatten()
    else:
        # TF-IDF based matching (deployment version)
        if loaded_vectorizer_tf is None or loaded_job_ads_df is None:
            load_models()
        
        cv_preprocessed = preprocess_text(cv_text.lower())
        cv_vector = loaded_vectorizer_tf.transform([cv_preprocessed])
        
        if loaded_tfidf_vectors is not None:
            # Use pre-computed TF-IDF vectors
            similarities = cosine_similarity(cv_vector, loaded_tfidf_vectors).flatten()
        else:
            # Compute TF-IDF vectors on-the-fly
            job_descriptions = [preprocess_text(desc.lower()) for desc in loaded_job_ads_df['Description'].astype(str)]
            job_vectors = loaded_vectorizer_tf.transform(job_descriptions)
            similarities = cosine_similarity(cv_vector, job_vectors).flatten()
    
    results_df = loaded_job_ads_df.copy()
    results_df['similarity'] = similarities
    sorted_results = results_df.sort_values(by='similarity', ascending=False)
    top_k_jobs = sorted_results.head(k)
    print(f"DEBUG: returning {len(top_k_jobs)} results")
   
    display_columns = ['Company', 'Role', 'Description', 'Job Link']
    top_k_jobs_output = top_k_jobs[display_columns].to_dict(orient='records')
   
    for i, job in enumerate(top_k_jobs_output):
        top_k_jobs_output[i]['similarity'] = round(float(top_k_jobs.iloc[i]['similarity']), 4)
        top_k_jobs_output[i]['metrics'] = extract_keywords_from_texts(cv_text, job['Description'])
   
    return top_k_jobs_output

def get_top_keywords(vectorizer, vector, top_k=10):
    arr = vector.toarray()[0]
    feature_names = vectorizer.get_feature_names_out()
    top_indices = arr.argsort()[::-1][:top_k]
    top_keywords = [(feature_names[i], round(arr[i], 4)) for i in top_indices if arr[i] > 0]
    return top_keywords

def extract_keywords_from_texts(cv_text, job_text, top_k=10):
    global loaded_vectorizer_tf
    
    # Ensure TF-IDF vectorizer is loaded
    if loaded_vectorizer_tf is None:
        load_models()
    
    cv_preprocessed = preprocess_text(cv_text.lower())
    job_preprocessed = preprocess_text(job_text.lower())
   
    cv_vector = loaded_vectorizer_tf.transform([cv_preprocessed])
    job_vector = loaded_vectorizer_tf.transform([job_preprocessed])
    
    cv_keywords = dict(get_top_keywords(loaded_vectorizer_tf, cv_vector, top_k))
    job_keywords = dict(get_top_keywords(loaded_vectorizer_tf, job_vector, top_k))
    
    common_keywords = set(cv_keywords.keys()) & set(job_keywords.keys())
    common_keywords_with_scores = {
        kw: (round(cv_keywords[kw], 4), round(job_keywords[kw], 4)) 
        for kw in common_keywords
    }
    
    return common_keywords_with_scores

def format_keywords_for_ui(common_keywords_with_scores):
    keywords_list = []
    for kw, (score_cv, score_job) in common_keywords_with_scores.items():
        keywords_list.append({
            "keyword": kw,
            "score_cv": round(score_cv, 4),
            "score_job": round(score_job, 4)
        })
    return json.dumps(keywords_list)


if __name__ == "__main__":
    # Example usage
    cv_text = "Software engineer with experience in restful and machine learning."
    
    print(find_top_matches(cv_text,1))