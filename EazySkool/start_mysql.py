#!/usr/bin/env python3
"""
Script de démarrage pour EazySkool avec MySQL
"""

import os
import sys
import subprocess
import webbrowser
import time

def check_python_dependencies():
    """Vérifie et installe les dépendances Python"""
    print("🔍 Vérification des dépendances Python...")
    
    try:
        import mysql.connector
        import flask
        import flask_cors
        import bcrypt
        print("✅ Toutes les dépendances sont installées")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("📦 Installation des dépendances...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dépendances installées avec succès")
            return True
        except subprocess.CalledProcessError:
            print("❌ Erreur lors de l'installation des dépendances")
            return False

def test_mysql_connection():
    """Teste la connexion à MySQL"""
    print("🔍 Test de connexion MySQL...")
    
    try:
        from mysql_database_manager import test_mysql_connection
        if test_mysql_connection():
            print("✅ Connexion MySQL réussie!")
            return True
        else:
            print("❌ Échec de la connexion MySQL")
            print("💡 Vérifiez que:")
            print("   - WampServer est démarré")
            print("   - MySQL est en cours d'exécution")
            print("   - La base de données 'eazyskool' existe")
            print("   - L'utilisateur 'root' a les bonnes permissions")
            return False
    except Exception as e:
        print(f"❌ Erreur de test MySQL: {e}")
        return False

def start_api_server():
    """Démarre le serveur API Flask"""
    print("🚀 Démarrage du serveur API...")
    
    try:
        # Démarrer le serveur en arrière-plan
        process = subprocess.Popen([
            sys.executable, "mysql_api_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Attendre un peu pour que le serveur démarre
        time.sleep(3)
        
        # Vérifier si le processus fonctionne
        if process.poll() is None:
            print("✅ Serveur API démarré avec succès")
            return process
        else:
            print("❌ Erreur lors du démarrage du serveur")
            return None
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

def open_browser():
    """Ouvre le navigateur sur l'application"""
    print("🌐 Ouverture du navigateur...")
    
    try:
        # Ouvrir l'API
        webbrowser.open("http://localhost:5000")
        print("✅ Navigateur ouvert sur l'API")
        
        # Ouvrir l'interface web si elle existe
        if os.path.exists("index.html"):
            webbrowser.open("file://" + os.path.abspath("index.html"))
            print("✅ Navigateur ouvert sur l'interface web")
    except Exception as e:
        print(f"❌ Erreur lors de l'ouverture du navigateur: {e}")

def main():
    """Fonction principale"""
    print("🎓 EazySkool - Démarrage avec MySQL")
    print("=" * 50)
    
    # Vérifier les dépendances
    if not check_python_dependencies():
        print("❌ Impossible de continuer sans les dépendances")
        return
    
    # Tester la connexion MySQL
    if not test_mysql_connection():
        print("\n📋 Instructions pour résoudre le problème:")
        print("1. Ouvrez WampServer")
        print("2. Vérifiez que l'icône est verte")
        print("3. Allez dans phpMyAdmin (http://localhost/phpmyadmin)")
        print("4. Créez une base de données nommée 'eazyskool'")
        print("5. Importez le fichier 'eazyskool_mysql.sql'")
        print("6. Relancez ce script")
        return
    
    # Démarrer le serveur API
    server_process = start_api_server()
    if not server_process:
        print("❌ Impossible de démarrer le serveur API")
        return
    
    # Ouvrir le navigateur
    open_browser()
    
    print("\n🎉 Application EazySkool démarrée!")
    print("📊 Base de données: MySQL")
    print("🌐 API: http://localhost:5000")
    print("📚 Documentation API: http://localhost:5000")
    print("\n💡 Pour arrêter l'application, fermez cette fenêtre")
    
    try:
        # Attendre que l'utilisateur ferme la fenêtre
        input("\nAppuyez sur Entrée pour arrêter l'application...")
    except KeyboardInterrupt:
        pass
    finally:
        if server_process:
            print("🛑 Arrêt du serveur...")
            server_process.terminate()
            server_process.wait()
            print("✅ Serveur arrêté")

if __name__ == "__main__":
    main() 