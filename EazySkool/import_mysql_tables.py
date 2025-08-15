#!/usr/bin/env python3
"""
Script pour importer automatiquement les tables MySQL pour EazySkool
"""

import mysql.connector
from mysql.connector import Error
import os

def import_mysql_tables():
    """Importe les tables MySQL depuis le fichier SQL"""
    print("🗄️ Import des tables MySQL pour EazySkool")
    print("=" * 50)
    
    # Paramètres de connexion
    host = 'localhost'
    user = 'root'
    password = ''
    database = 'eazyskool'
    port = 3306
    
    try:
        # Connexion à MySQL
        print("🔌 Connexion à MySQL...")
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        
        if connection.is_connected():
            print("✅ Connexion MySQL réussie!")
            
            cursor = connection.cursor()
            
            # Créer la base de données si elle n'existe pas
            print("📊 Création de la base de données...")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ Base de données '{database}' créée ou existante")
            
            # Sélectionner la base de données
            cursor.execute(f"USE {database}")
            
            # Lire le fichier SQL
            sql_file = 'eazyskool_mysql.sql'
            if not os.path.exists(sql_file):
                print(f"❌ Fichier {sql_file} non trouvé!")
                return False
            
            print(f"📖 Lecture du fichier {sql_file}...")
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            # Exécuter le script SQL
            print("🚀 Exécution du script SQL...")
            
            # Diviser le script en commandes individuelles
            commands = sql_script.split(';')
            
            for i, command in enumerate(commands):
                command = command.strip()
                if command and not command.startswith('--'):
                    try:
                        cursor.execute(command)
                        print(f"✅ Commande {i+1} exécutée")
                    except Error as e:
                        if "already exists" not in str(e).lower():
                            print(f"⚠️ Commande {i+1}: {e}")
            
            # Valider les changements
            connection.commit()
            print("✅ Toutes les tables ont été créées avec succès!")
            
            # Vérifier les tables créées
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"📋 Tables créées ({len(tables)}):")
            for table in tables:
                print(f"   - {table[0]}")
            
            # Vérifier les données
            cursor.execute("SELECT COUNT(*) FROM schools")
            school_count = cursor.fetchone()[0]
            print(f"📚 Écoles: {school_count}")
            
            cursor.execute("SELECT COUNT(*) FROM cities")
            city_count = cursor.fetchone()[0]
            print(f"🏙️ Villes: {city_count}")
            
            cursor.execute("SELECT COUNT(*) FROM school_types")
            type_count = cursor.fetchone()[0]
            print(f"🎓 Types d'écoles: {type_count}")
            
            cursor.execute("SELECT COUNT(*) FROM specializations")
            spec_count = cursor.fetchone()[0]
            print(f"🎯 Spécialisations: {spec_count}")
            
            cursor.execute("SELECT COUNT(*) FROM events")
            event_count = cursor.fetchone()[0]
            print(f"📅 Événements: {event_count}")
            
            cursor.close()
            connection.close()
            
            print("\n🎉 Import terminé avec succès!")
            print("🌐 Accès phpMyAdmin: http://localhost/phpmyadmin")
            print("📊 Base de données: eazyskool")
            
            return True
            
    except Error as e:
        print(f"❌ Erreur MySQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_connection_after_import():
    """Teste la connexion après l'import"""
    print("\n🔍 Test de connexion après import...")
    
    try:
        from mysql_database_manager import test_mysql_connection
        if test_mysql_connection():
            print("✅ Connexion réussie après import!")
            return True
        else:
            print("❌ Échec de la connexion après import")
            return False
    except Exception as e:
        print(f"❌ Erreur de test: {e}")
        return False

if __name__ == "__main__":
    print("🎓 EazySkool - Import des tables MySQL")
    print("=" * 50)
    
    # Importer les tables
    if import_mysql_tables():
        # Tester la connexion
        test_connection_after_import()
        
        print("\n📋 Prochaines étapes:")
        print("1. Démarrer l'API: python mysql_api_server.py")
        print("2. Tester l'API: python test_mysql_api.py")
        print("3. Ouvrir phpMyAdmin: http://localhost/phpmyadmin")
        print("4. Accéder à l'interface: index.html")
    else:
        print("\n❌ Échec de l'import")
        print("💡 Vérifiez que:")
        print("   - WampServer est démarré")
        print("   - MySQL est en cours d'exécution")
        print("   - L'utilisateur 'root' a les permissions") 