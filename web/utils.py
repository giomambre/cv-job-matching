from pdfminer.high_level import extract_text
from sentence_transformers import SentenceTransformer
import re
import sys
import os
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.train_model import preprocess_text

MODEL_PATH_EM = 'model/sentence_embedding_model.pkl'  # opzionale se vuoi salvarlo
VECTORS_PATH_EM = 'model/job_ads_embedding_vectors.pkl'
ORIGINAL_DATA_PATH = 'model/job_ads.csv'

try:
    with open(MODEL_PATH_EM, 'rb') as f:
        loaded_vectorizer = pickle.load(f)
    
    with open(VECTORS_PATH_EM, 'rb') as f:
        loaded_job_ads_vectors = pickle.load(f)  # array numpy (n_annunci, dim_embedding)

    
    loaded_job_ads_df = pd.read_csv(ORIGINAL_DATA_PATH)
    model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')  # o 'cpu' se non hai GPU
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
    # Genera embedding per il CV
    cv_vector = model.encode([cv_text])  # restituisce un array (1, dim_embedding)

    # Calcola similarità coseno tra CV e tutti gli annunci
    similarities = cosine_similarity(cv_vector, loaded_job_ads_vectors).flatten()

    # Combina i risultati con il dataframe
    results_df = loaded_job_ads_df.copy()
    results_df['similarity'] = similarities

    # Ordina per similarità decrescente
    sorted_results = results_df.sort_values(by='similarity', ascending=False)

    # Prendi i primi k annunci
    top_k_jobs = sorted_results.head(k)

    # Colonne da mostrare
    display_columns = ['Company', 'Role', 'Description', 'Job Link']

    # Converti in lista di dizionari
    top_k_jobs_output = top_k_jobs[display_columns].to_dict(orient='records')

    # Aggiungi similarità ai risultati
    for i, job in enumerate(top_k_jobs_output):
        job['similarity'] = float(sorted_results.iloc[i]['similarity'])

    return top_k_jobs_output


if __name__ == "__main__":
    # Example usage
    cv_text = "Software engineer with experience in Python and machine learning."
    top_matches = find_top_matches(cv_text)
    print(top_matches)
