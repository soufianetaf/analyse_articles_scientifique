import requests
from bs4 import BeautifulSoup
import re

def fetch_pubmed_articles(query="artificial intelligence", max_results=8000):
    """
    Scraping des articles depuis PubMed sur l'Intelligence Artificielle.
    """
    base_url = "https://pubmed.ncbi.nlm.nih.gov/"
    articles = []
    results_per_page = 200  # PubMed affiche jusqu'à 200 résultats par page
    
    for start in range(0, max_results, results_per_page):
        response = requests.get(f"{base_url}?term={query}&size={results_per_page}&page={start // results_per_page + 1}")
        
        if response.status_code != 200:
            print(f"Erreur lors de la récupération des articles PubMed: {response.status_code}")
            continue
        
        soup = BeautifulSoup(response.text, "html.parser")
        entries = soup.find_all("article", class_="full-docsum")
        
        for entry in entries:
            title_tag = entry.find("a", class_="docsum-title")
            title = title_tag.text.strip() if title_tag else ""
            url = base_url + title_tag["href"] if title_tag else ""
            
            authors_tag = entry.find("span", class_="docsum-authors full-authors")
            authors = authors_tag.text.strip() if authors_tag else ""
            
            date_tag = entry.find("span", class_="docsum-journal-citation full-journal-citation")
            raw_date = date_tag.text.strip().split(".")[0] if date_tag else ""
            
            # Vérification si la date est bien une année (YYYY)
            publication_date = raw_date if re.match(r'^\d{4}$', raw_date) else None
            
            articles.append({
                "source": "PubMed",
                "article_id": url.split("/")[-2] if url else "",
                "title": title,
                "authors": authors,
                "publication_date": publication_date,
                "abstract": "",  # L'abstract nécessite un scraping détaillé par article
                "url": url
            })
    
    return articles

if __name__ == "__main__":
    articles = fetch_pubmed_articles()
    print(f"Récupéré {len(articles)} articles depuis PubMed sur l'IA.")
