-- Script SQL pour créer la base de données EazySkool dans MySQL
-- À exécuter dans phpMyAdmin

-- Création des tables

-- Table des utilisateurs
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    city VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table des types d'écoles
CREATE TABLE school_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-- Table des villes
CREATE TABLE cities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    region VARCHAR(100)
);

-- Table des écoles
CREATE TABLE schools (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(255),
    website VARCHAR(255),
    city_id INT,
    school_type_id INT,
    rating DECIMAL(3,2) DEFAULT 0.00,
    price_range VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities(id),
    FOREIGN KEY (school_type_id) REFERENCES school_types(id)
);

-- Table des images d'écoles
CREATE TABLE school_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    school_id INT,
    image_url VARCHAR(500) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE
);

-- Table des spécialisations
CREATE TABLE specializations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-- Table de liaison écoles-spécialisations
CREATE TABLE school_specializations (
    school_id INT,
    specialization_id INT,
    PRIMARY KEY (school_id, specialization_id),
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (specialization_id) REFERENCES specializations(id) ON DELETE CASCADE
);

-- Table des avis
CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    school_id INT,
    user_id INT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Table des favoris
CREATE TABLE favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    school_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_school (user_id, school_id)
);

-- Table des événements
CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    event_date DATE,
    event_time TIME,
    location VARCHAR(255),
    school_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE
);

-- Insertion des données initiales

-- Types d'écoles
INSERT INTO school_types (name, description) VALUES
('École de commerce', 'Formation en management et commerce'),
('École d\'ingénieur', 'Formation en ingénierie et sciences'),
('École d\'art', 'Formation en arts et design'),
('École de communication', 'Formation en communication et médias'),
('École de santé', 'Formation en santé et paramédical'),
('École de droit', 'Formation en droit et sciences juridiques');

-- Villes
INSERT INTO cities (name, region) VALUES
('Strasbourg', 'Grand Est'),
('Nancy', 'Grand Est'),
('Metz', 'Grand Est'),
('Reims', 'Grand Est'),
('Troyes', 'Grand Est'),
('Châlons-en-Champagne', 'Grand Est');

-- Spécialisations
INSERT INTO specializations (name, description) VALUES
('Marketing Digital', 'Formation en marketing digital et e-commerce'),
('Intelligence Artificielle', 'Formation en IA et machine learning'),
('Finance', 'Formation en finance et gestion'),
('Informatique', 'Formation en développement et systèmes'),
('Design Graphique', 'Formation en design et création'),
('Communication', 'Formation en communication et médias'),
('Santé', 'Formation en santé et bien-être'),
('Droit', 'Formation en droit et législation');

-- Écoles
INSERT INTO schools (name, description, address, phone, email, website, city_id, school_type_id, rating, price_range) VALUES
('EM Strasbourg', 'École de management de Strasbourg', '61 Avenue de la Forêt-Noire, 67085 Strasbourg', '03 88 41 77 77', 'contact@em-strasbourg.eu', 'https://www.em-strasbourg.eu', 1, 1, 4.5, '8000-12000€'),
('INSA Strasbourg', 'Institut National des Sciences Appliquées', '24 Boulevard de la Victoire, 67084 Strasbourg', '03 88 14 47 00', 'contact@insa-strasbourg.fr', 'https://www.insa-strasbourg.fr', 1, 2, 4.3, '600€'),
('ESAD Strasbourg', 'École Supérieure d\'Art Dramatique', '7 Rue de l\'Académie, 67000 Strasbourg', '03 88 25 69 74', 'contact@esad-stg.fr', 'https://www.esad-stg.fr', 1, 3, 4.1, '400€'),
('ICN Business School', 'École de commerce à Nancy', '86 Rue du Sergent Blandan, 54003 Nancy', '03 54 50 25 00', 'contact@icn-artem.com', 'https://www.icn-artem.com', 2, 1, 4.2, '9000-11000€'),
('CentraleSupélec Metz', 'École d\'ingénieur', '2 Rue Édouard Belin, 57070 Metz', '03 87 34 69 00', 'contact@centralesupelec.fr', 'https://www.centralesupelec.fr', 3, 2, 4.4, '600€'),
('NEOMA Business School', 'École de commerce à Reims', '59 Rue Pierre Taittinger, 51100 Reims', '03 26 77 46 00', 'contact@neoma-bs.fr', 'https://www.neoma-bs.fr', 4, 1, 4.0, '8500-11500€'),
('UTT Troyes', 'Université de Technologie de Troyes', '12 Rue Marie Curie, 10004 Troyes', '03 25 71 76 00', 'contact@utt.fr', 'https://www.utt.fr', 5, 2, 4.2, '600€'),
('ESC Troyes', 'École Supérieure de Commerce', '217 Avenue Pierre Brossolette, 10000 Troyes', '03 25 49 49 49', 'contact@esctroyes.fr', 'https://www.esctroyes.fr', 5, 1, 3.9, '7500-9500€');

-- Images d'écoles
INSERT INTO school_images (school_id, image_url, is_primary) VALUES
(1, 'https://example.com/em-strasbourg.jpg', TRUE),
(1, 'https://example.com/em-strasbourg-2.jpg', FALSE),
(2, 'https://example.com/insa-strasbourg.jpg', TRUE),
(3, 'https://example.com/esad-strasbourg.jpg', TRUE),
(4, 'https://example.com/icn-nancy.jpg', TRUE),
(5, 'https://example.com/centralesupelec-metz.jpg', TRUE),
(6, 'https://example.com/neoma-reims.jpg', TRUE),
(7, 'https://example.com/utt-troyes.jpg', TRUE),
(8, 'https://example.com/esc-troyes.jpg', TRUE);

-- Liaisons écoles-spécialisations
INSERT INTO school_specializations (school_id, specialization_id) VALUES
(1, 1), (1, 3), -- EM Strasbourg: Marketing Digital, Finance
(2, 4), (2, 2), -- INSA Strasbourg: Informatique, IA
(3, 5), (3, 6), -- ESAD Strasbourg: Design Graphique, Communication
(4, 1), (4, 3), -- ICN Nancy: Marketing Digital, Finance
(5, 4), (5, 2), -- CentraleSupélec Metz: Informatique, IA
(6, 1), (6, 3), -- NEOMA Reims: Marketing Digital, Finance
(7, 4), (7, 2), -- UTT Troyes: Informatique, IA
(8, 1), (8, 3); -- ESC Troyes: Marketing Digital, Finance

-- Événements
INSERT INTO events (title, description, event_date, event_time, location, school_id) VALUES
('Journée Portes Ouvertes', 'Découvrez notre école et nos formations', '2024-03-15', '09:00:00', 'Campus principal', 1),
('Conférence IA', 'L\'intelligence artificielle dans l\'éducation', '2024-03-20', '14:00:00', 'Amphithéâtre A', 2),
('Workshop Design', 'Atelier de design graphique', '2024-03-25', '10:00:00', 'Atelier créatif', 3),
('Salon des métiers', 'Rencontrez les professionnels', '2024-04-10', '13:00:00', 'Hall d\'exposition', 4);

-- Création des vues utiles

-- Vue des écoles complètes avec toutes les informations
CREATE VIEW schools_complete AS
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
GROUP BY s.id;

-- Vue des avis avec informations utilisateur
CREATE VIEW reviews_with_users AS
SELECT 
    r.*,
    u.first_name,
    u.last_name,
    s.name as school_name
FROM reviews r
JOIN users u ON r.user_id = u.id
JOIN schools s ON r.school_id = s.id;

-- Création des index pour les performances
CREATE INDEX idx_schools_city ON schools(city_id);
CREATE INDEX idx_schools_type ON schools(school_type_id);
CREATE INDEX idx_reviews_school ON reviews(school_id);
CREATE INDEX idx_favorites_user ON favorites(user_id);
CREATE INDEX idx_events_school ON events(school_id); 