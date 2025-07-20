import requests
from bs4 import BeautifulSoup
import json
import time
import random
from urllib.parse import urljoin, quote_plus
from abc import ABC, abstractmethod
import logging

# Configurazione logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class JobScraper(ABC):
    """Classe astratta per definire l'interfaccia dei scraper"""
    
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    @abstractmethod
    def build_search_url(self, keyword, location="", page=0):
        """Costruisce l'URL di ricerca per il sito specifico"""
        pass
    
    @abstractmethod
    def parse_job_listings(self, soup):
        """Estrae le offerte di lavoro dalla pagina"""
        pass
    
    @abstractmethod
    def parse_job_details(self, job_element):
        """Estrae i dettagli di una singola offerta"""
        pass
    
    def get_page(self, url, max_retries=3):
        """Effettua la richiesta HTTP con retry automatico"""
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                logger.warning(f"Tentativo {attempt + 1} fallito per {url}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(random.uniform(2, 5))
                else:
                    logger.error(f"Impossibile recuperare {url}")
                    return None
    
    def scrape_jobs(self, keyword, location="", max_pages=3):
        """Metodo principale per il scraping"""
        all_jobs = []
        
        for page in range(max_pages):
            logger.info(f"Scraping pagina {page + 1} per '{keyword}' su {self.__class__.__name__}")
            
            search_url = self.build_search_url(keyword, location, page)
            response = self.get_page(search_url)
            
            if not response:
                continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            job_listings = self.parse_job_listings(soup)
            
            if not job_listings:
                logger.info("Nessuna offerta trovata, interruzione")
                break
            
            for job_element in job_listings:
                try:
                    job_data = self.parse_job_details(job_element)
                    if job_data:
                        all_jobs.append(job_data)
                except Exception as e:
                    logger.warning(f"Errore nel parsing di un'offerta: {e}")
            
            # Pausa tra le richieste per evitare di essere bloccati
            time.sleep(random.uniform(1, 3))
        
        return all_jobs

class IndeedScraper(JobScraper):
    """Scraper per Indeed.it"""
    
    def __init__(self):
        super().__init__("https://it.indeed.com")
    
    def build_search_url(self, keyword, location="", page=0):
        start = page * 10  # Indeed usa start invece di page
        keyword_encoded = quote_plus(keyword)
        location_encoded = quote_plus(location)
        return f"{self.base_url}/jobs?q={keyword_encoded}&l={location_encoded}&start={start}"
    
    def parse_job_listings(self, soup):
        # Indeed usa diverse strutture, proviamo entrambe
        jobs = soup.find_all('div', {'data-jk': True})  # Nuova struttura
        if not jobs:
            jobs = soup.find_all('a', {'data-jk': True})  # Struttura alternativa
        return jobs
    
    def parse_job_details(self, job_element):
        try:
           #Title
            title_elem = job_element.find('h2', class_='jobTitle') or job_element.find('a', {'data-jk': True})
            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # link
            link_elem = job_element.find('h2', class_='jobTitle')
            if link_elem:
                link_tag = link_elem.find('a')
                link = urljoin(self.base_url, link_tag['href']) if link_tag and link_tag.get('href') else "N/A"
            else:
                job_key = job_element.get('data-jk')
                link = f"{self.base_url}/viewjob?jk={job_key}" if job_key else "N/A"
            
            # snippet
            desc_elem = job_element.find('div', class_='job-snippet') or job_element.find('span', {'title': True})
            description = desc_elem.get_text(strip=True) if desc_elem else "N/A"
            
            # Company
            company_elem = job_element.find('span', class_='companyName') or job_element.find('a', {'data-testid': 'company-name'})
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            
            return {
                "title": title,
                "link": link,
                "description": description,
                "company": company,
                "source": "Indeed"
            }
        except Exception as e:
            logger.error(f"Errore nel parsing Indeed: {e}")
            return None

class LinkedInScraper(JobScraper):
    """Scraper for LinkedIn """
    
    def __init__(self):
        super().__init__("https://www.linkedin.com")
    
    def build_search_url(self, keyword, location="", page=0):
        keyword_encoded = quote_plus(keyword)
        location_encoded = quote_plus(location)
        start = page * 25
        return f"{self.base_url}/jobs/search/?keywords={keyword_encoded}&location={location_encoded}&start={start}"
    
    def parse_job_listings(self, soup):
        return soup.find_all('div', class_='base-card')
    
    def parse_job_details(self, job_element):
        try:
            # Titolo
            title_elem = job_element.find('h3', class_='base-search-card__title')
            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # Link
            link_elem = job_element.find('a', class_='base-card__full-link')
            link = link_elem['href'] if link_elem and link_elem.get('href') else "N/A"
            
            # Azienda
            company_elem = job_element.find('h4', class_='base-search-card__subtitle')
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            
            # Descrizione (limitata su LinkedIn)
            description = f"Posizione presso {company}"
            
            return {
                "title": title,
                "link": link,
                "description": description,
                "company": company,
                "source": "LinkedIn"
            }
        except Exception as e:
            logger.error(f"Errore nel parsing LinkedIn: {e}")
            return None

class InfoJobsScraper(JobScraper):
    """Scraper per InfoJobs.it"""
    
    def __init__(self):
        super().__init__("https://www.infojobs.it")
    
    def build_search_url(self, keyword, location="", page=0):
        keyword_encoded = quote_plus(keyword)
        return f"{self.base_url}/offerte-lavoro/?keyword={keyword_encoded}&page={page + 1}"
    
    def parse_job_listings(self, soup):
        return soup.find_all('div', class_='offer-item') or soup.find_all('article', class_='offer')
    
    def parse_job_details(self, job_element):
        try:
            # Titolo
            title_elem = job_element.find('h2') or job_element.find('h3')
            title_link = title_elem.find('a') if title_elem else None
            title = title_link.get_text(strip=True) if title_link else "N/A"
            
            # Link
            link = urljoin(self.base_url, title_link['href']) if title_link and title_link.get('href') else "N/A"
            
            # Descrizione
            desc_elem = job_element.find('div', class_='description') or job_element.find('p')
            description = desc_elem.get_text(strip=True) if desc_elem else "N/A"
            
            # Azienda
            company_elem = job_element.find('div', class_='company-name') or job_element.find('strong')
            company = company_elem.get_text(strip=True) if company_elem else "N/A"
            
            return {
                "title": title,
                "link": link,
                "description": description,
                "company": company,
                "source": "InfoJobs"
            }
        except Exception as e:
            logger.error(f"Errore nel parsing InfoJobs: {e}")
            return None

class JobScraperManager:
    """Manager per gestire multiple scrapers"""
    
    def __init__(self):
        self.scrapers = {
            'indeed': IndeedScraper(),
            'linkedin': LinkedInScraper(),
            'infojobs': InfoJobsScraper()
        }
    
    def scrape_all_sites(self, keyword, location="", max_pages=2, sites=None):
        """Scrape da tutti i siti o solo da quelli specificati"""
        if sites is None:
            sites = list(self.scrapers.keys())
        
        all_results = []
        
        for site_name in sites:
            if site_name in self.scrapers:
                logger.info(f"Inizio scraping da {site_name}")
                try:
                    scraper = self.scrapers[site_name]
                    jobs = scraper.scrape_jobs(keyword, location, max_pages)
                    all_results.extend(jobs)
                    logger.info(f"Trovate {len(jobs)} offerte su {site_name}")
                except Exception as e:
                    logger.error(f"Errore durante lo scraping di {site_name}: {e}")
            else:
                logger.warning(f"Scraper per {site_name} non trovato")
        
        return all_results
    
    def save_to_json(self, data, filename="job_results.json"):
        """Salva i risultati in un file JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    "total_jobs": len(data),
                    "jobs": data
                }, f, indent=2, ensure_ascii=False)
            logger.info(f"Risultati salvati in {filename}")
        except Exception as e:
            logger.error(f"Errore nel salvare il file: {e}")

def main():
    """Funzione principale per testare lo scraper"""
    
    # Configurazione della ricerca
    KEYWORD = "sviluppatore python"  # Modifica qui la keyword
    LOCATION = "Milano"              # Modifica qui la location
    MAX_PAGES = 2                    # Numero di pagine da scrapare per sito
    SITES = ['indeed']               # ['indeed', 'linkedin', 'infojobs'] per tutti
    
    # Inizializzazione del manager
    manager = JobScraperManager()
    
    print(f"🔍 Inizio ricerca per '{KEYWORD}' in {LOCATION}")
    print(f"📝 Siti da cercare: {', '.join(SITES)}")
    print("-" * 50)
    
    # Esecuzione dello scraping
    results = manager.scrape_all_sites(
        keyword=KEYWORD,
        location=LOCATION,
        max_pages=MAX_PAGES,
        sites=SITES
    )
    
    # Salvataggio risultati
    manager.save_to_json(results)
    
    # Stampa sommario
    print("\n" + "="*50)
    print(f"✅ Scraping completato! Trovate {len(results)} offerte totali")
    
    # Mostra le prime 3 offerte come esempio
    for i, job in enumerate(results[:3]):
        print(f"\n{i+1}. {job['title']} - {job['company']} ({job['source']})")
        print(f"   📄 {job['description'][:100]}...")
        print(f"   🔗 {job['link']}")

if __name__ == "__main__":
    
    main()
       
    manager = JobScraperManager()

 
    # Da tutti i siti
    results = manager.scrape_all_sites(
        keyword="frontend developer",
        location="Milano",
        max_pages=2,
        sites=['indeed', 'linkedin', 'infojobs']
    )

    # Salvare in JSON
    manager.save_to_json(results, "mie_offerte.json")