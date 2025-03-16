import requests
from bs4 import BeautifulSoup
import time
import random

def fetch_semantic_scholar_articles(query="machine learning", max_results=4000):
    """
    Scraping des articles depuis Semantic Scholar avec gestion des pauses et User-Agent dynamique.
    """
    base_url = "https://www.semanticscholar.org/search"
    articles = []
    results_per_page = 10  # Semantic Scholar affiche 10 résultats par page
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    ]
    
    for start in range(0, max_results, results_per_page):
        url = f"{base_url}?q={query}&sort=relevance&page={start // results_per_page + 1}"
        headers = {"User-Agent": random.choice(user_agents)}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Erreur lors de la récupération des articles Semantic Scholar: {response.status_code}")
                time.sleep(10)  # Pause plus longue en cas d'erreur
                continue
            
            soup = BeautifulSoup(response.text, "html.parser")
            entries = soup.find_all("div", class_="cl-paper-row")
            
            for entry in entries:
                title_tag = entry.find("a", class_="cl-paper-title")
                title = title_tag.text.strip() if title_tag else ""
                url = "https://www.semanticscholar.org" + title_tag["href"] if title_tag else ""
                
                authors_tag = entry.find("span", class_="cl-paper-authors")
                authors = authors_tag.text.strip() if authors_tag else ""
                
                date_tag = entry.find("span", class_="cl-paper-year")
                publication_date = date_tag.text.strip() if date_tag and date_tag.text.isdigit() else None
                
                articles.append({
                    "source": "Semantic Scholar",
                    "article_id": url.split("/")[-1] if url else "",
                    "title": title,
                    "authors": authors,
                    "publication_date": publication_date,
                    "abstract": "",  # L'abstract nécessite un scraping détaillé par article
                    "url": url
                })
            
            # Pause aléatoire pour éviter le blocage
            time.sleep(random.uniform(5, 10))
        
        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion : {e}")
            time.sleep(15)  # Pause plus longue avant de réessayer
            continue
    
    return articles

if __name__ == "__main__":
    articles = fetch_semantic_scholar_articles()
    print(f"Récupéré {len(articles)} articles depuis Semantic Scholar.")
