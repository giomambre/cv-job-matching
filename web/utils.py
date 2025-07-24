from pdfminer.high_level import extract_text
import re
import sys
import os
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.train_model import preprocess_text

MODEL_PATH = 'model/tfidf_vectorizer.pkl'
VECTORS_PATH = 'model/job_ads_tfidf_vectors.pkl'
ORIGINAL_DATA_PATH = 'model/job_ads.csv'

try:
    with open(MODEL_PATH, 'rb') as f:
        loaded_vectorizer = pickle.load(f)
    
    with open(VECTORS_PATH, 'rb') as f:
        loaded_job_ads_vectors = pickle.load(f)
    
    loaded_job_ads_df = pd.read_csv(ORIGINAL_DATA_PATH)

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
    
def find_top_matches(cv_text: str, k: int = 9):
    """Find top k job matches for the given CV text"""
    # Vectorize the CV text and find the most similar job ads
    cv_vector = loaded_vectorizer.transform([cv_text])

    # Calculate cosine similarity between the CV vector and job ads vectors
    similarities = cosine_similarity(cv_vector, loaded_job_ads_vectors).flatten()

    # Combine the similarities with the job ads DataFrame
    results_df = loaded_job_ads_df.copy() 
    results_df['similarity'] = similarities

    # Order the results by similarity score
    sorted_results = results_df.sort_values(by='similarity', ascending=False)

    # Select the top k job ads
    top_k_jobs = sorted_results.head(k)
   
    # Choose the columns to display
    display_columns = ['Company','Role', 'Description', 'Job Link']

    # Convert the DataFrame to a list of dictionaries for easy reading
    top_k_jobs_output = top_k_jobs[display_columns].to_dict(orient='records')
    
    # Add similarity scores to the output
    similarities_list = sorted_results.head(k)['similarity'].tolist()
    for i, job in enumerate(top_k_jobs_output):
        job['similarity'] = float(similarities_list[i])

    return top_k_jobs_output


if __name__ == "__main__":
    # Example usage
    cv_text = "Software engineer with experience in Python and machine learning."
    top_matches = find_top_matches(cv_text)
    print(top_matches)
