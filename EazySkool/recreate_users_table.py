#!/usr/bin/env python3
"""
Script pour recréer la table users avec la bonne structure
"""

import mysql.connector
from mysql.connector import Error

def recreate_users_table():
    """Recrée la table users avec la bonne structure"""
    print("🔧 Recréation de la table users")
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
            
            # Créer la nouvelle table users
            print("🏗️ Création de la nouvelle table users...")
            cursor.execute("""
                CREATE TABLE users (
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
            
            print("\n🎉 Table users recréée avec succès!")
            return True
            
    except Error as e:
        print(f"❌ Erreur MySQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def create_auth_api():
    """Crée l'API d'authentification"""
    print("\n🔧 Création de l'API d'authentification...")
    
    auth_api_code = '''
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import bcrypt
from datetime import datetime

app = Flask(__name__)
CORS(app)

def get_db_connection():
    """Crée une connexion à la base de données"""
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='eazyskool',
        charset='utf8mb4'
    )

@app.route('/')
def home():
    """Page d'accueil de l'API d'authentification"""
    return jsonify({
        'message': 'API d\'authentification EazySkool',
        'version': '1.0.0',
        'endpoints': [
            'POST /api/auth/register - Inscription',
            'POST /api/auth/login - Connexion',
            'GET /api/users - Liste des utilisateurs'
        ]
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Inscription d'un nouvel utilisateur"""
    try:
        data = request.get_json()
        
        # Vérifier les champs requis
        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Champ requis manquant: {field}'
                }), 400
        
        email = data['email']
        password = data['password']
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        city = data.get('city', '')
        
        # Hasher le mot de passe
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Connexion à la base de données
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Vérifier si l'email existe déjà
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({
                'success': False,
                'error': 'Cet email est déjà utilisé'
            }), 400
        
        # Insérer le nouvel utilisateur
        cursor.execute("""
            INSERT INTO users (email, password_hash, first_name, last_name, city) 
            VALUES (%s, %s, %s, %s, %s)
        """, (email, password_hash, first_name, last_name, city))
        
        user_id = cursor.lastrowid
        connection.commit()
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Utilisateur créé avec succès',
            'user_id': user_id
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Connexion d'un utilisateur"""
    try:
        data = request.get_json()
        
        # Vérifier les champs requis
        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Champ requis manquant: {field}'
                }), 400
        
        email = data['email']
        password = data['password']
        
        # Connexion à la base de données
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Récupérer l'utilisateur
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            # Ne pas renvoyer le hash du mot de passe
            user_data = {
                'id': user['id'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'city': user['city'],
                'created_at': user['created_at'].isoformat() if user['created_at'] else None
            }
            
            cursor.close()
            connection.close()
            
            return jsonify({
                'success': True,
                'message': 'Connexion réussie',
                'user': user_data
            })
        else:
            cursor.close()
            connection.close()
            
            return jsonify({
                'success': False,
                'error': 'Email ou mot de passe incorrect'
            }), 401
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    """Récupère la liste des utilisateurs (sans mots de passe)"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT id, email, first_name, last_name, city, created_at FROM users")
        users = cursor.fetchall()
        
        # Convertir les dates en chaînes
        for user in users:
            if user['created_at']:
                user['created_at'] = user['created_at'].isoformat()
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'data': users,
            'count': len(users)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🔐 API d'authentification EazySkool")
    print("🌐 URL: http://localhost:5001")
    print("📚 Endpoints:")
    print("   - GET  /")
    print("   - POST /api/auth/register")
    print("   - POST /api/auth/login")
    print("   - GET  /api/users")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
'''
    
    with open('auth_api.py', 'w', encoding='utf-8') as f:
        f.write(auth_api_code)
    
    print("✅ API d'authentification créée: auth_api.py")

if __name__ == "__main__":
    print("🎓 EazySkool - Recréation de la table users")
    print("=" * 50)
    
    if recreate_users_table():
        create_auth_api()
        
        print("\n📋 Prochaines étapes:")
        print("1. Démarrer l'API d'auth: python auth_api.py")
        print("2. Tester l'API: http://localhost:5001")
        print("3. Utilisateurs de test disponibles:")
        print("   - admin@eazyskool.fr / admin123")
        print("   - user1@eazyskool.fr / user123")
        print("   - user2@eazyskool.fr / user456")
        print("   - user3@eazyskool.fr / user789")
    else:
        print("\n❌ Échec de la recréation")
        print("💡 Vérifiez que la base de données est créée") 