import mysql.connector
from mysql.connector import Error
import bcrypt
from typing import List, Dict, Optional, Any
import json
from datetime import datetime
import os

class EazySkoolMySQLDB:
    def __init__(self, host='localhost', user='root', password='', database='eazyskool', port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None
        
    def connect(self):
        """Établit la connexion à la base de données MySQL"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
            return True
        except Error as e:
            print(f"Erreur de connexion MySQL: {e}")
            return False
    
    def disconnect(self):
        """Ferme la connexion à la base de données"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query: str, params: tuple = None, fetch: bool = True):
        """Exécute une requête SQL"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return None
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
            else:
                self.connection.commit()
                result = cursor.rowcount
            
            cursor.close()
            return result
        except Error as e:
            print(f"Erreur d'exécution de requête: {e}")
            return None
    
    def get_all_schools(self) -> List[Dict]:
        """Récupère toutes les écoles avec leurs informations complètes"""
        query = """
        SELECT 
            s.*,
            c.name as city_name,
            st.name as school_type_name,
            GROUP_CONCAT(DISTINCT sp.name) as specializations
        FROM schools s
        LEFT JOIN cities c ON s.city_id = c.id
        LEFT JOIN school_types st ON s.school_type_id = st.id
        LEFT JOIN school_specializations ss ON s.id = ss.school_id
        LEFT JOIN specializations sp ON ss.specialization_id = sp.id
        GROUP BY s.id
        """
        
        schools = self.execute_query(query)
        if schools:
            # Convertir les objets datetime en chaînes pour JSON
            for school in schools:
                if 'created_at' in school and school['created_at']:
                    school['created_at'] = school['created_at'].isoformat()
                if 'updated_at' in school and school['updated_at']:
                    school['updated_at'] = school['updated_at'].isoformat()
        
        return schools or []
    
    def get_school_by_id(self, school_id: int) -> Optional[Dict]:
        """Récupère une école par son ID"""
        query = """
        SELECT 
            s.*,
            c.name as city_name,
            st.name as school_type_name,
            GROUP_CONCAT(DISTINCT sp.name) as specializations
        FROM schools s
        LEFT JOIN cities c ON s.city_id = c.id
        LEFT JOIN school_types st ON s.school_type_id = st.id
        LEFT JOIN school_specializations ss ON s.id = ss.school_id
        LEFT JOIN specializations sp ON ss.specialization_id = sp.id
        WHERE s.id = %s
        GROUP BY s.id
        """
        
        result = self.execute_query(query, (school_id,))
        if result:
            school = result[0]
            if 'created_at' in school and school['created_at']:
                school['created_at'] = school['created_at'].isoformat()
            if 'updated_at' in school and school['updated_at']:
                school['updated_at'] = school['updated_at'].isoformat()
            return school
        return None
    
    def search_schools(self, query: str) -> List[Dict]:
        """Recherche des écoles par nom ou description"""
        search_query = """
        SELECT 
            s.*,
            c.name as city_name,
            st.name as school_type_name,
            GROUP_CONCAT(DISTINCT sp.name) as specializations
        FROM schools s
        LEFT JOIN cities c ON s.city_id = c.id
        LEFT JOIN school_types st ON s.school_type_id = st.id
        LEFT JOIN school_specializations ss ON s.id = ss.school_id
        LEFT JOIN specializations sp ON ss.specialization_id = sp.id
        WHERE s.name LIKE %s OR s.description LIKE %s OR c.name LIKE %s
        GROUP BY s.id
        """
        
        search_term = f"%{query}%"
        schools = self.execute_query(search_query, (search_term, search_term, search_term))
        
        if schools:
            for school in schools:
                if 'created_at' in school and school['created_at']:
                    school['created_at'] = school['created_at'].isoformat()
                if 'updated_at' in school and school['updated_at']:
                    school['updated_at'] = school['updated_at'].isoformat()
        
        return schools or []
    
    def get_cities(self) -> List[Dict]:
        """Récupère toutes les villes"""
        query = "SELECT * FROM cities ORDER BY name"
        return self.execute_query(query) or []
    
    def get_school_types(self) -> List[Dict]:
        """Récupère tous les types d'écoles"""
        query = "SELECT * FROM school_types ORDER BY name"
        return self.execute_query(query) or []
    
    def get_school_images(self, school_id: int) -> List[Dict]:
        """Récupère les images d'une école"""
        query = "SELECT * FROM school_images WHERE school_id = %s ORDER BY is_primary DESC"
        images = self.execute_query(query, (school_id,))
        
        if images:
            for image in images:
                if 'created_at' in image and image['created_at']:
                    image['created_at'] = image['created_at'].isoformat()
        
        return images or []
    
    def get_school_reviews(self, school_id: int) -> List[Dict]:
        """Récupère les avis d'une école"""
        query = """
        SELECT r.*, u.first_name, u.last_name
        FROM reviews r
        JOIN users u ON r.user_id = u.id
        WHERE r.school_id = %s
        ORDER BY r.created_at DESC
        """
        
        reviews = self.execute_query(query, (school_id,))
        
        if reviews:
            for review in reviews:
                if 'created_at' in review and review['created_at']:
                    review['created_at'] = review['created_at'].isoformat()
        
        return reviews or []
    
    def add_review(self, school_id: int, user_id: int, rating: int, comment: str) -> bool:
        """Ajoute un avis"""
        query = "INSERT INTO reviews (school_id, user_id, rating, comment) VALUES (%s, %s, %s, %s)"
        result = self.execute_query(query, (school_id, user_id, rating, comment), fetch=False)
        return result is not None and result > 0
    
    def create_user(self, email: str, password: str, first_name: str = None, last_name: str = None, city: str = None) -> Optional[int]:
        """Crée un nouvel utilisateur"""
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        query = "INSERT INTO users (email, password_hash, first_name, last_name, city) VALUES (%s, %s, %s, %s, %s)"
        result = self.execute_query(query, (email, password_hash, first_name, last_name, city), fetch=False)
        
        if result and result > 0:
            # Récupérer l'ID de l'utilisateur créé
            user_id = self.execute_query("SELECT LAST_INSERT_ID() as id")
            return user_id[0]['id'] if user_id else None
        return None
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authentifie un utilisateur"""
        query = "SELECT * FROM users WHERE email = %s"
        user = self.execute_query(query, (email,))
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user[0]['password_hash'].encode('utf-8')):
            user_data = user[0].copy()
            # Ne pas renvoyer le hash du mot de passe
            user_data.pop('password_hash', None)
            if 'created_at' in user_data and user_data['created_at']:
                user_data['created_at'] = user_data['created_at'].isoformat()
            if 'updated_at' in user_data and user_data['updated_at']:
                user_data['updated_at'] = user_data['updated_at'].isoformat()
            return user_data
        return None
    
    def get_user_favorites(self, user_id: int) -> List[Dict]:
        """Récupère les favoris d'un utilisateur"""
        query = """
        SELECT f.*, s.name as school_name, s.description, s.rating
        FROM favorites f
        JOIN schools s ON f.school_id = s.id
        WHERE f.user_id = %s
        ORDER BY f.created_at DESC
        """
        
        favorites = self.execute_query(query, (user_id,))
        
        if favorites:
            for favorite in favorites:
                if 'created_at' in favorite and favorite['created_at']:
                    favorite['created_at'] = favorite['created_at'].isoformat()
        
        return favorites or []
    
    def add_favorite(self, user_id: int, school_id: int) -> bool:
        """Ajoute un favori"""
        query = "INSERT IGNORE INTO favorites (user_id, school_id) VALUES (%s, %s)"
        result = self.execute_query(query, (user_id, school_id), fetch=False)
        return result is not None and result > 0
    
    def remove_favorite(self, user_id: int, school_id: int) -> bool:
        """Supprime un favori"""
        query = "DELETE FROM favorites WHERE user_id = %s AND school_id = %s"
        result = self.execute_query(query, (user_id, school_id), fetch=False)
        return result is not None and result > 0
    
    def get_events(self) -> List[Dict]:
        """Récupère tous les événements"""
        query = """
        SELECT e.*, s.name as school_name
        FROM events e
        LEFT JOIN schools s ON e.school_id = s.id
        ORDER BY e.event_date ASC, e.event_time ASC
        """
        
        events = self.execute_query(query)
        
        if events:
            for event in events:
                if 'created_at' in event and event['created_at']:
                    event['created_at'] = event['created_at'].isoformat()
                if 'event_date' in event and event['event_date']:
                    event['event_date'] = event['event_date'].isoformat()
                if 'event_time' in event and event['event_time']:
                    event['event_time'] = str(event['event_time'])
        
        return events or []
    
    def export_to_json(self, filename: str = 'eazyskool_export.json'):
        """Exporte toutes les données en JSON"""
        data = {
            'schools': self.get_all_schools(),
            'cities': self.get_cities(),
            'school_types': self.get_school_types(),
            'events': self.get_events()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Export terminé: {filename}")
    
    def test_connection(self) -> bool:
        """Teste la connexion à la base de données"""
        try:
            if self.connect():
                print("✅ Connexion MySQL réussie!")
                self.disconnect()
                return True
            else:
                print("❌ Échec de la connexion MySQL")
                return False
        except Exception as e:
            print(f"❌ Erreur de test: {e}")
            return False

# Fonction de test
def test_mysql_connection():
    """Teste la connexion MySQL avec les paramètres par défaut"""
    db = EazySkoolMySQLDB()
    return db.test_connection()

if __name__ == "__main__":
    print("Test de connexion MySQL...")
    if test_mysql_connection():
        print("La base de données MySQL est prête!")
    else:
        print("Vérifiez que MySQL est démarré et que la base 'eazyskool' existe.") 