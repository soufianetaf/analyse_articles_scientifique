import requests
from bs4 import BeautifulSoup

def fetch_arxiv_articles(query="machine learning", max_results=8000):
    """
    Scraping des articles depuis arXiv.
    """
    base_url = "https://arxiv.org/search/"
    articles = []
    results_per_page = 50  # arXiv affiche 50 articles par page
    
    for start in range(0, max_results, results_per_page):
        params = {
            "query": query,
            "searchtype": "all",
            "abstracts": "show",
            "order": "submitted_date",
            "size": results_per_page,
            "start": start
        }
        
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            print(f"Erreur lors de la récupération des articles arXiv: {response.status_code}")
            continue
        
        soup = BeautifulSoup(response.text, "html.parser")
        entries = soup.find_all("li", class_="arxiv-result")
        
        for entry in entries:
            title = entry.find("p", class_="title is-5 mathjax").text.strip()
            authors = entry.find("p", class_="authors").text.replace("Authors:", "").strip()
            abstract = entry.find("span", class_="abstract-full has-text-grey-dark mathjax").text.strip()
            url = entry.find("p", class_="list-title is-inline-block").find("a")["href"]
            
            articles.append({
                "source": "arXiv",
                "article_id": url.split("/")[-1],
                "title": title,
                "authors": authors,
                "publication_date": None,  # Date non disponible dans le listing
                "abstract": abstract,
                "url": url
            })
    
    return articles

if __name__ == "__main__":
    articles = fetch_arxiv_articles()
    print(f"Récupéré {len(articles)} articles depuis arXiv.")
