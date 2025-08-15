#!/usr/bin/env python3
"""
Script pour vérifier et corriger la structure de la table users
"""

import mysql.connector
from mysql.connector import Error

def check_and_fix_users_table():
    """Vérifie et corrige la structure de la table users"""
    print("🔧 Vérification de la table users")
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
            
            # Vérifier si la table users existe
            cursor.execute("SHOW TABLES LIKE 'users'")
            if not cursor.fetchone():
                print("❌ Table 'users' n'existe pas!")
                return False
            
            print("✅ Table 'users' trouvée")
            
            # Vérifier la structure de la table
            cursor.execute("DESCRIBE users")
            columns = cursor.fetchall()
            
            print("📋 Structure actuelle de la table users:")
            for column in columns:
                print(f"   - {column[0]} ({column[1]})")
            
            # Vérifier si password_hash existe
            has_password_hash = any('password_hash' in column[0] for column in columns)
            
            if not has_password_hash:
                print("\n🔧 Ajout du champ password_hash...")
                
                # Ajouter le champ password_hash
                cursor.execute("""
                    ALTER TABLE users 
                    ADD COLUMN password_hash VARCHAR(255) NOT NULL DEFAULT ''
                """)
                
                connection.commit()
                print("✅ Champ password_hash ajouté")
                
                # Vérifier la nouvelle structure
                cursor.execute("DESCRIBE users")
                columns = cursor.fetchall()
                
                print("\n📋 Nouvelle structure de la table users:")
                for column in columns:
                    print(f"   - {column[0]} ({column[1]})")
            else:
                print("✅ Champ password_hash existe déjà")
            
            # Créer un utilisateur de test
            print("\n👤 Création d'un utilisateur de test...")
            
            import bcrypt
            
            test_email = "admin@eazyskool.fr"
            test_password = "admin123"
            test_first_name = "Admin"
            test_last_name = "EazySkool"
            test_city = "Strasbourg"
            
            # Hasher le mot de passe
            password_hash = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Vérifier si l'utilisateur existe déjà
            cursor.execute("SELECT id FROM users WHERE email = %s", (test_email,))
            if not cursor.fetchone():
                # Insérer l'utilisateur de test
                cursor.execute("""
                    INSERT INTO users (email, password_hash, first_name, last_name, city) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (test_email, password_hash, test_first_name, test_last_name, test_city))
                
                connection.commit()
                print("✅ Utilisateur admin créé avec succès!")
                print(f"   Email: {test_email}")
                print(f"   Mot de passe: {test_password}")
                print(f"   Nom: {test_first_name} {test_last_name}")
            else:
                print("✅ Utilisateur admin existe déjà")
            
            # Afficher tous les utilisateurs
            print("\n📋 Liste des utilisateurs:")
            cursor.execute("SELECT id, email, first_name, last_name, city, created_at FROM users")
            users = cursor.fetchall()
            
            for user in users:
                print(f"   ID: {user[0]}, Email: {user[1]}, Nom: {user[2]} {user[3]}, Ville: {user[4]}")
            
            cursor.close()
            connection.close()
            
            print("\n🎉 Table users corrigée avec succès!")
            return True
            
    except Error as e:
        print(f"❌ Erreur MySQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def create_auth_interface():
    """Crée une interface simple pour tester l'authentification"""
    print("\n🔧 Création d'une interface d'authentification...")
    
    html_code = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EazySkool - Authentification</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        input[type="email"], input[type="password"], input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background-color: #007bff;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            margin-top: 10px;
        }
        button:hover {
            background-color: #0056b3;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            border-radius: 5px;
        }
        .success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .tabs {
            display: flex;
            margin-bottom: 20px;
        }
        .tab {
            flex: 1;
            padding: 10px;
            text-align: center;
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            cursor: pointer;
        }
        .tab.active {
            background-color: #007bff;
            color: white;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 EazySkool - Authentification</h1>
        
        <div class="tabs">
            <div class="tab active" onclick="showTab('login')">Connexion</div>
            <div class="tab" onclick="showTab('register')">Inscription</div>
        </div>
        
        <!-- Formulaire de connexion -->
        <div id="login" class="tab-content active">
            <h2>Connexion</h2>
            <form id="loginForm">
                <div class="form-group">
                    <label for="loginEmail">Email:</label>
                    <input type="email" id="loginEmail" required>
                </div>
                <div class="form-group">
                    <label for="loginPassword">Mot de passe:</label>
                    <input type="password" id="loginPassword" required>
                </div>
                <button type="submit">Se connecter</button>
            </form>
        </div>
        
        <!-- Formulaire d'inscription -->
        <div id="register" class="tab-content">
            <h2>Inscription</h2>
            <form id="registerForm">
                <div class="form-group">
                    <label for="registerEmail">Email:</label>
                    <input type="email" id="registerEmail" required>
                </div>
                <div class="form-group">
                    <label for="registerPassword">Mot de passe:</label>
                    <input type="password" id="registerPassword" required>
                </div>
                <div class="form-group">
                    <label for="firstName">Prénom:</label>
                    <input type="text" id="firstName">
                </div>
                <div class="form-group">
                    <label for="lastName">Nom:</label>
                    <input type="text" id="lastName">
                </div>
                <div class="form-group">
                    <label for="city">Ville:</label>
                    <input type="text" id="city">
                </div>
                <button type="submit">S'inscrire</button>
            </form>
        </div>
        
        <div id="result"></div>
    </div>

    <script>
        function showTab(tabName) {
            // Masquer tous les contenus
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            // Désactiver tous les onglets
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Afficher le contenu sélectionné
            document.getElementById(tabName).classList.add('active');
            
            // Activer l'onglet sélectionné
            event.target.classList.add('active');
        }
        
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            
            try {
                const response = await fetch('http://localhost:5001/api/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showResult('Connexion réussie! Bienvenue ' + data.user.first_name + ' ' + data.user.last_name, 'success');
                } else {
                    showResult('Erreur: ' + data.error, 'error');
                }
            } catch (error) {
                showResult('Erreur de connexion: ' + error.message, 'error');
            }
        });
        
        document.getElementById('registerForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = document.getElementById('registerEmail').value;
            const password = document.getElementById('registerPassword').value;
            const firstName = document.getElementById('firstName').value;
            const lastName = document.getElementById('lastName').value;
            const city = document.getElementById('city').value;
            
            try {
                const response = await fetch('http://localhost:5001/api/auth/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        email, 
                        password, 
                        first_name: firstName, 
                        last_name: lastName, 
                        city 
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showResult('Inscription réussie! Votre compte a été créé.', 'success');
                } else {
                    showResult('Erreur: ' + data.error, 'error');
                }
            } catch (error) {
                showResult('Erreur d\'inscription: ' + error.message, 'error');
            }
        });
        
        function showResult(message, type) {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = message;
            resultDiv.className = 'result ' + type;
        }
    </script>
</body>
</html>
'''
    
    with open('auth_interface.html', 'w', encoding='utf-8') as f:
        f.write(html_code)
    
    print("✅ Interface d'authentification créée: auth_interface.html")

if __name__ == "__main__":
    print("🎓 EazySkool - Correction de la table users")
    print("=" * 50)
    
    if check_and_fix_users_table():
        create_auth_interface()
        
        print("\n📋 Prochaines étapes:")
        print("1. Démarrer l'API d'auth: python auth_api.py")
        print("2. Ouvrir l'interface: auth_interface.html")
        print("3. Tester avec l'utilisateur admin:")
        print("   Email: admin@eazyskool.fr")
        print("   Mot de passe: admin123")
    else:
        print("\n❌ Échec de la correction")
        print("💡 Vérifiez que la base de données est créée") 