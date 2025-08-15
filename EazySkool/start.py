#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de démarrage EazySkool
Lance l'application complète avec base de données et API
"""

import sys
import os
import subprocess
import time
import webbrowser
from pathlib import Path

# Ajoute le répertoire du projet au path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config import validate_config, API_HOST, API_PORT
from database_manager import EazySkoolDB

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    required_packages = ['flask', 'flask-cors', 'bcrypt']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Dépendances manquantes:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nInstallez-les avec:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ Toutes les dépendances sont installées")
    return True

def setup_database():
    """Configure la base de données"""
    print("\n🗄️  Configuration de la base de données...")
    
    try:
        db = EazySkoolDB()
        print("✅ Base de données configurée")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la configuration de la base de données: {e}")
        return False

def start_api_server():
    """Démarre le serveur API"""
    print("\n🚀 Démarrage du serveur API...")
    
    try:
        # Import ici pour éviter les conflits
        from api_server import app
        
        print(f"✅ Serveur API démarré sur http://{API_HOST}:{API_PORT}")
        print("📖 Documentation: http://localhost:5000/")
        print("🔗 Endpoints disponibles:")
        print("  - GET  /api/schools")
        print("  - GET  /api/schools/search")
        print("  - POST /api/auth/login")
        print("  - POST /api/auth/register")
        print("  - GET  /api/favorites")
        print("  - POST /api/reviews")
        
        # Ouvre le navigateur automatiquement
        time.sleep(2)
        webbrowser.open(f"http://localhost:{API_PORT}")
        
        # Lance le serveur
        app.run(
            host=API_HOST,
            port=API_PORT,
            debug=True,
            use_reloader=False  # Évite le double démarrage
        )
        
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur: {e}")
        return False

def show_usage():
    """Affiche les instructions d'utilisation"""
    print("\n📖 UTILISATION:")
    print("1. Ouvrez votre navigateur sur http://localhost:5000")
    print("2. Testez l'API avec les endpoints listés ci-dessus")
    print("3. Pour utiliser avec le frontend:")
    print("   - Remplacez script.js par script_with_api.js")
    print("   - Ou modifiez index.html pour utiliser l'API")
    print("\n🛠️  OUTILS DISPONIBLES:")
    print("- python database_manager.py  # Gestion de la DB")
    print("- python test_api.py          # Tests de l'API")
    print("- python config.py            # Configuration")

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🎓 EazySkool - Démarrage de l'application")
    print("=" * 60)
    
    # Vérifie la configuration
    if not validate_config():
        print("❌ Configuration invalide. Arrêt.")
        return 1
    
    # Vérifie les dépendances
    if not check_dependencies():
        return 1
    
    # Configure la base de données
    if not setup_database():
        return 1
    
    # Affiche les instructions
    show_usage()
    
    # Démarre le serveur
    try:
        start_api_server()
    except KeyboardInterrupt:
        print("\n\n👋 Arrêt du serveur...")
        return 0
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 