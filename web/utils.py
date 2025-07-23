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
    
    loaded_job_ads_df = pd.read_csv(ORIGINAL_DATA_PATH) #loads original data

except FileNotFoundError as e:
    print(f"Error: file {MODEL_PATH}, {VECTORS_PATH} and {ORIGINAL_DATA_PATH} are missing. {e}")
    exit() # Exits the script if the files are not found
except Exception as e:
    print(f"Error during loading: {e}")
    exit()
    
def extract_pdf_text(pdf_source):
   

    try:
        text = extract_text(pdf_source)
        text = text.lower()
        text = preprocess_text(text)
        return text
    except Exception as e:
        print(f"Error in text extraction: {e}")
        return ""
    
def find_top_matches(cv_text: str, k: int = 5):
   

    # vectorize the CV text and find the most similar job ads

    cv_vector = loaded_vectorizer.transform([cv_text])

    # calculate cosine similarity between the CV vector and job ads vectors
    # it returns a 2D array, so we flatten it to a 1D array
    similarities = cosine_similarity(cv_vector, loaded_job_ads_vectors).flatten()

    # combine the similarities with the job ads DataFrame
    results_df = loaded_job_ads_df.copy() 
    results_df['similarity'] = similarities

    # Orders the results by similarity score
    sorted_results = results_df.sort_values(by='similarity', ascending=False)

    # select the top k job ads
    top_k_jobs = sorted_results.head(k)
   
    # choose the columns to display
    display_columns = ['Company','Role', 'Description', 'Job Link'] #in the future ill add the link

    # Convert the DataFrame to a list of dictionaries for easy reading
    # top_k_jobs_output = top_k_jobs.drop(columns=['similarity']).to_dict(orient='records')
    top_k_jobs_output = top_k_jobs[display_columns].to_dict(orient='records')

    return top_k_jobs_output
