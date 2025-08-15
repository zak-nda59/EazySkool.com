#!/usr/bin/env python3
"""
Script simplifié pour importer les tables MySQL
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
            port=3306
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
            
            # Types d'écoles
            cursor.execute("""
                INSERT IGNORE INTO school_types (name, description) VALUES
                ('École de commerce', 'Formation en management et commerce'),
                ('École d\'ingénieur', 'Formation en ingénierie et sciences'),
                ('École d\'art', 'Formation en arts et design'),
                ('École de communication', 'Formation en communication et médias'),
                ('École de santé', 'Formation en santé et paramédical'),
                ('École de droit', 'Formation en droit et sciences juridiques')
            """)
            print("✅ Types d'écoles insérés")
            
            # Villes
            cursor.execute("""
                INSERT IGNORE INTO cities (name, region) VALUES
                ('Strasbourg', 'Grand Est'),
                ('Nancy', 'Grand Est'),
                ('Metz', 'Grand Est'),
                ('Reims', 'Grand Est'),
                ('Troyes', 'Grand Est'),
                ('Châlons-en-Champagne', 'Grand Est')
            """)
            print("✅ Villes insérées")
            
            # Spécialisations
            cursor.execute("""
                INSERT IGNORE INTO specializations (name, description) VALUES
                ('Marketing Digital', 'Formation en marketing digital et e-commerce'),
                ('Intelligence Artificielle', 'Formation en IA et machine learning'),
                ('Finance', 'Formation en finance et gestion'),
                ('Informatique', 'Formation en développement et systèmes'),
                ('Design Graphique', 'Formation en design et création'),
                ('Communication', 'Formation en communication et médias'),
                ('Santé', 'Formation en santé et bien-être'),
                ('Droit', 'Formation en droit et législation')
            """)
            print("✅ Spécialisations insérées")
            
            # Écoles
            cursor.execute("""
                INSERT IGNORE INTO schools (name, description, address, phone, email, website, city_id, school_type_id, rating, price_range) VALUES
                ('EM Strasbourg', 'École de management de Strasbourg', '61 Avenue de la Forêt-Noire, 67085 Strasbourg', '03 88 41 77 77', 'contact@em-strasbourg.eu', 'https://www.em-strasbourg.eu', 1, 1, 4.5, '8000-12000€'),
                ('INSA Strasbourg', 'Institut National des Sciences Appliquées', '24 Boulevard de la Victoire, 67084 Strasbourg', '03 88 14 47 00', 'contact@insa-strasbourg.fr', 'https://www.insa-strasbourg.fr', 1, 2, 4.3, '600€'),
                ('ESAD Strasbourg', 'École Supérieure d\'Art Dramatique', '7 Rue de l\'Académie, 67000 Strasbourg', '03 88 25 69 74', 'contact@esad-stg.fr', 'https://www.esad-stg.fr', 1, 3, 4.1, '400€'),
                ('ICN Business School', 'École de commerce à Nancy', '86 Rue du Sergent Blandan, 54003 Nancy', '03 54 50 25 00', 'contact@icn-artem.com', 'https://www.icn-artem.com', 2, 1, 4.2, '9000-11000€'),
                ('CentraleSupélec Metz', 'École d\'ingénieur', '2 Rue Édouard Belin, 57070 Metz', '03 87 34 69 00', 'contact@centralesupelec.fr', 'https://www.centralesupelec.fr', 3, 2, 4.4, '600€'),
                ('NEOMA Business School', 'École de commerce à Reims', '59 Rue Pierre Taittinger, 51100 Reims', '03 26 77 46 00', 'contact@neoma-bs.fr', 'https://www.neoma-bs.fr', 4, 1, 4.0, '8500-11500€'),
                ('UTT Troyes', 'Université de Technologie de Troyes', '12 Rue Marie Curie, 10004 Troyes', '03 25 71 76 00', 'contact@utt.fr', 'https://www.utt.fr', 5, 2, 4.2, '600€'),
                ('ESC Troyes', 'École Supérieure de Commerce', '217 Avenue Pierre Brossolette, 10000 Troyes', '03 25 49 49 49', 'contact@esctroyes.fr', 'https://www.esctroyes.fr', 5, 1, 3.9, '7500-9500€')
            """)
            print("✅ Écoles insérées")
            
            # Images d'écoles
            cursor.execute("""
                INSERT IGNORE INTO school_images (school_id, image_url, is_primary) VALUES
                (1, 'https://example.com/em-strasbourg.jpg', TRUE),
                (2, 'https://example.com/insa-strasbourg.jpg', TRUE),
                (3, 'https://example.com/esad-strasbourg.jpg', TRUE),
                (4, 'https://example.com/icn-nancy.jpg', TRUE),
                (5, 'https://example.com/centralesupelec-metz.jpg', TRUE),
                (6, 'https://example.com/neoma-reims.jpg', TRUE),
                (7, 'https://example.com/utt-troyes.jpg', TRUE),
                (8, 'https://example.com/esc-troyes.jpg', TRUE)
            """)
            print("✅ Images d'écoles insérées")
            
            # Liaisons écoles-spécialisations
            cursor.execute("""
                INSERT IGNORE INTO school_specializations (school_id, specialization_id) VALUES
                (1, 1), (1, 3), (2, 4), (2, 2), (3, 5), (3, 6), (4, 1), (4, 3),
                (5, 4), (5, 2), (6, 1), (6, 3), (7, 4), (7, 2), (8, 1), (8, 3)
            """)
            print("✅ Liaisons écoles-spécialisations insérées")
            
            # Événements
            cursor.execute("""
                INSERT IGNORE INTO events (title, description, event_date, event_time, location, school_id) VALUES
                ('Journée Portes Ouvertes', 'Découvrez notre école et nos formations', '2024-03-15', '09:00:00', 'Campus principal', 1),
                ('Conférence IA', 'L\'intelligence artificielle dans l\'éducation', '2024-03-20', '14:00:00', 'Amphithéâtre A', 2),
                ('Workshop Design', 'Atelier de design graphique', '2024-03-25', '10:00:00', 'Atelier créatif', 3),
                ('Salon des métiers', 'Rencontrez les professionnels', '2024-04-10', '13:00:00', 'Hall d\'exposition', 4)
            """)
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