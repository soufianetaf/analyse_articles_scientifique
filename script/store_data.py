import psycopg2
from database.db_connection import get_db_connection

def insert_articles(articles):
    """
    Insère une liste d'articles dans la base de données PostgreSQL.
    """
    conn = get_db_connection()
    if conn is None:
        print("Connexion à la base de données impossible.")
        return
    
    try:
        with conn.cursor() as cursor:
            query = """
            INSERT INTO articles (source, article_id, title, authors, publication_date, abstract, url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (article_id) DO NOTHING;
            """
            
            for article in articles:
                cursor.execute(query, (
                    article["source"],
                    article["article_id"],
                    article["title"],
                    article["authors"],
                    article["publication_date"],
                    article["abstract"],
                    article["url"]
                ))
        conn.commit()
        print(f"{len(articles)} articles insérés dans la base de données.")
    except Exception as e:
        print(f"Erreur lors de l'insertion des articles : {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    # Exemple de test avec une liste d'articles factices
    sample_articles = [
        {
            "source": "arXiv",
            "article_id": "12345",
            "title": "Deep Learning for AI",
            "authors": "John Doe, Jane Smith",
            "publication_date": "2024-02-01",
            "abstract": "Cet article explore les avancées du deep learning...",
            "url": "https://arxiv.org/abs/12345"
        }
    ]
    insert_articles(sample_articles)
