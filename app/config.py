"""
Configuration de l'application Ymmo.
Les valeurs sensibles sont chargées depuis le fichier .env (voir .env.example).
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration de base, commune à tous les environnements."""

    SECRET_KEY = os.getenv("SECRET_KEY", "change-moi-en-production")

    # --- Connexion MySQL ---
    # Format : mysql+pymysql://utilisateur:motdepasse@hote:port/nom_base
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "ymmo")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False