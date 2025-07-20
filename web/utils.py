from pdfminer.high_level import extract_text
import re
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity 
from ..model.train_model import preprocess_text
MODEL_PATH = 'tfidf_vectorizer.pkl'
VECTORS_PATH = 'job_ads_tfidf_vectors.pkl'
ORIGINAL_DATA_PATH = 'job_descriptions.csv'
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
    print(f"Vettore CV creato con dimensioni: {cv_vector.shape}")

    # calculate cosine similarity between the CV vector and job ads vectors
    # it returns a 2D array, so we flatten it to a 1D array
    similarities = cosine_similarity(cv_vector, loaded_job_ads_vectors).flatten()
    print(f"Calcolate {len(similarities)} similarità.")

    # combine the similarities with the job ads DataFrame
    results_df = loaded_job_ads_df.copy() 
    results_df['similarity'] = similarities
    
    # Oders the results by similarity score
    sorted_results = results_df.sort_values(by='similarity', ascending=False)

    # select the top k job ads
    top_k_jobs = sorted_results.head(k)

   
    # choose the columns to display
    display_columns = ['title', 'description', 'similarity'] #in the future ill add the link
    
    # Convert the DataFrame to a list of dictionaries for easy reading
    # You can remove the 'similarity' column if you don't want to show it to the end user
    # top_k_jobs_output = top_k_jobs.drop(columns=['similarity']).to_dict(orient='records')
    top_k_jobs_output = top_k_jobs[display_columns].to_dict(orient='records')

    return top_k_jobs_output

# --- Esempio di utilizzo con un CV di prova ---
if __name__ == "__main__":
    # Puoi caricare il testo del CV da un file o inserirlo direttamente
    try:
        with open('my_cv.txt', 'r', encoding='utf-8') as f:
            my_cv_text = f.read()
    except FileNotFoundError:
        print("\nErrore: Il file 'my_cv.txt' non è stato trovato. Creane uno con il testo del tuo CV.")
        # Se non hai un file, usa una stringa di testo direttamente:
        # my_cv_text = "Sono un ingegnere software con forte esperienza in Python, FastAPI e AWS. Ho lavorato su progetti di machine learning e analisi dati, con competenze in SQL e sistemi distribuiti. Cerco ruoli sfidanti."
        my_cv_text = "Un testo di esempio per il mio CV con Python e Machine Learning." # Testo di fallback

    if my_cv_text:
        print("\n--- Ricerca degli Annunci più Pertinenti ---")
        top_5_matches = find_top_matches(my_cv_text, k=5)

        if top_5_matches:
            print("\nEcco i 5 annunci di lavoro più pertinenti:")
            for i, job in enumerate(top_5_matches):
                print(f"\n--- Annuncio {i+1} (Similarità: {job.get('similarity', 'N/A'):.4f}) ---")
                print(f"Titolo: {job.get('title', 'N/A')}")
                print(f"Descrizione (Estratto): {job.get('description', 'N/A')[:200]}...") # Limita per chiarezza
                # Puoi aggiungere altri dettagli dell'annuncio qui
        else:
            print("Nessun annuncio trovato o errore nel matching.")
    else:
        print("Il testo del CV è vuoto. Impossibile procedere con il matching.")