#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration EazySkool
Fichier de configuration centralisé pour l'application
"""

import os
from pathlib import Path

# =================================================================================
# CONFIGURATION DE BASE
# =================================================================================

# Répertoire du projet
PROJECT_ROOT = Path(__file__).parent

# Base de données
DATABASE_PATH = PROJECT_ROOT / "eazyskool.db"
DATABASE_SQL_PATH = PROJECT_ROOT / "database.sql"

# Serveur API
API_HOST = "0.0.0.0"
API_PORT = 5000
API_DEBUG = True

# Configuration CORS
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "file://",  # Pour les fichiers HTML locaux
]

# =================================================================================
# CONFIGURATION DE SÉCURITÉ
# =================================================================================

# Clé secrète pour Flask (à changer en production)
SECRET_KEY = os.environ.get('SECRET_KEY', 'eazyskool-dev-secret-key-change-in-production')

# Configuration bcrypt
BCRYPT_ROUNDS = 12

# =================================================================================
# CONFIGURATION DES DONNÉES
# =================================================================================

# Limites par défaut
DEFAULT_SCHOOLS_PER_PAGE = 6
DEFAULT_EVENTS_LIMIT = 10
DEFAULT_REVIEWS_LIMIT = 50

# Types d'écoles supportés
SCHOOL_TYPES = [
    "Université",
    "École de commerce", 
    "Institut d'études politiques",
    "École d'ingénieur",
    "École d'art",
    "École de santé"
]

# Villes du Grand Est
GRAND_EST_CITIES = [
    "Strasbourg",
    "Nancy", 
    "Mulhouse",
    "Metz",
    "Reims",
    "Troyes"
]

# Spécialités disponibles
SPECIALIZATIONS = [
    "Informatique",
    "Médecine",
    "Droit", 
    "Commerce",
    "Ingénierie",
    "Arts",
    "Sciences",
    "Langues"
]

# =================================================================================
# CONFIGURATION DES LOGS
# =================================================================================

# Niveau de log
LOG_LEVEL = "INFO"

# Format des logs
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# =================================================================================
# CONFIGURATION DE DÉVELOPPEMENT
# =================================================================================

# Mode développement
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# Auto-reload
AUTO_RELOAD = DEBUG

# =================================================================================
# FONCTIONS UTILITAIRES
# =================================================================================

def get_database_url():
    """Retourne l'URL de la base de données"""
    return f"sqlite:///{DATABASE_PATH}"

def ensure_directories():
    """Crée les répertoires nécessaires"""
    directories = [
        PROJECT_ROOT / "logs",
        PROJECT_ROOT / "exports",
        PROJECT_ROOT / "uploads"
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)

def get_config():
    """Retourne la configuration complète"""
    return {
        'database_path': str(DATABASE_PATH),
        'api_host': API_HOST,
        'api_port': API_PORT,
        'debug': DEBUG,
        'cors_origins': CORS_ORIGINS,
        'school_types': SCHOOL_TYPES,
        'cities': GRAND_EST_CITIES,
        'specializations': SPECIALIZATIONS
    }

# =================================================================================
# VALIDATION DE CONFIGURATION
# =================================================================================

def validate_config():
    """Valide la configuration"""
    errors = []
    
    # Vérifie que les fichiers nécessaires existent
    if not DATABASE_SQL_PATH.exists():
        errors.append(f"Fichier SQL manquant: {DATABASE_SQL_PATH}")
    
    # Vérifie les permissions
    try:
        PROJECT_ROOT.mkdir(exist_ok=True)
    except PermissionError:
        errors.append(f"Pas de permission d'écriture dans: {PROJECT_ROOT}")
    
    if errors:
        print("Erreurs de configuration:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    return True

if __name__ == "__main__":
    print("Configuration EazySkool:")
    print(f"  Répertoire projet: {PROJECT_ROOT}")
    print(f"  Base de données: {DATABASE_PATH}")
    print(f"  Serveur API: {API_HOST}:{API_PORT}")
    print(f"  Mode debug: {DEBUG}")
    print(f"  Types d'écoles: {len(SCHOOL_TYPES)}")
    print(f"  Villes: {len(GRAND_EST_CITIES)}")
    print(f"  Spécialités: {len(SPECIALIZATIONS)}")
    
    if validate_config():
        print("✅ Configuration valide")
    else:
        print("❌ Configuration invalide") 