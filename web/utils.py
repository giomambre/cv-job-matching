from pdfminer.high_level import extract_text
from sentence_transformers import SentenceTransformer
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

MODEL_PATH = 'model/tfidf_vectorizer.pkl'
VECTORS_PATH = 'model/job_ads_tfidf_vectors.pkl'
MODEL_PATH_EM = 'model/sentence_embedding_model.pkl' 
VECTORS_PATH_EM = 'model/job_ads_embedding_vectors.pkl'
ORIGINAL_DATA_PATH = 'model/job_ads.csv'

try:
    with open(MODEL_PATH, 'rb') as f:
        loaded_vectorizer_tf = pickle.load(f)
    
    with open(MODEL_PATH_EM, 'rb') as f:
        loaded_vectorizer = pickle.load(f)
    
    with open(VECTORS_PATH_EM, 'rb') as f:
        loaded_job_ads_vectors = pickle.load(f)  # array numpy (n_annunci, dim_embedding)

    
    loaded_job_ads_df = pd.read_csv(ORIGINAL_DATA_PATH)
    model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')  # or 'cuda' with gpu
except FileNotFoundError as e:
    print(f"Error: files {MODEL_PATH}, {VECTORS_PATH} and {ORIGINAL_DATA_PATH} are missing. {e}")
    exit()
except Exception as e:
    print(f"Error during loading: {e}")
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
    print(f"DEBUG: find_top_matches called with k={k}")
    cv_vector = model.encode([cv_text])
    similarities = cosine_similarity(cv_vector, loaded_job_ads_vectors).flatten()
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