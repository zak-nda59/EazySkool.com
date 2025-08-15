#!/usr/bin/env python3
"""
Script corrigé pour créer la table users
"""

import mysql.connector
from mysql.connector import Error

def create_users_table():
    """Crée la table users avec la bonne structure"""
    print("🔧 Création de la table users")
    print("=" * 50)
    
    try:
        # Connexion à MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='eazyskool',
            charset='utf8mb4'
        )
        
        if connection.is_connected():
            print("✅ Connexion MySQL réussie!")
            cursor = connection.cursor()
            
            # Supprimer la table users existante
            print("🗑️ Suppression de la table users existante...")
            cursor.execute("DROP TABLE IF EXISTS users")
            connection.commit()
            print("✅ Table users supprimée")
            
            # Créer la nouvelle table users avec des contraintes corrigées
            print("🏗️ Création de la nouvelle table users...")
            cursor.execute("""
                CREATE TABLE users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    city VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            connection.commit()
            print("✅ Nouvelle table users créée")
            
            # Vérifier la structure
            cursor.execute("DESCRIBE users")
            columns = cursor.fetchall()
            
            print("\n📋 Structure de la nouvelle table users:")
            for column in columns:
                print(f"   - {column[0]} ({column[1]})")
            
            # Créer un utilisateur admin
            print("\n👤 Création de l'utilisateur admin...")
            
            import bcrypt
            
            admin_email = "admin@eazyskool.fr"
            admin_password = "admin123"
            admin_first_name = "Admin"
            admin_last_name = "EazySkool"
            admin_city = "Strasbourg"
            
            # Hasher le mot de passe
            password_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Insérer l'utilisateur admin
            cursor.execute("""
                INSERT INTO users (email, password_hash, first_name, last_name, city) 
                VALUES (%s, %s, %s, %s, %s)
            """, (admin_email, password_hash, admin_first_name, admin_last_name, admin_city))
            
            connection.commit()
            print("✅ Utilisateur admin créé avec succès!")
            print(f"   Email: {admin_email}")
            print(f"   Mot de passe: {admin_password}")
            print(f"   Nom: {admin_first_name} {admin_last_name}")
            
            # Créer quelques utilisateurs de test
            test_users = [
                ("user1@eazyskool.fr", "user123", "Jean", "Dupont", "Strasbourg"),
                ("user2@eazyskool.fr", "user456", "Marie", "Martin", "Nancy"),
                ("user3@eazyskool.fr", "user789", "Pierre", "Durand", "Metz")
            ]
            
            print("\n👥 Création d'utilisateurs de test...")
            for email, password, first_name, last_name, city in test_users:
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                cursor.execute("""
                    INSERT INTO users (email, password_hash, first_name, last_name, city) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (email, password_hash, first_name, last_name, city))
                
                print(f"   ✅ {email} créé")
            
            connection.commit()
            
            # Afficher tous les utilisateurs
            print("\n📋 Liste des utilisateurs:")
            cursor.execute("SELECT id, email, first_name, last_name, city, created_at FROM users")
            users = cursor.fetchall()
            
            for user in users:
                print(f"   ID: {user[0]}, Email: {user[1]}, Nom: {user[2]} {user[3]}, Ville: {user[4]}")
            
            cursor.close()
            connection.close()
            
            print("\n🎉 Table users créée avec succès!")
            return True
            
    except Error as e:
        print(f"❌ Erreur MySQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_auth():
    """Teste l'authentification"""
    print("\n🔐 Test d'authentification...")
    
    try:
        import bcrypt
        
        # Connexion à MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='eazyskool',
            charset='utf8mb4'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Tester la connexion avec l'utilisateur admin
            test_email = "admin@eazyskool.fr"
            test_password = "admin123"
            
            cursor.execute("SELECT * FROM users WHERE email = %s", (test_email,))
            user = cursor.fetchone()
            
            if user:
                stored_password_hash = user[2]  # password_hash
                
                if bcrypt.checkpw(test_password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                    print("✅ Authentification réussie!")
                    print(f"   Utilisateur: {user[4]} {user[5]}")  # first_name, last_name
                    print(f"   Email: {user[1]}")  # email
                    print(f"   Ville: {user[6]}")  # city
                else:
                    print("❌ Échec de l'authentification")
            else:
                print("❌ Utilisateur non trouvé")
            
            cursor.close()
            connection.close()
            
    except Exception as e:
        print(f"❌ Erreur de test: {e}")

if __name__ == "__main__":
    print("🎓 EazySkool - Création de la table users")
    print("=" * 50)
    
    if create_users_table():
        test_auth()
        
        print("\n📋 Prochaines étapes:")
        print("1. Démarrer l'API d'auth: python auth_api.py")
        print("2. Tester l'API: http://localhost:5001")
        print("3. Utilisateurs de test disponibles:")
        print("   - admin@eazyskool.fr / admin123")
        print("   - user1@eazyskool.fr / user123")
        print("   - user2@eazyskool.fr / user456")
        print("   - user3@eazyskool.fr / user789")
    else:
        print("\n❌ Échec de la création")
        print("💡 Vérifiez que la base de données est créée") 