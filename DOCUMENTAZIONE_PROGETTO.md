# 📄 CV Job Matcher - Documentazione Completa del Progetto

## Indice
1. [Panoramica del Progetto](#panoramica-del-progetto)
2. [Come Funziona il Sistema](#come-funziona-il-sistema)
3. [Architettura del Progetto](#architettura-del-progetto)
4. [Componenti Principali](#componenti-principali)
5. [Tecnologie Utilizzate](#tecnologie-utilizzate)
6. [Flusso di Lavoro Dettagliato](#flusso-di-lavoro-dettagliato)
7. [Machine Learning e AI](#machine-learning-e-ai)
8. [Interfaccia Utente](#interfaccia-utente)
9. [API e Backend](#api-e-backend)
10. [Come Avviare il Progetto](#come-avviare-il-progetto)

---

## Panoramica del Progetto

**CV Job Matcher** è un'applicazione web intelligente che utilizza l'intelligenza artificiale per abbinare automaticamente i CV (curriculum vitae) delle persone con le offerte di lavoro più adatte.

### Cosa fa il progetto?
- **Carica un CV**: L'utente carica il suo curriculum in formato PDF
- **Analizza il contenuto**: L'AI estrae e analizza le competenze, esperienze e parole chiave
- **Trova i lavori migliori**: Il sistema confronta il profilo con un database di offerte di lavoro
- **Mostra i risultati**: Presenta le migliori corrispondenze con percentuali di compatibilità

### Perché è utile?
- **Risparmia tempo**: Non devi cercare manualmente tra centinaia di annunci
- **Risultati precisi**: L'AI capisce le competenze tecniche e fa abbinamenti intelligenti
- **Facilita la ricerca**: Ti mostra subito i lavori più adatti al tuo profilo

---

## Come Funziona il Sistema

### Il Processo in 4 Passi

1. **📥 Upload del CV**
   - L'utente trascina o seleziona un file PDF
   - Il sistema verifica che il file sia valido (massimo 10MB)

2. **🔍 Estrazione del Testo**
   - Il PDF viene processato per estrarre tutto il testo
   - Il testo viene pulito e preparato per l'analisi

3. **🧠 Analisi con AI**
   - L'intelligenza artificiale trasforma il testo in "numeri" (vettori)
   - Confronta questi numeri con quelli dei lavori nel database
   - Calcola la similarità usando formule matematiche

4. **📊 Presentazione Risultati**
   - Mostra i 6 lavori più compatibili
   - Per ogni lavoro indica la percentuale di compatibilità
   - Evidenzia le parole chiave in comune tra CV e offerta

---

## Architettura del Progetto

Il progetto è diviso in diverse cartelle, ognuna con un ruolo specifico:

```
cv-ranking/
├── main.py                    # File principale - avvia l'applicazione
├── requirements.txt           # Lista delle librerie Python necessarie
├── model/                     # Cartella con l'intelligenza artificiale
│   ├── job_ads.csv           # Database delle offerte di lavoro
│   ├── train_model.py        # Addestra i modelli AI
│   └── *.pkl                 # Modelli AI salvati
├── web/                      # Cartella dell'interfaccia web
│   ├── api.py               # API che gestisce le richieste
│   ├── utils.py             # Funzioni di supporto
│   ├── index.html           # Pagina web principale
│   └── static/              # CSS, JavaScript, immagini
└── tests/                   # Test per verificare che tutto funzioni
```

---

## Componenti Principali

### 1. **main.py** - Il Cuore dell'Applicazione
```python
from fastapi import FastAPI
from web.api import router

app = FastAPI()  # Crea l'applicazione web
app.include_router(router)  # Collega le API
```

**Cosa fa**: Questo file è come il "direttore d'orchestra" - coordina tutto il sistema e avvia il server web.

### 2. **web/api.py** - Le API (Interfacce di Comunicazione)

Le API sono come "camerieri" che prendono le richieste dell'utente e restituiscono le risposte:

- **`/`**: Mostra la pagina principale
- **`/api/analyze`**: Riceve il CV e restituisce i risultati
- **`/api/health`**: Verifica che il sistema funzioni

**Esempio di come funziona l'upload**:
```python
@router.post("/api/analyze")
async def analyze_cv_api(cvFile: UploadFile = File(...)):
    # 1. Controlla che il file sia PDF
    # 2. Estrae il testo dal PDF
    # 3. Trova i lavori più compatibili
    # 4. Restituisce i risultati in formato JSON
```

### 3. **web/utils.py** - Le Funzioni Intelligenti

Questo file contiene le funzioni più importanti per l'AI:

#### `extract_pdf_text(pdf_source)`
- **Cosa fa**: Estrae tutto il testo da un file PDF
- **Come**: Usa una libreria chiamata `pdfminer` che "legge" il PDF
- **Risultato**: Restituisce il testo pulito e in minuscolo

#### `find_top_matches(cv_text, k=6)`
- **Cosa fa**: Trova i 6 lavori più compatibili con il CV
- **Come**: 
  1. Trasforma il testo del CV in numeri (vettore)
  2. Confronta con i vettori di tutte le offerte di lavoro
  3. Calcola la similarità coseno (formula matematica)
  4. Ordina i risultati dal più compatibile al meno compatibile

#### `extract_keywords_from_texts(cv_text, job_text)`
- **Cosa fa**: Trova le parole chiave in comune tra CV e offerta di lavoro
- **Perché è utile**: Mostra all'utente perché quel lavoro è compatibile

### 4. **model/train_model.py** - L'Addestratore dei Modelli

Questo file "insegna" all'AI come capire i testi:

#### Preprocessing del Testo
```python
def preprocess_text(text: str) -> str:
    # 1. Converte tutto in minuscolo
    # 2. Rimuove parole comuni ("looking", "seeking", "role")
    # 3. Pulisce spazi extra
    return processed_text
```

#### Addestramento del Modello
```python
def train_embedding_model():
    # 1. Carica il dataset delle offerte di lavoro
    # 2. Preprocessa tutti i testi
    # 3. Usa SentenceTransformer per creare i vettori
    # 4. Salva il modello addestrato
```

---

## Tecnologie Utilizzate

### Backend (Lato Server)
- **FastAPI**: Framework web moderno e veloce per Python
- **uvicorn**: Server web per eseguire FastAPI
- **pandas**: Libreria per gestire dati e tabelle
- **scikit-learn**: Libreria per machine learning e calcoli matematici

### Intelligenza Artificiale
- **SentenceTransformers**: Modello AI che "capisce" il significato delle frasi
- **all-MiniLM-L6-v2**: Modello specifico ottimizzato per velocità e precisione
- **Cosine Similarity**: Formula matematica per calcolare quanto due testi sono simili

### Frontend (Lato Utente)
- **HTML5**: Struttura della pagina web
- **CSS3**: Stili e design responsivo
- **JavaScript (ES6+)**: Interattività e comunicazione con il server

### Strumenti di Supporto
- **pdfminer.six**: Estrazione testo da file PDF
- **pickle**: Salvataggio e caricamento dei modelli AI

---

## Flusso di Lavoro Dettagliato

### 1. Preparazione Iniziale (Quando si avvia l'app)

```python
# In web/utils.py - Si caricano i modelli addestrati
try:
    with open('model/sentence_embedding_model.pkl', 'rb') as f:
        loaded_vectorizer = pickle.load(f)  # Carica il modello AI
    
    with open('model/job_ads_embedding_vectors.pkl', 'rb') as f:
        loaded_job_ads_vectors = pickle.load(f)  # Carica i vettori dei lavori
    
    loaded_job_ads_df = pd.read_csv('model/job_ads.csv')  # Carica il database
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Inizializza l'AI
except:
    print("Errore nel caricamento dei modelli")
```

### 2. Upload del CV (Quando l'utente carica il file)

**Frontend (JavaScript)**:
```javascript
// L'utente seleziona il file
fileInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    
    // Controlla che sia un PDF
    if (file.type !== 'application/pdf') {
        alert('Please upload a PDF file');
        return;
    }
    
    // Invia il file al server
    uploadFile(file);
});
```

**Backend (Python)**:
```python
@router.post("/api/analyze")
async def analyze_cv_api(cvFile: UploadFile = File(...)):
    # 1. Validazione del file
    if cvFile.content_type not in ["application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # 2. Controllo dimensioni (max 10MB)
    content = await cvFile.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")
```

### 3. Estrazione e Preprocessing del Testo

```python
def extract_pdf_text(pdf_source):
    # 1. Estrae il testo grezzo dal PDF
    text = extract_text(pdf_source)
    
    # 2. Converte in minuscolo
    text = text.lower()
    
    # 3. Applica il preprocessing
    text = preprocess_text(text)
    
    return text

def preprocess_text(text: str) -> str:
    # 1. Rimuove parole comuni che non aggiungono significato
    common_words = ["looking", "seeking", "role", "position", ...]
    processed_text = re.sub(r'\b(?:' + '|'.join(common_words) + r')\b', '', text)
    
    # 2. Rimuove spazi multipli
    processed_text = re.sub(r'\s+', ' ', processed_text).strip()
    
    return processed_text
```

### 4. Matching con Intelligenza Artificiale

```python
def find_top_matches(cv_text: str, k: int = 6):
    # 1. Trasforma il testo del CV in vettore numerico
    cv_vector = model.encode([cv_text])  # Risultato: array di 384 numeri
    
    # 2. Calcola la similarità con tutti i lavori
    similarities = cosine_similarity(cv_vector, loaded_job_ads_vectors).flatten()
    
    # 3. Aggiunge le similarità al database
    results_df = loaded_job_ads_df.copy()
    results_df['similarity'] = similarities
    
    # 4. Ordina per similarità (dal più alto al più basso)
    sorted_results = results_df.sort_values(by='similarity', ascending=False)
    
    # 5. Prende i primi k risultati
    top_k_jobs = sorted_results.head(k)
    
    # 6. Prepara i risultati per l'interfaccia
    for i, job in enumerate(top_k_jobs_output):
        # Aggiunge la percentuale di compatibilità
        top_k_jobs_output[i]['similarity'] = round(float(similarities[i]), 4)
        
        # Aggiunge le parole chiave in comune
        top_k_jobs_output[i]['metrics'] = extract_keywords_from_texts(cv_text, job['Description'])
    
    return top_k_jobs_output
```

### 5. Analisi delle Parole Chiave

```python
def extract_keywords_from_texts(cv_text, job_text, top_k=10):
    # 1. Preprocessa entrambi i testi
    cv_preprocessed = preprocess_text(cv_text.lower())
    job_preprocessed = preprocess_text(job_text.lower())
    
    # 2. Trasforma in vettori TF-IDF (diverso da SentenceTransformer)
    cv_vector = loaded_vectorizer_tf.transform([cv_preprocessed])
    job_vector = loaded_vectorizer_tf.transform([job_preprocessed])
    
    # 3. Estrae le parole più importanti
    cv_keywords = dict(get_top_keywords(loaded_vectorizer_tf, cv_vector, top_k))
    job_keywords = dict(get_top_keywords(loaded_vectorizer_tf, job_vector, top_k))
    
    # 4. Trova le parole in comune
    common_keywords = set(cv_keywords.keys()) & set(job_keywords.keys())
    
    # 5. Crea un dizionario con i punteggi
    common_keywords_with_scores = {
        kw: (cv_keywords[kw], job_keywords[kw]) 
        for kw in common_keywords
    }
    
    return common_keywords_with_scores
```

---

## Machine Learning e AI

### Cos'è SentenceTransformer?

**SentenceTransformer** è un tipo speciale di intelligenza artificiale che "capisce" il significato delle frasi. È come avere un traduttore che converte le parole in numeri, ma mantenendo il significato.

#### Come Funziona:
1. **Input**: "Software engineer with Python experience"
2. **Processing**: L'AI analizza ogni parola e il contesto
3. **Output**: Un array di 384 numeri (vettore) che rappresenta il significato

#### Perché è Meglio di Altri Metodi:
- **TF-IDF** (metodo vecchio): Conta solo la frequenza delle parole
- **SentenceTransformer** (metodo nuovo): Capisce il significato e il contesto

**Esempio Pratico**:
- "Python developer" e "Python programmer" hanno significati simili
- TF-IDF vedrebbe parole diverse
- SentenceTransformer capisce che sono simili

### Similarità Coseno

La **similarità coseno** è una formula matematica che misura quanto due vettori sono simili:

```python
from sklearn.metrics.pairwise import cosine_similarity

# Vettore del CV: [0.2, 0.8, 0.1, ...]
# Vettore del lavoro: [0.3, 0.7, 0.2, ...]

similarity = cosine_similarity(cv_vector, job_vector)
# Risultato: numero tra 0 e 1
# 0 = completamente diversi
# 1 = identici
```

#### Interpretazione dei Risultati:
- **0.8-1.0**: Compatibilità eccellente
- **0.6-0.8**: Buona compatibilità  
- **0.4-0.6**: Compatibilità discreta
- **0.0-0.4**: Compatibilità bassa

---

## Interfaccia Utente

### Struttura della Pagina (HTML)

La pagina web è organizzata in sezioni:

```html
<div class="container">
    <!-- Header con logo e titolo -->
    <header class="header">
        <h1>CV Job Matcher</h1>
        <p>AI-powered job matching for your career</p>
    </header>

    <!-- Sezione upload del CV -->
    <section class="upload-section">
        <div class="upload-area">
            <!-- Area drag & drop -->
        </div>
        <button class="analyze-btn">Analyze CV</button>
    </section>

    <!-- Sezione loading (nascosta inizialmente) -->
    <section class="loading-section">
        <div class="loading-spinner"></div>
        <div class="progress-steps">
            <!-- Passi del processo -->
        </div>
    </section>

    <!-- Sezione risultati (nascosta inizialmente) -->
    <section class="results-section">
        <div class="results-grid">
            <!-- I risultati vengono inseriti qui -->
        </div>
    </section>
</div>
```

### Interattività (JavaScript)

Il JavaScript gestisce l'interazione con l'utente:

#### Upload del File
```javascript
// Gestisce il drag & drop
uploadArea.addEventListener('dragover', function(e) {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('drop', function(e) {
    e.preventDefault();
    const files = e.dataTransfer.files;
    handleFileSelect(files[0]);
});

// Gestisce la selezione tramite click
fileInput.addEventListener('change', function(e) {
    handleFileSelect(e.target.files[0]);
});
```

#### Comunicazione con il Server
```javascript
async function uploadFile(file) {
    // 1. Prepara i dati per l'invio
    const formData = new FormData();
    formData.append('cvFile', file);
    
    // 2. Mostra la schermata di caricamento
    showLoadingSection();
    
    try {
        // 3. Invia il file al server
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });
        
        // 4. Elabora la risposta
        const result = await response.json();
        
        if (result.success) {
            // 5. Mostra i risultati
            showResults(result.results);
        } else {
            showError(result.message);
        }
    } catch (error) {
        showError('Error occurred during upload');
    }
}
```

#### Visualizzazione dei Risultati
```javascript
function showResults(results) {
    const resultsGrid = document.getElementById('resultsGrid');
    resultsGrid.innerHTML = '';
    
    results.forEach((job, index) => {
        const jobCard = createJobCard(job, index + 1);
        resultsGrid.appendChild(jobCard);
    });
    
    // Nasconde loading e mostra risultati
    hideLoadingSection();
    showResultsSection();
}

function createJobCard(job, rank) {
    const compatibility = Math.round(job.similarity * 100);
    
    return `
        <div class="job-card">
            <div class="job-header">
                <h3>${job.Company} - ${job.Role}</h3>
                <div class="compatibility-badge">
                    ${compatibility}% Match
                </div>
            </div>
            <p class="job-description">${job.Description}</p>
            <div class="job-keywords">
                <!-- Parole chiave in comune -->
            </div>
            <a href="${job['Job Link']}" target="_blank" class="apply-btn">
                View Job
            </a>
        </div>
    `;
}
```

---

## API e Backend

### Struttura delle API

Il sistema usa **FastAPI**, un framework moderno per creare API veloci e sicure.

#### Endpoint Principali:

##### 1. **GET /** - Pagina Principale
```python
@router.get("/", response_class=HTMLResponse)
def home():
    with open("web/index.html", "r", encoding="utf-8") as f:
        return f.read()
```
- **Cosa fa**: Restituisce la pagina HTML principale
- **Quando viene chiamata**: Quando l'utente visita il sito

##### 2. **POST /api/analyze** - Analisi del CV
```python
@router.post("/api/analyze")
async def analyze_cv_api(cvFile: UploadFile = File(...)):
    try:
        # Validazione del file
        allowed_types = ["application/pdf"]
        if cvFile.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        # Controllo dimensioni
        content = await cvFile.read()
        if len(content) > 10 * 1024 * 1024:  # 10MB
            raise HTTPException(status_code=400, detail="File too large")
        
        # Estrazione testo
        pdf_stream = BytesIO(content)
        text = extract_pdf_text(pdf_stream)
        
        # Controllo testo valido
        if not text or text.strip() == "":
            raise HTTPException(status_code=400, detail="Could not extract text")
        
        # Matching con AI
        results = find_top_matches(text)
        
        # Risposta JSON
        return JSONResponse(content={
            "success": True,
            "message": "CV analyzed successfully",
            "results": results,
            "total_matches": len(results)
        })
        
    except HTTPException:
        raise  # Riporta l'errore HTTP
    except Exception as e:
        print(f"Error in CV analysis: {e}")
        raise HTTPException(status_code=500, detail="Processing error")
```

##### 3. **GET /api/health** - Controllo Stato
```python
@router.get("/api/health")
async def health_check():
    return JSONResponse(content={
        "status": "healthy",
        "message": "CV Job Matcher API is running"
    })
```
- **Cosa fa**: Verifica che il sistema funzioni correttamente
- **Quando viene chiamata**: Per il monitoraggio del sistema

### Gestione degli Errori

Il sistema gestisce diversi tipi di errori:

#### 1. **Errori di Validazione**
```python
# File non valido
if cvFile.content_type not in allowed_types:
    raise HTTPException(
        status_code=400, 
        detail="Invalid file type. Please upload a PDF file."
    )

# File troppo grande
if len(content) > 10 * 1024 * 1024:
    raise HTTPException(
        status_code=400, 
        detail="File size too large. Maximum size is 10MB."
    )
```

#### 2. **Errori di Processing**
```python
# Testo non estratto
if not text or text.strip() == "":
    raise HTTPException(
        status_code=400, 
        detail="Could not extract text from the uploaded file."
    )
```

#### 3. **Errori del Server**
```python
except Exception as e:
    print(f"Error in CV analysis: {e}")
    raise HTTPException(
        status_code=500, 
        detail="An error occurred while processing your CV."
    )
```

---

## Come Avviare il Progetto

### Prerequisiti

1. **Python 3.8+** installato sul computer
2. **pip** (gestore pacchetti Python)
3. **Git** (opzionale, per scaricare il codice)

### Passo 1: Scaricare il Progetto
```bash
# Se hai Git installato
git clone <url-del-repository>
cd cv-ranking

# Oppure scarica e estrai il file ZIP
```

### Passo 2: Installare le Dipendenze
```bash
# Installa tutte le librerie necessarie
pip install -r requirements.txt
```

### Passo 3: Preparare i Modelli AI
```bash
# Vai nella cartella model
cd model

# Esegui l'addestramento (se necessario)
python train_model.py
```

### Passo 4: Avviare l'Applicazione
```bash
# Torna nella cartella principale
cd ..

# Avvia il server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Passo 5: Usare l'Applicazione
1. Apri il browser
2. Vai su `http://localhost:8000`
3. Carica un CV in formato PDF
4. Aspetta i risultati!

### Risoluzione Problemi Comuni

#### Errore: "ModuleNotFoundError"
```bash
# Assicurati di essere nella cartella giusta
pwd  # Dovrebbe mostrare la cartella del progetto

# Reinstalla le dipendenze
pip install -r requirements.txt
```

#### Errore: "Port already in use"
```bash
# Usa una porta diversa
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

#### Errore: "Model files not found"
```bash
# Esegui l'addestramento dei modelli
cd model
python train_model.py
cd ..
```

---

## File di Configurazione

### requirements.txt
```txt
beautifulsoup4==4.13.4      # Per parsing HTML (se necessario)
fastapi==0.116.1            # Framework web principale
pandas==2.3.1               # Gestione dati e CSV
pdfminer_six==20250506      # Estrazione testo da PDF
Requests==2.32.4            # Richieste HTTP
scikit_learn==1.7.1         # Machine learning e matematica
starlette==0.47.2           # Base per FastAPI
gunicorn                    # Server per produzione
uvicorn                     # Server per sviluppo
itsdangerous                # Sicurezza delle sessioni
python-multipart            # Upload file
sentence-transformers       # AI per comprensione testi
```

### Procfile (per Heroku)
```
web: gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

## Considerazioni di Sicurezza

### Validazione File
- Controlla il tipo di file (solo PDF)
- Limita la dimensione (max 10MB)
- Verifica il contenuto estratto

### Gestione Errori
- Non espone informazioni sensibili negli errori
- Log degli errori per il debugging
- Risposte standardizzate per gli utenti

### Sicurezza Sessioni
```python
import secrets
secret_key = secrets.token_urlsafe(32)
app.add_middleware(SessionMiddleware, secret_key=secret_key)
```

---

## Possibili Miglioramenti Futuri

1. **Database Reale**: Usare PostgreSQL invece di CSV
2. **Autenticazione**: Login utenti e salvataggio cronologia
3. **Più Formati**: Supporto per DOCX e altri formati
4. **AI Migliorata**: Modelli più grandi e precisi
5. **Cache**: Memorizzare risultati per velocizzare
6. **API Esterne**: Integrare con siti di lavoro reali
7. **Mobile App**: Versione per smartphone

---

## Conclusione

Questo progetto dimostra come l'intelligenza artificiale possa essere utilizzata per risolvere problemi reali. Combina diverse tecnologie moderne:

- **Backend robusto** con FastAPI
- **AI avanzata** con SentenceTransformers  
- **Interfaccia utente moderna** con HTML5/CSS3/JS
- **Architettura scalabile** e manutenibile

È un ottimo esempio di come la programmazione moderna possa creare soluzioni utili e intelligenti per aiutare le persone nella ricerca del lavoro.

---

*Documentazione creata per il progetto CV Job Matcher*  
*Autore: Analisi del codice sorgente*  
*Data: 2025*