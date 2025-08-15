from flask import Flask, request, jsonify
from flask_cors import CORS
from mysql_database_manager import EazySkoolMySQLDB
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialisation de la base de données MySQL
db = EazySkoolMySQLDB()

@app.route('/')
def home():
    """Page d'accueil de l'API"""
    return jsonify({
        'message': 'API EazySkool MySQL',
        'version': '2.0.0',
        'database': 'MySQL',
        'status': 'running'
    })

# Endpoints pour les écoles
@app.route('/api/schools', methods=['GET'])
def get_schools():
    """Récupère toutes les écoles"""
    try:
        schools = db.get_all_schools()
        return jsonify({
            'success': True,
            'data': schools,
            'count': len(schools)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/schools/<int:school_id>', methods=['GET'])
def get_school(school_id):
    """Récupère une école par ID"""
    try:
        school = db.get_school_by_id(school_id)
        if school:
            return jsonify({
                'success': True,
                'data': school
            })
        else:
            return jsonify({
                'success': False,
                'error': 'École non trouvée'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/schools/search', methods=['GET'])
def search_schools():
    """Recherche des écoles"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({
            'success': False,
            'error': 'Paramètre de recherche requis'
        }), 400
    
    try:
        schools = db.search_schools(query)
        return jsonify({
            'success': True,
            'data': schools,
            'count': len(schools),
            'query': query
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Endpoints pour les villes et types
@app.route('/api/cities', methods=['GET'])
def get_cities():
    """Récupère toutes les villes"""
    try:
        cities = db.get_cities()
        return jsonify({
            'success': True,
            'data': cities
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/school-types', methods=['GET'])
def get_school_types():
    """Récupère tous les types d'écoles"""
    try:
        types = db.get_school_types()
        return jsonify({
            'success': True,
            'data': types
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Endpoints pour les images
@app.route('/api/schools/<int:school_id>/images', methods=['GET'])
def get_school_images(school_id):
    """Récupère les images d'une école"""
    try:
        images = db.get_school_images(school_id)
        return jsonify({
            'success': True,
            'data': images
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Endpoints pour les avis
@app.route('/api/schools/<int:school_id>/reviews', methods=['GET'])
def get_school_reviews(school_id):
    """Récupère les avis d'une école"""
    try:
        reviews = db.get_school_reviews(school_id)
        return jsonify({
            'success': True,
            'data': reviews
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/reviews', methods=['POST'])
def add_review():
    """Ajoute un avis"""
    try:
        data = request.get_json()
        required_fields = ['school_id', 'user_id', 'rating', 'comment']
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Champ requis manquant: {field}'
                }), 400
        
        success = db.add_review(
            data['school_id'],
            data['user_id'],
            data['rating'],
            data['comment']
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Avis ajouté avec succès'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Erreur lors de l\'ajout de l\'avis'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Endpoints pour l'authentification
@app.route('/api/auth/register', methods=['POST'])
def register():
    """Inscription d'un nouvel utilisateur"""
    try:
        data = request.get_json()
        required_fields = ['email', 'password']
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Champ requis manquant: {field}'
                }), 400
        
        user_id = db.create_user(
            data['email'],
            data['password'],
            data.get('first_name'),
            data.get('last_name'),
            data.get('city')
        )
        
        if user_id:
            return jsonify({
                'success': True,
                'message': 'Utilisateur créé avec succès',
                'user_id': user_id
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Erreur lors de la création de l\'utilisateur'
            }), 500
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
        required_fields = ['email', 'password']
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Champ requis manquant: {field}'
                }), 400
        
        user = db.authenticate_user(data['email'], data['password'])
        
        if user:
            return jsonify({
                'success': True,
                'message': 'Connexion réussie',
                'user': user
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Email ou mot de passe incorrect'
            }), 401
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Endpoints pour les favoris
@app.route('/api/favorites/<int:user_id>', methods=['GET'])
def get_user_favorites(user_id):
    """Récupère les favoris d'un utilisateur"""
    try:
        favorites = db.get_user_favorites(user_id)
        return jsonify({
            'success': True,
            'data': favorites
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    """Ajoute un favori"""
    try:
        data = request.get_json()
        required_fields = ['user_id', 'school_id']
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Champ requis manquant: {field}'
                }), 400
        
        success = db.add_favorite(data['user_id'], data['school_id'])
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Favori ajouté avec succès'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Erreur lors de l\'ajout du favori'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/favorites', methods=['DELETE'])
def remove_favorite():
    """Supprime un favori"""
    try:
        data = request.get_json()
        required_fields = ['user_id', 'school_id']
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Champ requis manquant: {field}'
                }), 400
        
        success = db.remove_favorite(data['user_id'], data['school_id'])
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Favori supprimé avec succès'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Erreur lors de la suppression du favori'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Endpoints pour les événements
@app.route('/api/events', methods=['GET'])
def get_events():
    """Récupère tous les événements"""
    try:
        events = db.get_events()
        return jsonify({
            'success': True,
            'data': events
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Endpoint de test de connexion
@app.route('/api/test-connection', methods=['GET'])
def test_connection():
    """Teste la connexion à la base de données"""
    try:
        if db.test_connection():
            return jsonify({
                'success': True,
                'message': 'Connexion MySQL réussie'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Échec de la connexion MySQL'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Démarrage du serveur API EazySkool MySQL...")
    print("📊 Base de données: MySQL")
    print("🌐 URL: http://localhost:5000")
    print("📚 API Documentation:")
    print("   - GET  /api/schools")
    print("   - GET  /api/schools/<id>")
    print("   - GET  /api/schools/search?q=<query>")
    print("   - POST /api/auth/register")
    print("   - POST /api/auth/login")
    print("   - GET  /api/test-connection")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 