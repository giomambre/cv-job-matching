import pandas as pd
import pickle
import re
import os

# Only import sentence_transformers if needed (for BERT version)
try:
    USE_BERT = os.getenv('USE_BERT', 'false').lower() == 'true'
    if USE_BERT:
        from sentence_transformers import SentenceTransformer
except ImportError:
    USE_BERT = False
    print("sentence_transformers not available, using TF-IDF only")

# Import sklearn only when needed
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
except ImportError:
    print("Warning: sklearn not available")

CSV_FILE_PATH = 'model/job_ads.csv'
TEXT_COLUMN_NAME = 'Description'
MODEL_SAVE_PATH = 'model/sentence_embedding_model.pkl'
VECTORS_SAVE_PATH = 'model/job_ads_embedding_vectors.pkl'

common_words = [
    "looking", "join", "seeking", "role", "position", "candidate", "experience",
    "skills", "team", "work", "opportunity", "company", "apply", "apply now",
    "apply today", "and", "competitive", "salary", "benefits", "full-time", "part-time",
    "remote", "hybrid", "flexible", "culture", "environment", "innovative",
    "dynamic", "collaborative", "leadership", "development", "growth",
    "responsibilities", "comprehensive", "talented", "supportive", "inclusive",
    "diverse", "mission", "vision", "values", "strategic", "impactful",
    "contribute", "success", "achieve", "goals", "objectives", "projects",
    "initiatives", "strong", "excellent", "proven", "ability", "manage",
    "deliver", "ensure", "drive", "solve", "foster", "optimize", "lead",
    "implement", "support", "develop", "high", "standards", "key", "best practices",
    "solutions", "effective", "successful", "outstanding", "advanced", "extensive",
    "demonstrate", "commitment", "continuous improvement", "forward-thinking",
    "analytical", "communication", "shape", "strategies", "complex", "mentor",
    "colleagues", "essential", "ambitious", "proactive", "detail-oriented",
    "passionate", "making a difference", "background", "strategic planning",
    "process improvement", "execution", "stakeholders", "coordination",
    "requirements gathering", "executive leadership", "will be responsible for",
    "you will", "we are", "our company is", "become part of", "who excels in",
    "with", "with expertise in", "in this role", "we value"
]

def preprocess_text(text: str) -> str:
    #clean the text of the csv file
    processed_text = str(text).lower()
    
   
    # processed_text = re.sub(r'[^\w\s]', '', processed_text) 
    processed_text = re.sub(r'\b(?:' + '|'.join(common_words) + r')\b', '', processed_text) 
    processed_text = re.sub(r'\s+', ' ', processed_text).strip()  # Rimuove spazi multipli e strip 
    return processed_text



def train_embedding_model(csv_path, text_col, model_path, vectors_path):
    if not USE_BERT:
        print("BERT not available or disabled. Use train_tfidf_model instead.")
        return
        
    print(f"1. Loading CSV from {csv_path}")
    df = pd.read_csv(csv_path)

    if text_col not in df.columns:
        print(f"Column '{text_col}' not found.")
        return

    # Preprocess
    text_data = df[text_col].fillna('')
    print(f"2. Preprocessing {len(text_data)} descriptions...")
    processed_docs = text_data.apply(preprocess_text)

    # Load model
    print("3. Loading sentence-transformer model...")  
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Encode
    print("4. Generating embeddings...")
    embeddings = model.encode(processed_docs.tolist(), show_progress_bar=True)

    # Save model and vectors
    print(f"5. Saving embedding model to {model_path}")
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    print(f"6. Saving job vectors to {vectors_path}")
    with open(vectors_path, 'wb') as f:
        pickle.dump(embeddings, f)

    print("✅ Embedding training completed.")



def train_tfidf_model(csv_path: str, text_col: str, model_path: str, vectors_path: str):
    print(f"loading file '{csv_path}'...")
    try:
        # load the Csv file
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"file '{csv_path}' was not found. Please check the file path.")
        return
    
    if text_col not in df.columns:
        print(f"Column '{text_col}' has not been found in the csv file.")
        return

    
    # df['combined_text'] = df['title'].fillna('') + ' ' + df[text_col].fillna('') + ' ' + df['requirements'].fillna('')
    text_data = df[text_col].fillna('') #fills the NaN values with empty strings

    print(f"2. Preprocessing {len(text_data)} documents...")
    processed_docs = text_data.apply(preprocess_text)

    print("3. Initializing and training the TfidfVectorizer...")
    # 'stop_words="english"' removes common English words (e.g. "the", "is", "in").
    # max 5000 terms, max dimension of the vector space
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)

    #  Learns the vocabulary and computes the IDF from 'processed_docs'.
    #  Transforms each document in 'processed_docs' into a TF-IDF vector.
    tfidf_matrix = vectorizer.fit_transform(processed_docs)

    print(f"TF-IDF model trained. Vocabulary size: {len(vectorizer.vocabulary_)} terms.")
    print(f"TF-IDF matrix created: {tfidf_matrix.shape[0]} documents, {tfidf_matrix.shape[1]} features (words).")

    print(f"4. Saving trained model to '{model_path}'...")
    with open(model_path, 'wb') as f:
        pickle.dump(vectorizer, f)

    print(f"5. Saving TF-IDF matrix of job ads to '{vectors_path}'...")
    with open(vectors_path, 'wb') as f:
        pickle.dump(tfidf_matrix, f)

    print("Training completed successfully!")

# Run the training function
if __name__ == "__main__":
    if USE_BERT:
        train_embedding_model(CSV_FILE_PATH, TEXT_COLUMN_NAME, MODEL_SAVE_PATH, VECTORS_SAVE_PATH)
    else:
        # Default TF-IDF paths
        tfidf_model_path = 'model/tfidf_vectorizer.pkl'
        tfidf_vectors_path = 'model/job_ads_tfidf_vectors.pkl'
        train_tfidf_model(CSV_FILE_PATH, TEXT_COLUMN_NAME, tfidf_model_path, tfidf_vectors_path)
