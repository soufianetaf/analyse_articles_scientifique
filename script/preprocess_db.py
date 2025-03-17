import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) 
import psycopg2
from database.db_connection import get_db_connection
from preprocessing import preprocess_text

def fetch_articles():
    """
    Récupère les articles depuis la base de données.
    """
    conn = get_db_connection()
    if conn is None:
        print("Erreur de connexion à la base de données.")
        return []
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, abstract FROM articles WHERE abstract IS NOT NULL")
            articles = cursor.fetchall()
        return articles
    except Exception as e:
        print(f"Erreur lors de la récupération des articles : {e}")
        return []
    finally:
        conn.close()

def update_article(article_id, processed_text):
    """
    Met à jour l'article avec le texte prétraité.
    """
    conn = get_db_connection()
    if conn is None:
        return
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE articles SET abstract = %s WHERE id = %s
            """, (processed_text, article_id))
        conn.commit()
    except Exception as e:
        print(f"Erreur lors de la mise à jour de l'article {article_id} : {e}")
        conn.rollback()
    finally:
        conn.close()

def preprocess_articles():
    """
    Applique le prétraitement à tous les articles et met à jour la base de données.
    """
    articles = fetch_articles()
    print(f"{len(articles)} articles à prétraiter...")
    
    for article_id, abstract in articles:
        processed_text = preprocess_text(abstract)
        update_article(article_id, processed_text)
    
    print("Prétraitement terminé !")

if __name__ == "__main__":
    preprocess_articles()
