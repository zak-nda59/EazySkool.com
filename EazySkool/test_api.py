#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'API EazySkool
Script pour tester les endpoints de l'API
"""

import requests
import json
import time

# URL de base de l'API
BASE_URL = "http://localhost:5000"

def test_api():
    """Teste les différents endpoints de l'API"""
    
    print("=== Test de l'API EazySkool ===\n")
    
    # Test 1: Page d'accueil
    print("1. Test de la page d'accueil...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Page d'accueil accessible")
            data = response.json()
            print(f"   Version: {data.get('version')}")
            print(f"   Endpoints disponibles: {len(data.get('endpoints', []))}")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    print()
    
    # Test 2: Récupération des écoles
    print("2. Test de récupération des écoles...")
    try:
        response = requests.get(f"{BASE_URL}/api/schools")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                schools = data.get('data', [])
                print(f"✅ {len(schools)} écoles récupérées")
                for school in schools[:3]:  # Affiche les 3 premières
                    print(f"   - {school['name']} ({school['city_name']})")
            else:
                print(f"❌ Erreur API: {data.get('error')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print()
    
    # Test 3: Recherche d'écoles
    print("3. Test de recherche d'écoles...")
    try:
        response = requests.get(f"{BASE_URL}/api/schools/search?q=Strasbourg")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                schools = data.get('data', [])
                print(f"✅ {len(schools)} écoles trouvées pour 'Strasbourg'")
                for school in schools:
                    print(f"   - {school['name']} ({school['city_name']})")
            else:
                print(f"❌ Erreur API: {data.get('error')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print()
    
    # Test 4: Récupération des villes
    print("4. Test de récupération des villes...")
    try:
        response = requests.get(f"{BASE_URL}/api/cities")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                cities = data.get('data', [])
                print(f"✅ {len(cities)} villes récupérées")
                for city in cities:
                    print(f"   - {city['name']} ({city['region']})")
            else:
                print(f"❌ Erreur API: {data.get('error')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print()
    
    # Test 5: Récupération des types d'écoles
    print("5. Test de récupération des types d'écoles...")
    try:
        response = requests.get(f"{BASE_URL}/api/types")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                types = data.get('data', [])
                print(f"✅ {len(types)} types d'écoles récupérés")
                for type_school in types:
                    print(f"   - {type_school['name']}")
            else:
                print(f"❌ Erreur API: {data.get('error')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print()
    
    # Test 6: Récupération des événements
    print("6. Test de récupération des événements...")
    try:
        response = requests.get(f"{BASE_URL}/api/events")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                events = data.get('data', [])
                print(f"✅ {len(events)} événements récupérés")
                for event in events:
                    print(f"   - {event['title']} ({event['event_date']})")
            else:
                print(f"❌ Erreur API: {data.get('error')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print()
    
    # Test 7: Création d'un compte utilisateur
    print("7. Test de création de compte...")
    try:
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
            "city": "Strasbourg"
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Compte créé avec succès")
                user_id = data.get('user_id')
                print(f"   ID utilisateur: {user_id}")
            else:
                print(f"❌ Erreur API: {data.get('error')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print()
    
    # Test 8: Connexion utilisateur
    print("8. Test de connexion...")
    try:
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                user = data.get('data', {})
                print("✅ Connexion réussie")
                print(f"   Utilisateur: {user.get('first_name')} {user.get('last_name')}")
                print(f"   Email: {user.get('email')}")
            else:
                print(f"❌ Erreur API: {data.get('error')}")
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print()
    print("=== Tests terminés ===")

if __name__ == "__main__":
    # Attendre un peu que le serveur démarre
    print("Attente du démarrage du serveur...")
    time.sleep(2)
    test_api() 