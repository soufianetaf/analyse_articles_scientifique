from script.arxiv_extraction import fetch_arxiv_articles
from script.pubmed_extraction import fetch_pubmed_articles
from script.store_data import insert_articles

def main():
    print("Démarrage du scraping des articles...")
    
    # Scraping des articles
    print("Scraping des articles depuis arXiv...")
    arxiv_articles = fetch_arxiv_articles()
    print(f"{len(arxiv_articles)} articles récupérés depuis arXiv.")
    
    print("Scraping des articles depuis PubMed...")
    pubmed_articles = fetch_pubmed_articles()
    print(f"{len(pubmed_articles)} articles récupérés depuis PubMed.")
    
    # Fusion des données
    all_articles = arxiv_articles + pubmed_articles
    print(f"Total des articles récupérés : {len(all_articles)}")
    
    # Stockage des articles en base de données
    print("Insertion des articles dans la base de données...")
    insert_articles(all_articles)
    print("Processus terminé avec succès !")

if __name__ == "__main__":
    main()
