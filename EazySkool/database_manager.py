#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EazySkool Database Manager
Gestionnaire de base de données pour la plateforme EazySkool
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import hashlib
import bcrypt

class EazySkoolDB:
    def __init__(self, db_path: str = "eazyskool.db"):
        """Initialise la connexion à la base de données"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialise la base de données si elle n'existe pas"""
        if not os.path.exists(self.db_path):
            print("Création de la base de données...")
            self.create_database()
        else:
            print("Base de données existante trouvée.")
    
    def create_database(self):
        """Crée la base de données et insère les données initiales"""
        with open('database.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Exécute le script SQL
        cursor.executescript(sql_script)
        
        conn.commit()
        conn.close()
        print("Base de données créée avec succès !")
    
    def get_connection(self):
        """Retourne une connexion à la base de données"""
        return sqlite3.connect(self.db_path)
    
    def get_all_schools(self) -> List[Dict]:
        """Récupère toutes les écoles avec leurs informations complètes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            s.id,
            s.name,
            s.description,
            s.website,
            s.email,
            s.phone,
            s.address,
            s.latitude,
            s.longitude,
            s.average_rating,
            s.total_reviews,
            st.name as type_name,
            c.name as city_name,
            c.region,
            GROUP_CONCAT(DISTINCT sp.name) as specializations
        FROM schools s
        JOIN school_types st ON s.type_id = st.id
        JOIN cities c ON s.city_id = c.id
        LEFT JOIN school_specializations ss ON s.id = ss.school_id
        LEFT JOIN specializations sp ON ss.specialization_id = sp.id
        GROUP BY s.id
        ORDER BY s.average_rating DESC
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        schools = []
        for row in rows:
            school = {
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'website': row[3],
                'email': row[4],
                'phone': row[5],
                'address': row[6],
                'latitude': row[7],
                'longitude': row[8],
                'average_rating': row[9],
                'total_reviews': row[10],
                'type_name': row[11],
                'city_name': row[12],
                'region': row[13],
                'specializations': row[14].split(',') if row[14] else []
            }
            schools.append(school)
        
        conn.close()
        return schools
    
    def get_school_by_id(self, school_id: int) -> Optional[Dict]:
        """Récupère une école par son ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT 
            s.id,
            s.name,
            s.description,
            s.website,
            s.email,
            s.phone,
            s.address,
            s.latitude,
            s.longitude,
            s.average_rating,
            s.total_reviews,
            st.name as type_name,
            c.name as city_name,
            c.region,
            GROUP_CONCAT(DISTINCT sp.name) as specializations
        FROM schools s
        JOIN school_types st ON s.type_id = st.id
        JOIN cities c ON s.city_id = c.id
        LEFT JOIN school_specializations ss ON s.id = ss.school_id
        LEFT JOIN specializations sp ON ss.specialization_id = sp.id
        WHERE s.id = ?
        GROUP BY s.id
        """
        
        cursor.execute(query, (school_id,))
        row = cursor.fetchone()
        
        if row:
            school = {
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'website': row[3],
                'email': row[4],
                'phone': row[5],
                'address': row[6],
                'latitude': row[7],
                'longitude': row[8],
                'average_rating': row[9],
                'total_reviews': row[10],
                'type_name': row[11],
                'city_name': row[12],
                'region': row[13],
                'specializations': row[14].split(',') if row[14] else []
            }
            conn.close()
            return school
        
        conn.close()
        return None
    
    def search_schools(self, query: str, city: str = None, school_type: str = None) -> List[Dict]:
        """Recherche des écoles selon différents critères"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        sql_conditions = []
        params = []
        
        if query:
            sql_conditions.append("(s.name LIKE ? OR s.description LIKE ?)")
            params.extend([f"%{query}%", f"%{query}%"])
        
        if city:
            sql_conditions.append("c.name = ?")
            params.append(city)
        
        if school_type:
            sql_conditions.append("st.name = ?")
            params.append(school_type)
        
        where_clause = " AND ".join(sql_conditions) if sql_conditions else "1=1"
        
        query_sql = f"""
        SELECT 
            s.id,
            s.name,
            s.description,
            s.website,
            s.email,
            s.phone,
            s.address,
            s.latitude,
            s.longitude,
            s.average_rating,
            s.total_reviews,
            st.name as type_name,
            c.name as city_name,
            c.region,
            GROUP_CONCAT(DISTINCT sp.name) as specializations
        FROM schools s
        JOIN school_types st ON s.type_id = st.id
        JOIN cities c ON s.city_id = c.id
        LEFT JOIN school_specializations ss ON s.id = ss.school_id
        LEFT JOIN specializations sp ON ss.specialization_id = sp.id
        WHERE {where_clause}
        GROUP BY s.id
        ORDER BY s.average_rating DESC
        """
        
        cursor.execute(query_sql, params)
        rows = cursor.fetchall()
        
        schools = []
        for row in rows:
            school = {
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'website': row[3],
                'email': row[4],
                'phone': row[5],
                'address': row[6],
                'latitude': row[7],
                'longitude': row[8],
                'average_rating': row[9],
                'total_reviews': row[10],
                'type_name': row[11],
                'city_name': row[12],
                'region': row[13],
                'specializations': row[14].split(',') if row[14] else []
            }
            schools.append(school)
        
        conn.close()
        return schools
    
    def get_cities(self) -> List[Dict]:
        """Récupère toutes les villes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, region FROM cities ORDER BY name")
        rows = cursor.fetchall()
        
        cities = [{'id': row[0], 'name': row[1], 'region': row[2]} for row in rows]
        
        conn.close()
        return cities
    
    def get_school_types(self) -> List[Dict]:
        """Récupère tous les types d'écoles"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, description FROM school_types ORDER BY name")
        rows = cursor.fetchall()
        
        types = [{'id': row[0], 'name': row[1], 'description': row[2]} for row in rows]
        
        conn.close()
        return types
    
    def get_school_images(self, school_id: int) -> List[Dict]:
        """Récupère les images d'une école"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, image_path, is_primary 
            FROM school_images 
            WHERE school_id = ? 
            ORDER BY is_primary DESC, id
        """, (school_id,))
        
        rows = cursor.fetchall()
        images = [{'id': row[0], 'path': row[1], 'is_primary': bool(row[2])} for row in rows]
        
        conn.close()
        return images
    
    def get_school_reviews(self, school_id: int) -> List[Dict]:
        """Récupère les avis d'une école"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT r.id, r.rating, r.comment, r.created_at,
                   u.first_name, u.last_name, u.city
            FROM reviews r
            JOIN users u ON r.user_id = u.id
            WHERE r.school_id = ?
            ORDER BY r.created_at DESC
        """, (school_id,))
        
        rows = cursor.fetchall()
        reviews = []
        for row in rows:
            review = {
                'id': row[0],
                'rating': row[1],
                'comment': row[2],
                'created_at': row[3],
                'user_name': f"{row[4]} {row[5]}" if row[4] and row[5] else "Anonyme",
                'user_city': row[6]
            }
            reviews.append(review)
        
        conn.close()
        return reviews
    
    def add_review(self, school_id: int, user_id: int, rating: int, comment: str = None) -> bool:
        """Ajoute un avis pour une école"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Insère l'avis
            cursor.execute("""
                INSERT INTO reviews (school_id, user_id, rating, comment)
                VALUES (?, ?, ?, ?)
            """, (school_id, user_id, rating, comment))
            
            # Met à jour la note moyenne de l'école
            cursor.execute("""
                UPDATE schools 
                SET average_rating = (
                    SELECT AVG(rating) 
                    FROM reviews 
                    WHERE school_id = ?
                ),
                total_reviews = (
                    SELECT COUNT(*) 
                    FROM reviews 
                    WHERE school_id = ?
                )
                WHERE id = ?
            """, (school_id, school_id, school_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'avis: {e}")
            return False
    
    def create_user(self, email: str, password: str, first_name: str = None, last_name: str = None, city: str = None) -> Optional[int]:
        """Crée un nouvel utilisateur"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Hash du mot de passe
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            cursor.execute("""
                INSERT INTO users (email, password_hash, first_name, last_name, city)
                VALUES (?, ?, ?, ?, ?)
            """, (email, password_hash, first_name, last_name, city))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            print("Un utilisateur avec cet email existe déjà.")
            return None
        except Exception as e:
            print(f"Erreur lors de la création de l'utilisateur: {e}")
            return None
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authentifie un utilisateur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, email, password_hash, first_name, last_name, city
            FROM users 
            WHERE email = ?
        """, (email,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row and bcrypt.checkpw(password.encode('utf-8'), row[2].encode('utf-8')):
            return {
                'id': row[0],
                'email': row[1],
                'first_name': row[3],
                'last_name': row[4],
                'city': row[5]
            }
        
        return None
    
    def get_user_favorites(self, user_id: int) -> List[Dict]:
        """Récupère les écoles favorites d'un utilisateur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.id, s.name, s.average_rating, s.total_reviews,
                   st.name as type_name, c.name as city_name
            FROM favorites f
            JOIN schools s ON f.school_id = s.id
            JOIN school_types st ON s.type_id = st.id
            JOIN cities c ON s.city_id = c.id
            WHERE f.user_id = ?
            ORDER BY f.created_at DESC
        """, (user_id,))
        
        rows = cursor.fetchall()
        favorites = []
        for row in rows:
            favorite = {
                'id': row[0],
                'name': row[1],
                'average_rating': row[2],
                'total_reviews': row[3],
                'type_name': row[4],
                'city_name': row[5]
            }
            favorites.append(favorite)
        
        conn.close()
        return favorites
    
    def add_favorite(self, user_id: int, school_id: int) -> bool:
        """Ajoute une école aux favoris"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO favorites (user_id, school_id)
                VALUES (?, ?)
            """, (user_id, school_id))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            print("Cette école est déjà dans vos favoris.")
            return False
        except Exception as e:
            print(f"Erreur lors de l'ajout aux favoris: {e}")
            return False
    
    def remove_favorite(self, user_id: int, school_id: int) -> bool:
        """Retire une école des favoris"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM favorites 
                WHERE user_id = ? AND school_id = ?
            """, (user_id, school_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression des favoris: {e}")
            return False
    
    def get_events(self, limit: int = 10) -> List[Dict]:
        """Récupère les événements à venir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT e.id, e.title, e.description, e.event_date, e.event_time,
                   e.location, e.is_online, s.name as school_name
            FROM events e
            LEFT JOIN schools s ON e.school_id = s.id
            WHERE e.event_date >= date('now')
            ORDER BY e.event_date ASC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        events = []
        for row in rows:
            event = {
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'event_date': row[3],
                'event_time': row[4],
                'location': row[5],
                'is_online': bool(row[6]),
                'school_name': row[7]
            }
            events.append(event)
        
        conn.close()
        return events
    
    def export_to_json(self, filename: str = "schools_data.json"):
        """Exporte toutes les données en JSON"""
        data = {
            'schools': self.get_all_schools(),
            'cities': self.get_cities(),
            'school_types': self.get_school_types(),
            'events': self.get_events(20)
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Données exportées vers {filename}")

def main():
    """Fonction principale pour tester la base de données"""
    db = EazySkoolDB()
    
    print("=== Test de la base de données EazySkool ===")
    
    # Test récupération des écoles
    schools = db.get_all_schools()
    print(f"Nombre d'écoles: {len(schools)}")
    
    # Test recherche
    search_results = db.search_schools("Strasbourg")
    print(f"Écoles à Strasbourg: {len(search_results)}")
    
    # Test récupération des villes
    cities = db.get_cities()
    print(f"Villes disponibles: {len(cities)}")
    
    # Export des données
    db.export_to_json()
    
    print("Tests terminés avec succès !")

if __name__ == "__main__":
    main() 