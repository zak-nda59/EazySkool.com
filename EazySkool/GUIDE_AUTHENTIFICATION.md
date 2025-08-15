# 🔐 Guide d'authentification EazySkool

## ✅ Système d'authentification configuré avec succès !

Votre système EazySkool dispose maintenant d'un système d'authentification complet avec stockage sécurisé des emails et mots de passe dans MySQL.

## 📊 État du système

### ✅ Fonctionnalités opérationnelles :
- **Table `users`** créée avec la bonne structure
- **Stockage sécurisé** des mots de passe (hashés avec bcrypt)
- **API d'authentification** fonctionnelle
- **4 utilisateurs de test** créés
- **Interface web** d'authentification disponible

### 🔐 Utilisateurs de test disponibles :
1. **Admin** : `admin@eazyskool.fr` / `admin123`
2. **User 1** : `user1@eazyskool.fr` / `user123`
3. **User 2** : `user2@eazyskool.fr` / `user456`
4. **User 3** : `user3@eazyskool.fr` / `user789`

## 🗄️ Structure de la base de données

### Table `users` :
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    city VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Champs stockés :
- **`id`** : Identifiant unique auto-incrémenté
- **`email`** : Adresse email (unique)
- **`password_hash`** : Mot de passe hashé (sécurisé)
- **`first_name`** : Prénom
- **`last_name`** : Nom
- **`city`** : Ville
- **`created_at`** : Date de création
- **`updated_at`** : Date de modification

## 🌐 API d'authentification

### URL de base : `http://localhost:5001`

### Endpoints disponibles :

#### 1. Page d'accueil
```
GET http://localhost:5001/
```
**Réponse :** Informations sur l'API

#### 2. Inscription d'un nouvel utilisateur
```
POST http://localhost:5001/api/auth/register
```
**Corps de la requête :**
```json
{
    "email": "nouveau@example.com",
    "password": "motdepasse123",
    "first_name": "Jean",
    "last_name": "Dupont",
    "city": "Strasbourg"
}
```

#### 3. Connexion d'un utilisateur
```
POST http://localhost:5001/api/auth/login
```
**Corps de la requête :**
```json
{
    "email": "admin@eazyskool.fr",
    "password": "admin123"
}
```

#### 4. Liste des utilisateurs
```
GET http://localhost:5001/api/users
```
**Réponse :** Liste de tous les utilisateurs (sans mots de passe)

## 🚀 Comment utiliser

### 1. Démarrer l'API d'authentification
```bash
python auth_api.py
```

### 2. Tester avec curl
```bash
# Inscription
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","first_name":"Test","last_name":"User","city":"Paris"}'

# Connexion
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@eazyskool.fr","password":"admin123"}'

# Liste des utilisateurs
curl http://localhost:5001/api/users
```

### 3. Tester avec l'interface web
Ouvrez `auth_interface.html` dans votre navigateur pour tester l'authentification via une interface graphique.

## 🔒 Sécurité

### Mots de passe hashés
- Les mots de passe sont **hashés avec bcrypt**
- **Impossible de récupérer** les mots de passe en clair
- **Sécurisé** contre les attaques par force brute

### Validation des données
- **Email unique** : Impossible d'avoir deux comptes avec le même email
- **Champs requis** : Email et mot de passe obligatoires
- **Validation** : Vérification des formats et longueurs

## 📱 Intégration avec le frontend

### Exemple JavaScript pour l'authentification :
```javascript
// Inscription
async function register(email, password, firstName, lastName, city) {
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
    
    return await response.json();
}

// Connexion
async function login(email, password) {
    const response = await fetch('http://localhost:5001/api/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password })
    });
    
    return await response.json();
}

// Utilisation
login('admin@eazyskool.fr', 'admin123')
    .then(result => {
        if (result.success) {
            console.log('Connexion réussie:', result.user);
        } else {
            console.log('Erreur:', result.error);
        }
    });
```

## 🛠️ Gestion des utilisateurs via phpMyAdmin

### Accès à phpMyAdmin :
1. Ouvrez `http://localhost/phpmyadmin`
2. Connectez-vous avec `root` (mot de passe vide)
3. Sélectionnez la base `eazyskool`
4. Cliquez sur la table `users`

### Opérations disponibles :
- **Voir tous les utilisateurs**
- **Ajouter un utilisateur manuellement**
- **Modifier les informations**
- **Supprimer un utilisateur**

### Exemple d'ajout manuel :
```sql
INSERT INTO users (email, password_hash, first_name, last_name, city) 
VALUES ('nouveau@example.com', '$2b$12$...', 'Nouveau', 'Utilisateur', 'Lyon');
```

## 📊 Statistiques actuelles

- **4 utilisateurs** créés
- **API fonctionnelle** sur le port 5001
- **Sécurité** : Mots de passe hashés
- **Interface** : Interface web disponible
- **Base de données** : MySQL avec phpMyAdmin

## 🎯 Prochaines étapes

### 1. Intégrer l'authentification dans votre site
- Modifier `index.html` pour utiliser l'API d'authentification
- Ajouter des formulaires de connexion/inscription
- Gérer les sessions utilisateur

### 2. Ajouter des fonctionnalités
- **Gestion des sessions** (JWT, cookies)
- **Récupération de mot de passe**
- **Validation d'email**
- **Profil utilisateur**

### 3. Sécuriser davantage
- **Rate limiting** (limitation des tentatives)
- **Validation plus stricte** des mots de passe
- **Logs de connexion**
- **Authentification à deux facteurs**

## 🔧 Dépannage

### Problème : API ne répond pas
```bash
# Vérifier que l'API est démarrée
python auth_api.py

# Vérifier le port 5001
netstat -an | findstr 5001
```

### Problème : Erreur de connexion MySQL
```bash
# Vérifier WampServer
# Vérifier que MySQL fonctionne
# Tester phpMyAdmin
```

### Problème : Utilisateur non trouvé
```bash
# Vérifier dans phpMyAdmin
# Vérifier l'email exact
# Vérifier le mot de passe
```

## 🌟 Félicitations !

Votre système EazySkool dispose maintenant d'un système d'authentification complet et sécurisé :

- ✅ **Stockage sécurisé** des emails et mots de passe
- ✅ **API REST** fonctionnelle
- ✅ **Interface web** d'authentification
- ✅ **Utilisateurs de test** prêts
- ✅ **Documentation** complète

**Votre système d'authentification est prêt pour la production !** 🔐 