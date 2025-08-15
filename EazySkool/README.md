# 🎓 EazySkool - Plateforme de Recherche d'Écoles

Une plateforme moderne pour découvrir, comparer et noter les écoles du Grand Est, avec une base de données complète et une API REST.

## 📋 Table des matières

- [🚀 Démarrage rapide](#-démarrage-rapide)
- [🗄️ Base de données](#️-base-de-données)
- [🔧 Architecture](#-architecture)
- [📁 Structure du projet](#-structure-du-projet)
- [🔌 API REST](#-api-rest)
- [🎨 Interface utilisateur](#-interface-utilisateur)
- [🛠️ Outils de développement](#️-outils-de-développement)
- [📊 Fonctionnalités](#-fonctionnalités)
- [🔒 Sécurité](#-sécurité)
- [📈 Évolutions futures](#-évolutions-futures)

## 🚀 Démarrage rapide

### Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)

### Installation

1. **Clonez le projet** (si applicable)
2. **Installez les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancez l'application** :
   ```bash
   python start.py
   ```

4. **Accédez à l'application** :
   - API : http://localhost:5000
   - Interface : Ouvrez `index.html` dans votre navigateur

## 🗄️ Base de données

### Structure

La base de données SQLite contient les tables suivantes :

- **`users`** - Gestion des utilisateurs et authentification
- **`schools`** - Informations des écoles
- **`school_types`** - Types d'écoles (Université, École de commerce, etc.)
- **`cities`** - Villes du Grand Est
- **`reviews`** - Avis des utilisateurs
- **`favorites`** - Écoles favorites des utilisateurs
- **`events`** - Événements (portes ouvertes, salons)
- **`specializations`** - Spécialités/formations
- **`school_images`** - Images des écoles
- **`school_specializations`** - Liaison écoles-spécialités

### Données incluses

- **8 écoles** du Grand Est
- **6 villes** principales
- **6 types d'écoles**
- **8 spécialités** différentes
- **4 événements** à venir

### Gestion de la base de données

```bash
# Créer/réinitialiser la base de données
python database_manager.py

# Exporter les données en JSON
curl http://localhost:5000/api/export
```

## 🔧 Architecture

```
EazySkool/
├── Frontend (HTML/CSS/JS)
│   ├── index.html          # Interface principale
│   ├── style.css           # Styles CSS
│   ├── script.js           # Version statique
│   └── script_with_api.js  # Version avec API
├── Backend (Python/Flask)
│   ├── api_server.py       # Serveur API Flask
│   ├── database_manager.py # Gestionnaire de DB
│   └── config.py           # Configuration
├── Base de données
│   ├── database.sql        # Script de création
│   └── eazyskool.db       # Base SQLite
└── Outils
    ├── start.py            # Script de démarrage
    ├── test_api.py         # Tests de l'API
    └── requirements.txt    # Dépendances Python
```

## 📁 Structure du projet

```
EazySkool/
├── 📄 index.html                 # Interface utilisateur
├── 🎨 style.css                  # Styles CSS
├── ⚡ script.js                  # JavaScript (version statique)
├── 🔌 script_with_api.js         # JavaScript (version API)
├── 🗄️ database.sql              # Structure de la base de données
├── 🐍 database_manager.py        # Gestionnaire de base de données
├── 🚀 api_server.py              # Serveur API Flask
├── ⚙️ config.py                  # Configuration
├── 🎯 start.py                   # Script de démarrage
├── 🧪 test_api.py                # Tests de l'API
├── 📋 requirements.txt            # Dépendances Python
├── 📖 README.md                  # Documentation principale
├── 📚 README_DATABASE.md         # Documentation de la DB
├── 🗃️ eazyskool.db              # Base de données SQLite
├── 📊 schools_data.json          # Export des données
└── 🖼️ images/                    # Images des écoles
    ├── strasbourg.jpg
    ├── icn_campus.jpg
    ├── sciencespo_batiment.jpg
    └── ...
```

## 🔌 API REST

### Endpoints principaux

#### Écoles
- `GET /api/schools` - Liste toutes les écoles
- `GET /api/schools/<id>` - Détails d'une école
- `GET /api/schools/search?q=query&city=ville&type=type` - Recherche

#### Authentification
- `POST /api/auth/login` - Connexion utilisateur
- `POST /api/auth/register` - Création de compte

#### Favoris
- `GET /api/favorites` - Récupère les favoris
- `POST /api/favorites` - Ajoute un favori
- `DELETE /api/favorites` - Supprime un favori

#### Avis
- `POST /api/reviews` - Ajoute un avis

#### Données de référence
- `GET /api/cities` - Liste des villes
- `GET /api/types` - Types d'écoles
- `GET /api/events` - Événements à venir

### Exemples d'utilisation

```bash
# Récupérer toutes les écoles
curl http://localhost:5000/api/schools

# Rechercher des écoles
curl "http://localhost:5000/api/schools/search?q=Strasbourg"

# Créer un compte
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

## 🎨 Interface utilisateur

### Fonctionnalités

- **Recherche d'écoles** avec filtres avancés
- **Système de favoris** pour les utilisateurs connectés
- **Avis et notes** sur les écoles
- **Carte interactive** des écoles
- **Conseiller IA** pour l'orientation
- **Interface responsive** et moderne

### Sections principales

1. **Accueil** - Présentation de la plateforme
2. **Recherche d'écoles** - Liste et filtres
3. **IA Conseiller** - Assistant d'orientation
4. **Favoris** - Écoles sauvegardées
5. **Compte** - Gestion du profil utilisateur

## 🛠️ Outils de développement

### Scripts disponibles

```bash
# Démarrage complet de l'application
python start.py

# Tests de l'API
python test_api.py

# Gestion de la base de données
python database_manager.py

# Configuration
python config.py
```

### Tests

```bash
# Test de l'API
python test_api.py

# Test de la base de données
python database_manager.py
```

## 📊 Fonctionnalités

### ✅ Implémentées

- [x] Base de données SQLite complète
- [x] API REST avec Flask
- [x] Authentification utilisateur
- [x] Système de favoris
- [x] Avis et notes
- [x] Recherche et filtres
- [x] Interface utilisateur moderne
- [x] Carte interactive
- [x] Export des données
- [x] Tests automatisés

### 🔄 En cours

- [ ] Système de notifications
- [ ] Statistiques avancées
- [ ] Modération des avis
- [ ] API pour applications mobiles

## 🔒 Sécurité

- **Mots de passe hashés** avec bcrypt
- **Validation des données** côté serveur
- **Protection contre les injections SQL**
- **CORS configuré** pour les requêtes cross-origin
- **Gestion des erreurs** robuste

## 📈 Évolutions futures

### Court terme
- [ ] Ajout de nouvelles écoles
- [ ] Système de notifications
- [ ] Amélioration de l'IA conseiller

### Moyen terme
- [ ] Application mobile
- [ ] Système de modération
- [ ] Statistiques avancées

### Long terme
- [ ] Extension à d'autres régions
- [ ] Intégration avec les établissements
- [ ] Système de recommandations

## 🤝 Contribution

1. Fork le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

- **Email** : contact@eazyskool.com
- **Documentation** : http://localhost:5000/ (quand le serveur est démarré)
- **Issues** : Utilisez les issues GitHub pour signaler des bugs

---

**🎓 EazySkool** - Trouvez l'école de vos rêves dans le Grand Est ! 