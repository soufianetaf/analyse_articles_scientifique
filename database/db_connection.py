import psycopg2
from psycopg2 import sql
import os

def get_db_connection():
    """
    Établit une connexion à la base de données PostgreSQL.
    """
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "analyse_articles"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "0000"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432")
        )
        return conn
    except Exception as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return None

def execute_query(query, params=None):
    """
    Exécute une requête SQL avec gestion automatique de la connexion.
    """
    conn = get_db_connection()
    if conn is None:
        return
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
    except Exception as e:
        print(f"Erreur lors de l'exécution de la requête : {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    # Test de connexion
    conn = get_db_connection()
    if conn:
        print("Connexion réussie à PostgreSQL !")
        conn.close()
