#!/usr/bin/env python3
"""
Script pour tester l'authentification et le stockage des emails/mots de passe
"""

import mysql.connector
from mysql.connector import Error
import bcrypt

def test_user_creation():
    """Teste la création d'utilisateurs avec email et mot de passe"""
    print("🔐 Test d'authentification MySQL")
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
            
            # Vérifier que la table users existe
            cursor.execute("SHOW TABLES LIKE 'users'")
            if not cursor.fetchone():
                print("❌ Table 'users' n'existe pas!")
                return False
            
            print("✅ Table 'users' trouvée")
            
            # Créer un utilisateur de test
            test_email = "test@example.com"
            test_password = "motdepasse123"
            test_first_name = "Jean"
            test_last_name = "Dupont"
            test_city = "Strasbourg"
            
            # Hasher le mot de passe
            password_hash = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Insérer l'utilisateur
            cursor.execute("""
                INSERT INTO users (email, password_hash, first_name, last_name, city) 
                VALUES (%s, %s, %s, %s, %s)
            """, (test_email, password_hash, test_first_name, test_last_name, test_city))
            
            connection.commit()
            print("✅ Utilisateur créé avec succès!")
            print(f"   Email: {test_email}")
            print(f"   Nom: {test_first_name} {test_last_name}")
            print(f"   Ville: {test_city}")
            
            # Récupérer l'ID de l'utilisateur créé
            user_id = cursor.lastrowid
            print(f"   ID: {user_id}")
            
            # Tester l'authentification
            print("\n🔍 Test d'authentification...")
            
            # Récupérer l'utilisateur par email
            cursor.execute("SELECT * FROM users WHERE email = %s", (test_email,))
            user = cursor.fetchone()
            
            if user:
                stored_password_hash = user[2]  # password_hash est à l'index 2
                
                # Vérifier le mot de passe
                if bcrypt.checkpw(test_password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                    print("✅ Authentification réussie!")
                    print(f"   Utilisateur: {user[4]} {user[5]}")  # first_name, last_name
                    print(f"   Email: {user[1]}")  # email
                    print(f"   Ville: {user[6]}")  # city
                else:
                    print("❌ Échec de l'authentification - mot de passe incorrect")
            else:
                print("❌ Utilisateur non trouvé")
            
            # Afficher tous les utilisateurs
            print("\n📋 Liste des utilisateurs:")
            cursor.execute("SELECT id, email, first_name, last_name, city, created_at FROM users")
            users = cursor.fetchall()
            
            for user in users:
                print(f"   ID: {user[0]}, Email: {user[1]}, Nom: {user[2]} {user[3]}, Ville: {user[4]}")
            
            cursor.close()
            connection.close()
            
            print("\n🎉 Test d'authentification terminé!")
            return True
            
    except Error as e:
        print(f"❌ Erreur MySQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def create_auth_api():
    """Crée un script API pour l'authentification"""
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
    print("   - POST /api/auth/register")
    print("   - POST /api/auth/login")
    print("   - GET  /api/users")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
'''
    
    with open('auth_api.py', 'w', encoding='utf-8') as f:
        f.write(auth_api_code)
    
    print("✅ API d'authentification créée: auth_api.py")

if __name__ == "__main__":
    print("🎓 EazySkool - Test d'authentification")
    print("=" * 50)
    
    # Tester la création d'utilisateurs
    if test_user_creation():
        # Créer l'API d'authentification
        create_auth_api()
        
        print("\n📋 Prochaines étapes:")
        print("1. Démarrer l'API d'auth: python auth_api.py")
        print("2. Tester l'inscription: POST http://localhost:5001/api/auth/register")
        print("3. Tester la connexion: POST http://localhost:5001/api/auth/login")
        print("4. Voir les utilisateurs: GET http://localhost:5001/api/users")
    else:
        print("\n❌ Échec du test d'authentification")
        print("💡 Vérifiez que la base de données est créée") 