import pickle
import pandas as pd
# from scipy.sparse import csr_matrix 

MODEL_PATH = 'tfidf_vectorizer.pkl'
VECTORS_PATH = 'job_ads_tfidf_vectors.pkl'
ORIGINAL_DATA_PATH = 'job_ads.csv'

try:
    with open(MODEL_PATH, 'rb') as f:
        loaded_vectorizer = pickle.load(f)
    with open(VECTORS_PATH, 'rb') as f:
        loaded_vectors = pickle.load(f)
    original_df = pd.read_csv(ORIGINAL_DATA_PATH)
except FileNotFoundError as e:
    print(f"Errore: Assicurati che tutti i file necessari siano presenti. {e}")
    exit() # Esci se i file non sono trovati

# --- 1. Termini con IDF più alto  ---
print("\n--- I 20 termini più distintivi nel vocabolario ( IDF  più alto) ---")
# Ottieni gli IDF (Inverse Document Frequency)
idfs = loaded_vectorizer.idf_
# Crea una serie Pandas per associare IDF ai nomi dei termini
feature_names = loaded_vectorizer.get_feature_names_out()
idf_df = pd.DataFrame({'term': feature_names, 'idf': idfs})
# Ordina per IDF in ordine decrescente
top_idf_terms = idf_df.sort_values(by='idf', ascending=False).head(20)
print(top_idf_terms)

print("\n--- Termini più importanti per il primo annuncio ---")
first_doc_vector = loaded_vectors[0]
first_doc_vector_dense = first_doc_vector.toarray().flatten()

# Crea una serie Pandas per associare i pesi TF-IDF ai nomi dei termini
tfidf_scores = pd.DataFrame({'term': feature_names, 'tfidf_score': first_doc_vector_dense})
# Ordina per TF-IDF score in ordine decrescente
top_tfidf_terms_for_doc = tfidf_scores.sort_values(by='tfidf_score', ascending=False).head(10)
print(top_tfidf_terms_for_doc)

if not original_df.empty:
    print("\nTesto originale del PRIMO annuncio:")
    print(original_df.iloc[0]['description']) 