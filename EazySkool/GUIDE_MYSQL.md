# Guide d'installation et configuration MySQL pour EazySkool

## 📋 Prérequis

1. **WampServer** installé et configuré
2. **Python 3.7+** installé
3. **phpMyAdmin** accessible via WampServer

## 🚀 Installation étape par étape

### Étape 1: Vérifier WampServer

1. Ouvrez WampServer
2. Vérifiez que l'icône dans la barre des tâches est **verte**
3. Si elle est orange ou rouge, attendez ou redémarrez WampServer

### Étape 2: Créer la base de données

1. Ouvrez votre navigateur
2. Allez sur `http://localhost/phpmyadmin`
3. Connectez-vous (utilisateur: `root`, mot de passe: vide par défaut)
4. Cliquez sur **"Nouvelle base de données"**
5. Nommez-la `eazyskool`
6. Sélectionnez l'interclassement `utf8mb4_unicode_ci`
7. Cliquez sur **"Créer"**

### Étape 3: Importer les tables

1. Dans phpMyAdmin, sélectionnez la base `eazyskool`
2. Cliquez sur l'onglet **"Importer"**
3. Cliquez sur **"Choisir un fichier"**
4. Sélectionnez le fichier `eazyskool_mysql.sql`
5. Cliquez sur **"Exécuter"**

### Étape 4: Installer les dépendances Python

```bash
pip install -r requirements.txt
```

### Étape 5: Tester la connexion

```bash
python mysql_database_manager.py
```

Si tout fonctionne, vous devriez voir: `✅ Connexion MySQL réussie!`

## 🎯 Utilisation

### Démarrage rapide

```bash
python start_mysql.py
```

Ce script va:
- Vérifier les dépendances
- Tester la connexion MySQL
- Démarrer le serveur API
- Ouvrir le navigateur

### Démarrage manuel

1. **Démarrer le serveur API:**
   ```bash
   python mysql_api_server.py
   ```

2. **Ouvrir l'interface web:**
   - Ouvrez `index.html` dans votre navigateur
   - Ou utilisez `script_with_api.js` pour la version API

## 📊 Structure de la base de données

### Tables principales

- **`users`** - Utilisateurs du système
- **`schools`** - Écoles et établissements
- **`cities`** - Villes
- **`school_types`** - Types d'écoles
- **`specializations`** - Spécialisations
- **`school_specializations`** - Liaison écoles-spécialisations
- **`school_images`** - Images des écoles
- **`reviews`** - Avis des utilisateurs
- **`favorites`** - Favoris des utilisateurs
- **`events`** - Événements

### Vues utiles

- **`schools_complete`** - Écoles avec toutes les informations
- **`reviews_with_users`** - Avis avec informations utilisateur

## 🔧 Configuration

### Paramètres de connexion MySQL

Par défaut, le système utilise:
- **Host:** `localhost`
- **Port:** `3306`
- **User:** `root`
- **Password:** (vide)
- **Database:** `eazyskool`

Pour modifier ces paramètres, éditez `mysql_database_manager.py`:

```python
db = EazySkoolMySQLDB(
    host='localhost',
    user='root',
    password='votre_mot_de_passe',
    database='eazyskool',
    port=3306
)
```

## 🌐 API Endpoints

### Écoles
- `GET /api/schools` - Liste toutes les écoles
- `GET /api/schools/<id>` - Détails d'une école
- `GET /api/schools/search?q=<query>` - Recherche d'écoles

### Authentification
- `POST /api/auth/register` - Inscription
- `POST /api/auth/login` - Connexion

### Favoris
- `GET /api/favorites/<user_id>` - Favoris d'un utilisateur
- `POST /api/favorites` - Ajouter un favori
- `DELETE /api/favorites` - Supprimer un favori

### Autres
- `GET /api/cities` - Liste des villes
- `GET /api/school-types` - Types d'écoles
- `GET /api/events` - Événements
- `GET /api/test-connection` - Test de connexion

## 🛠️ Dépannage

### Problème: Connexion MySQL échoue

**Solutions:**
1. Vérifiez que WampServer est démarré
2. Vérifiez que l'icône WampServer est verte
3. Testez l'accès à phpMyAdmin
4. Vérifiez que la base `eazyskool` existe

### Problème: Erreur "Access denied"

**Solutions:**
1. Vérifiez le mot de passe root MySQL
2. Créez un utilisateur MySQL dédié:
   ```sql
   CREATE USER 'eazyskool'@'localhost' IDENTIFIED BY 'password';
   GRANT ALL PRIVILEGES ON eazyskool.* TO 'eazyskool'@'localhost';
   FLUSH PRIVILEGES;
   ```

### Problème: Tables manquantes

**Solutions:**
1. Importez à nouveau le fichier `eazyskool_mysql.sql`
2. Vérifiez que l'import s'est bien passé
3. Vérifiez les logs d'erreur dans phpMyAdmin

### Problème: Dépendances Python manquantes

**Solutions:**
```bash
pip install mysql-connector-python flask flask-cors bcrypt
```

## 📈 Avantages de MySQL vs SQLite

1. **Performance** - Plus rapide pour les grosses bases
2. **Concurrence** - Gestion multi-utilisateurs
3. **Sécurité** - Authentification et permissions
4. **Interface** - phpMyAdmin pour la gestion
5. **Scalabilité** - Adapté aux applications en production

## 🔄 Migration depuis SQLite

Si vous avez déjà des données dans SQLite:

1. Exportez les données SQLite:
   ```bash
   python database_manager.py
   ```

2. Importez dans MySQL via phpMyAdmin

3. Vérifiez l'intégrité des données

## 📞 Support

En cas de problème:
1. Vérifiez les logs du serveur API
2. Testez la connexion MySQL directement
3. Consultez la documentation phpMyAdmin
4. Vérifiez les permissions MySQL

---

**🎓 EazySkool avec MySQL - Prêt pour la production!** 