#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EazySkool API Server
Serveur API simple pour connecter la base de données à l'application frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from database_manager import EazySkoolDB
import json

app = Flask(__name__)
CORS(app)  # Permet les requêtes cross-origin

# Initialise la base de données
db = EazySkoolDB()

@app.route('/')
def home():
    """Page d'accueil de l'API"""
    return jsonify({
        'message': 'EazySkool API',
        'version': '1.0.0',
        'endpoints': [
            '/api/schools',
            '/api/schools/<id>',
            '/api/schools/search',
            '/api/cities',
            '/api/types',
            '/api/events',
            '/api/auth/login',
            '/api/auth/register',
            '/api/favorites',
            '/api/reviews'
        ]
    })

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
    """Récupère une école par son ID"""
    try:
        school = db.get_school_by_id(school_id)
        if school:
            # Récupère aussi les images et avis
            images = db.get_school_images(school_id)
            reviews = db.get_school_reviews(school_id)
            
            school['images'] = images
            school['reviews'] = reviews
            
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
    try:
        query = request.args.get('q', '')
        city = request.args.get('city', '')
        school_type = request.args.get('type', '')
        
        schools = db.search_schools(query, city, school_type)
        
        return jsonify({
            'success': True,
            'data': schools,
            'count': len(schools),
            'filters': {
                'query': query,
                'city': city,
                'type': school_type
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

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

@app.route('/api/types', methods=['GET'])
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

@app.route('/api/events', methods=['GET'])
def get_events():
    """Récupère les événements à venir"""
    try:
        limit = request.args.get('limit', 10, type=int)
        events = db.get_events(limit)
        return jsonify({
            'success': True,
            'data': events
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authentification d'un utilisateur"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email et mot de passe requis'
            }), 400
        
        user = db.authenticate_user(email, password)
        if user:
            return jsonify({
                'success': True,
                'data': user
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

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Création d'un nouveau compte"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        city = data.get('city', '')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'error': 'Email et mot de passe requis'
            }), 400
        
        user_id = db.create_user(email, password, first_name, last_name, city)
        if user_id:
            return jsonify({
                'success': True,
                'message': 'Compte créé avec succès',
                'user_id': user_id
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Impossible de créer le compte'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/favorites', methods=['GET', 'POST', 'DELETE'])
def manage_favorites():
    """Gestion des favoris"""
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        school_id = data.get('school_id')
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'ID utilisateur requis'
            }), 400
        
        if request.method == 'GET':
            # Récupère les favoris d'un utilisateur
            favorites = db.get_user_favorites(user_id)
            return jsonify({
                'success': True,
                'data': favorites
            })
        
        elif request.method == 'POST':
            # Ajoute un favori
            if not school_id:
                return jsonify({
                    'success': False,
                    'error': 'ID école requis'
                }), 400
            
            success = db.add_favorite(user_id, school_id)
            if success:
                return jsonify({
                    'success': True,
                    'message': 'École ajoutée aux favoris'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Impossible d\'ajouter aux favoris'
                }), 400
        
        elif request.method == 'DELETE':
            # Supprime un favori
            if not school_id:
                return jsonify({
                    'success': False,
                    'error': 'ID école requis'
                }), 400
            
            success = db.remove_favorite(user_id, school_id)
            if success:
                return jsonify({
                    'success': True,
                    'message': 'École retirée des favoris'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Impossible de retirer des favoris'
                }), 400
                
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
        school_id = data.get('school_id')
        user_id = data.get('user_id')
        rating = data.get('rating')
        comment = data.get('comment', '')
        
        if not all([school_id, user_id, rating]):
            return jsonify({
                'success': False,
                'error': 'ID école, ID utilisateur et note requis'
            }), 400
        
        if not 1 <= rating <= 5:
            return jsonify({
                'success': False,
                'error': 'La note doit être entre 1 et 5'
            }), 400
        
        success = db.add_review(school_id, user_id, rating, comment)
        if success:
            return jsonify({
                'success': True,
                'message': 'Avis ajouté avec succès'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Impossible d\'ajouter l\'avis'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export', methods=['GET'])
def export_data():
    """Exporte toutes les données en JSON"""
    try:
        db.export_to_json('export_data.json')
        return jsonify({
            'success': True,
            'message': 'Données exportées vers export_data.json'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("Démarrage du serveur API EazySkool...")
    print("API disponible sur: http://localhost:5000")
    print("Documentation: http://localhost:5000/")
    app.run(debug=True, host='0.0.0.0', port=5000) 