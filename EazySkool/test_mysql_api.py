import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_api():
    """Test complet de l'API MySQL"""
    print("🧪 Test de l'API EazySkool MySQL")
    print("=" * 50)
    
    # 1. Test de la page d'accueil
    print("1. Test de la page d'accueil...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Page d'accueil accessible")
            data = response.json()
            print(f"   Version: {data.get('version')}")
            print(f"   Database: {data.get('database')}")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    # 2. Test de connexion MySQL
    print("\n2. Test de connexion MySQL...")
    try:
        response = requests.get(f"{BASE_URL}/api/test-connection")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Connexion MySQL réussie")
            else:
                print(f"❌ Échec MySQL: {data.get('error')}")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 3. Test récupération des écoles
    print("\n3. Test récupération des écoles...")
    try:
        response = requests.get(f"{BASE_URL}/api/schools")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                schools = data.get('data', [])
                print(f"✅ {len(schools)} écoles récupérées")
                if schools:
                    print(f"   Première école: {schools[0].get('name')}")
            else:
                print(f"❌ Erreur: {data.get('error')}")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 4. Test recherche d'écoles
    print("\n4. Test recherche d'écoles...")
    try:
        response = requests.get(f"{BASE_URL}/api/schools/search?q=Strasbourg")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                schools = data.get('data', [])
                print(f"✅ {len(schools)} écoles trouvées pour 'Strasbourg'")
            else:
                print(f"❌ Erreur: {data.get('error')}")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 5. Test récupération des villes
    print("\n5. Test récupération des villes...")
    try:
        response = requests.get(f"{BASE_URL}/api/cities")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                cities = data.get('data', [])
                print(f"✅ {len(cities)} villes récupérées")
                if cities:
                    print(f"   Première ville: {cities[0].get('name')}")
            else:
                print(f"❌ Erreur: {data.get('error')}")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 6. Test récupération des types d'écoles
    print("\n6. Test récupération des types d'écoles...")
    try:
        response = requests.get(f"{BASE_URL}/api/school-types")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                types = data.get('data', [])
                print(f"✅ {len(types)} types d'écoles récupérés")
                if types:
                    print(f"   Premier type: {types[0].get('name')}")
            else:
                print(f"❌ Erreur: {data.get('error')}")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 7. Test récupération des événements
    print("\n7. Test récupération des événements...")
    try:
        response = requests.get(f"{BASE_URL}/api/events")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                events = data.get('data', [])
                print(f"✅ {len(events)} événements récupérés")
                if events:
                    print(f"   Premier événement: {events[0].get('title')}")
            else:
                print(f"❌ Erreur: {data.get('error')}")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 8. Test inscription utilisateur
    print("\n8. Test inscription utilisateur...")
    try:
        user_data = {
            "email": "test@example.com",
            "password": "test123",
            "first_name": "Test",
            "last_name": "User",
            "city": "Strasbourg"
        }
        response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Utilisateur créé avec succès")
                user_id = data.get('user_id')
            else:
                print(f"❌ Erreur: {data.get('error')}")
                user_id = None
        else:
            print(f"❌ Erreur: {response.status_code}")
            user_id = None
    except Exception as e:
        print(f"❌ Erreur: {e}")
        user_id = None
    
    # 9. Test connexion utilisateur
    print("\n9. Test connexion utilisateur...")
    try:
        login_data = {
            "email": "test@example.com",
            "password": "test123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Connexion réussie")
                user = data.get('user', {})
                print(f"   Utilisateur: {user.get('first_name')} {user.get('last_name')}")
            else:
                print(f"❌ Erreur: {data.get('error')}")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Tests terminés!")
    print("📊 Base de données: MySQL")
    print("🌐 API: http://localhost:5000")
    print("📚 Documentation: Voir GUIDE_MYSQL.md")

if __name__ == "__main__":
    test_api() 