#!/usr/bin/env python3
"""
Script corrigé pour importer les tables MySQL
"""

import mysql.connector
from mysql.connector import Error
import os

def create_database_and_tables():
    """Crée la base de données et les tables"""
    print("🗄️ Création de la base de données EazySkool")
    print("=" * 50)
    
    try:
        # Connexion à MySQL
        print("🔌 Connexion à MySQL...")
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            port=3306,
            charset='utf8mb4'
        )
        
        if connection.is_connected():
            print("✅ Connexion MySQL réussie!")
            cursor = connection.cursor()
            
            # Créer la base de données
            print("📊 Création de la base de données...")
            cursor.execute("CREATE DATABASE IF NOT EXISTS eazyskool CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            cursor.execute("USE eazyskool")
            print("✅ Base de données 'eazyskool' créée")
            
            # Créer les tables une par une
            print("🏗️ Création des tables...")
            
            # Table users
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    first_name VARCHAR(100),
                    last_name VARCHAR(100),
                    city VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            print("✅ Table 'users' créée")
            
            # Table school_types
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS school_types (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT
                )
            """)
            print("✅ Table 'school_types' créée")
            
            # Table cities
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cities (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    region VARCHAR(100)
                )
            """)
            print("✅ Table 'cities' créée")
            
            # Table schools
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS schools (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    address TEXT,
                    phone VARCHAR(20),
                    email VARCHAR(255),
                    website VARCHAR(255),
                    city_id INT,
                    school_type_id INT,
                    rating DECIMAL(3,2) DEFAULT 0.00,
                    price_range VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (city_id) REFERENCES cities(id),
                    FOREIGN KEY (school_type_id) REFERENCES school_types(id)
                )
            """)
            print("✅ Table 'schools' créée")
            
            # Table school_images
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS school_images (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    school_id INT,
                    image_url VARCHAR(500) NOT NULL,
                    is_primary BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE
                )
            """)
            print("✅ Table 'school_images' créée")
            
            # Table specializations
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS specializations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT
                )
            """)
            print("✅ Table 'specializations' créée")
            
            # Table school_specializations
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS school_specializations (
                    school_id INT,
                    specialization_id INT,
                    PRIMARY KEY (school_id, specialization_id),
                    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
                    FOREIGN KEY (specialization_id) REFERENCES specializations(id) ON DELETE CASCADE
                )
            """)
            print("✅ Table 'school_specializations' créée")
            
            # Table reviews
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    school_id INT,
                    user_id INT,
                    rating INT,
                    comment TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            print("✅ Table 'reviews' créée")
            
            # Table favorites
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS favorites (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    school_id INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_user_school (user_id, school_id)
                )
            """)
            print("✅ Table 'favorites' créée")
            
            # Table events
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    event_date DATE,
                    event_time TIME,
                    location VARCHAR(255),
                    school_id INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE
                )
            """)
            print("✅ Table 'events' créée")
            
            # Insérer les données
            print("📝 Insertion des données...")
            
            # Types d'écoles (avec échappement des caractères spéciaux)
            school_types_data = [
                ("Ecole de commerce", "Formation en management et commerce"),
                ("Ecole d'ingenieur", "Formation en ingenierie et sciences"),
                ("Ecole d'art", "Formation en arts et design"),
                ("Ecole de communication", "Formation en communication et medias"),
                ("Ecole de sante", "Formation en sante et paramedical"),
                ("Ecole de droit", "Formation en droit et sciences juridiques")
            ]
            
            for name, description in school_types_data:
                cursor.execute("INSERT IGNORE INTO school_types (name, description) VALUES (%s, %s)", (name, description))
            print("✅ Types d'écoles insérés")
            
            # Villes
            cities_data = [
                ("Strasbourg", "Grand Est"),
                ("Nancy", "Grand Est"),
                ("Metz", "Grand Est"),
                ("Reims", "Grand Est"),
                ("Troyes", "Grand Est"),
                ("Chalons-en-Champagne", "Grand Est")
            ]
            
            for name, region in cities_data:
                cursor.execute("INSERT IGNORE INTO cities (name, region) VALUES (%s, %s)", (name, region))
            print("✅ Villes insérées")
            
            # Spécialisations
            specializations_data = [
                ("Marketing Digital", "Formation en marketing digital et e-commerce"),
                ("Intelligence Artificielle", "Formation en IA et machine learning"),
                ("Finance", "Formation en finance et gestion"),
                ("Informatique", "Formation en developpement et systemes"),
                ("Design Graphique", "Formation en design et creation"),
                ("Communication", "Formation en communication et medias"),
                ("Sante", "Formation en sante et bien-etre"),
                ("Droit", "Formation en droit et legislation")
            ]
            
            for name, description in specializations_data:
                cursor.execute("INSERT IGNORE INTO specializations (name, description) VALUES (%s, %s)", (name, description))
            print("✅ Spécialisations insérées")
            
            # Écoles
            schools_data = [
                ("EM Strasbourg", "Ecole de management de Strasbourg", "61 Avenue de la Foret-Noire, 67085 Strasbourg", "03 88 41 77 77", "contact@em-strasbourg.eu", "https://www.em-strasbourg.eu", 1, 1, 4.5, "8000-12000€"),
                ("INSA Strasbourg", "Institut National des Sciences Appliquees", "24 Boulevard de la Victoire, 67084 Strasbourg", "03 88 14 47 00", "contact@insa-strasbourg.fr", "https://www.insa-strasbourg.fr", 1, 2, 4.3, "600€"),
                ("ESAD Strasbourg", "Ecole Superieure d'Art Dramatique", "7 Rue de l'Academie, 67000 Strasbourg", "03 88 25 69 74", "contact@esad-stg.fr", "https://www.esad-stg.fr", 1, 3, 4.1, "400€"),
                ("ICN Business School", "Ecole de commerce a Nancy", "86 Rue du Sergent Blandan, 54003 Nancy", "03 54 50 25 00", "contact@icn-artem.com", "https://www.icn-artem.com", 2, 1, 4.2, "9000-11000€"),
                ("CentraleSupelec Metz", "Ecole d'ingenieur", "2 Rue Edouard Belin, 57070 Metz", "03 87 34 69 00", "contact@centralesupelec.fr", "https://www.centralesupelec.fr", 3, 2, 4.4, "600€"),
                ("NEOMA Business School", "Ecole de commerce a Reims", "59 Rue Pierre Taittinger, 51100 Reims", "03 26 77 46 00", "contact@neoma-bs.fr", "https://www.neoma-bs.fr", 4, 1, 4.0, "8500-11500€"),
                ("UTT Troyes", "Universite de Technologie de Troyes", "12 Rue Marie Curie, 10004 Troyes", "03 25 71 76 00", "contact@utt.fr", "https://www.utt.fr", 5, 2, 4.2, "600€"),
                ("ESC Troyes", "Ecole Superieure de Commerce", "217 Avenue Pierre Brossolette, 10000 Troyes", "03 25 49 49 49", "contact@esctroyes.fr", "https://www.esctroyes.fr", 5, 1, 3.9, "7500-9500€")
            ]
            
            for school in schools_data:
                cursor.execute("""
                    INSERT IGNORE INTO schools (name, description, address, phone, email, website, city_id, school_type_id, rating, price_range) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, school)
            print("✅ Écoles insérées")
            
            # Images d'écoles
            images_data = [
                (1, "https://example.com/em-strasbourg.jpg", True),
                (2, "https://example.com/insa-strasbourg.jpg", True),
                (3, "https://example.com/esad-strasbourg.jpg", True),
                (4, "https://example.com/icn-nancy.jpg", True),
                (5, "https://example.com/centralesupelec-metz.jpg", True),
                (6, "https://example.com/neoma-reims.jpg", True),
                (7, "https://example.com/utt-troyes.jpg", True),
                (8, "https://example.com/esc-troyes.jpg", True)
            ]
            
            for image in images_data:
                cursor.execute("INSERT IGNORE INTO school_images (school_id, image_url, is_primary) VALUES (%s, %s, %s)", image)
            print("✅ Images d'écoles insérées")
            
            # Liaisons écoles-spécialisations
            specializations_links = [
                (1, 1), (1, 3), (2, 4), (2, 2), (3, 5), (3, 6), (4, 1), (4, 3),
                (5, 4), (5, 2), (6, 1), (6, 3), (7, 4), (7, 2), (8, 1), (8, 3)
            ]
            
            for link in specializations_links:
                cursor.execute("INSERT IGNORE INTO school_specializations (school_id, specialization_id) VALUES (%s, %s)", link)
            print("✅ Liaisons écoles-spécialisations insérées")
            
            # Événements
            events_data = [
                ("Journee Portes Ouvertes", "Decouvrez notre ecole et nos formations", "2024-03-15", "09:00:00", "Campus principal", 1),
                ("Conference IA", "L'intelligence artificielle dans l'education", "2024-03-20", "14:00:00", "Amphitheatre A", 2),
                ("Workshop Design", "Atelier de design graphique", "2024-03-25", "10:00:00", "Atelier creatif", 3),
                ("Salon des metiers", "Rencontrez les professionnels", "2024-04-10", "13:00:00", "Hall d'exposition", 4)
            ]
            
            for event in events_data:
                cursor.execute("""
                    INSERT IGNORE INTO events (title, description, event_date, event_time, location, school_id) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, event)
            print("✅ Événements insérés")
            
            # Valider les changements
            connection.commit()
            
            # Vérifier les données
            cursor.execute("SELECT COUNT(*) FROM schools")
            school_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM cities")
            city_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM school_types")
            type_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM specializations")
            spec_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM events")
            event_count = cursor.fetchone()[0]
            
            print(f"\n📊 Statistiques:")
            print(f"   📚 Écoles: {school_count}")
            print(f"   🏙️ Villes: {city_count}")
            print(f"   🎓 Types d'écoles: {type_count}")
            print(f"   🎯 Spécialisations: {spec_count}")
            print(f"   📅 Événements: {event_count}")
            
            cursor.close()
            connection.close()
            
            print("\n🎉 Base de données créée avec succès!")
            print("🌐 Accès phpMyAdmin: http://localhost/phpmyadmin")
            print("📊 Base de données: eazyskool")
            
            return True
            
    except Error as e:
        print(f"❌ Erreur MySQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("🎓 EazySkool - Création de la base de données MySQL")
    print("=" * 50)
    
    if create_database_and_tables():
        print("\n📋 Prochaines étapes:")
        print("1. Démarrer l'API: python mysql_api_server.py")
        print("2. Tester l'API: python test_mysql_api.py")
        print("3. Ouvrir phpMyAdmin: http://localhost/phpmyadmin")
        print("4. Accéder à l'interface: index.html")
    else:
        print("\n❌ Échec de la création")
        print("💡 Vérifiez que WampServer est démarré et MySQL fonctionne") 