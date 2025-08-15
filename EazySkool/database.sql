-- =================================================================================
-- EazySkool Database Schema
-- Base de données pour la plateforme de recherche d'écoles
-- =================================================================================

-- Table des utilisateurs
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    city VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des types d'écoles
CREATE TABLE school_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-- Table des villes
CREATE TABLE cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    region VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8)
);

-- Table principale des écoles
CREATE TABLE schools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    type_id INTEGER NOT NULL,
    city_id INTEGER NOT NULL,
    description TEXT,
    website VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    average_rating DECIMAL(3, 2) DEFAULT 0.0,
    total_reviews INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (type_id) REFERENCES school_types(id),
    FOREIGN KEY (city_id) REFERENCES cities(id)
);

-- Table des images d'écoles
CREATE TABLE school_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_id INTEGER NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    is_primary BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id)
);

-- Table des avis/commentaires
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Table des favoris
CREATE TABLE favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    school_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, school_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (school_id) REFERENCES schools(id)
);

-- Table des événements
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    event_date DATE NOT NULL,
    event_time TIME,
    location VARCHAR(255),
    school_id INTEGER,
    is_online BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (school_id) REFERENCES schools(id)
);

-- Table des spécialités/formations
CREATE TABLE specializations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100)
);

-- Table de liaison écoles-spécialités
CREATE TABLE school_specializations (
    school_id INTEGER NOT NULL,
    specialization_id INTEGER NOT NULL,
    PRIMARY KEY (school_id, specialization_id),
    FOREIGN KEY (school_id) REFERENCES schools(id),
    FOREIGN KEY (specialization_id) REFERENCES specializations(id)
);

-- =================================================================================
-- INSERTION DES DONNÉES DE BASE
-- =================================================================================

-- Insertion des types d'écoles
INSERT INTO school_types (name, description) VALUES
('Université', 'Établissement public d''enseignement supérieur'),
('École de commerce', 'École spécialisée dans le management et le commerce'),
('Institut d''études politiques', 'École spécialisée en sciences politiques'),
('École d''ingénieur', 'École spécialisée en ingénierie'),
('École d''art', 'École spécialisée dans les arts'),
('École de santé', 'École spécialisée dans les métiers de la santé');

-- Insertion des villes
INSERT INTO cities (name, region, latitude, longitude) VALUES
('Strasbourg', 'Grand Est', 48.5839, 7.7455),
('Nancy', 'Grand Est', 48.6921, 6.1844),
('Mulhouse', 'Grand Est', 47.7508, 7.3359),
('Metz', 'Grand Est', 49.1193, 6.1757),
('Reims', 'Grand Est', 49.2583, 4.0317),
('Troyes', 'Grand Est', 48.2973, 4.0744);

-- Insertion des écoles
INSERT INTO schools (name, type_id, city_id, description, website, email, phone, address, latitude, longitude, average_rating, total_reviews) VALUES
('Université de Strasbourg', 1, 1, 'L''Université de Strasbourg est l''une des plus grandes universités de France, reconnue pour la qualité de son enseignement et de sa recherche.', 'https://www.unistra.fr/', 'contact@unistra.fr', '03 68 85 00 00', '4 rue Blaise Pascal, 67081 Strasbourg', 48.5839, 7.7455, 4.6, 127),
('Université de Lorraine', 1, 2, 'L''Université de Lorraine propose une offre de formation complète et innovante dans de nombreux domaines.', 'https://www.univ-lorraine.fr/', 'contact@univ-lorraine.fr', '03 72 74 00 00', '34 cours Léopold, 54000 Nancy', 48.6921, 6.1844, 4.3, 89),
('ICN Business School', 2, 2, 'ICN Business School est une grande école de management reconnue internationalement.', 'https://www.icn-artem.com/', 'contact@icn-artem.com', '03 54 50 25 00', '86 rue du Sergent Blandan, 54003 Nancy', 48.6937, 6.1843, 4.5, 156),
('Sciences Po Strasbourg', 3, 1, 'Sciences Po Strasbourg forme les futurs cadres de la fonction publique et du secteur privé.', 'https://www.sciencespo-strasbourg.fr/', 'contact@sciencespo-strasbourg.fr', '03 68 85 84 00', '47 avenue de la Forêt-Noire, 67082 Strasbourg', 48.5846, 7.7616, 4.7, 203),
('Université de Haute-Alsace', 1, 3, 'L''Université de Haute-Alsace est reconnue pour ses formations en sciences, technologies et ingénierie.', 'https://www.uha.fr/', 'contact@uha.fr', '03 89 33 64 00', '2 rue des Frères Lumière, 68093 Mulhouse', 47.7508, 7.3359, 4.2, 67),
('INSA Strasbourg', 4, 1, 'L''INSA Strasbourg forme des ingénieurs dans de nombreux domaines techniques.', 'https://www.insa-strasbourg.fr/', 'contact@insa-strasbourg.fr', '03 88 14 47 00', '24 boulevard de la Victoire, 67084 Strasbourg', 48.5840, 7.7460, 4.4, 134),
('Université de Reims Champagne-Ardenne', 1, 5, 'L''URCA propose des formations dans tous les domaines de la connaissance.', 'https://www.univ-reims.fr/', 'contact@univ-reims.fr', '03 26 91 30 00', 'Campus Croix-Rouge, 51100 Reims', 49.2583, 4.0317, 4.1, 78),
('Université de Troyes', 1, 6, 'L''UTT est spécialisée dans les technologies et l''innovation.', 'https://www.utt.fr/', 'contact@utt.fr', '03 25 71 76 00', '12 rue Marie Curie, 10004 Troyes', 48.2973, 4.0744, 4.0, 45);

-- Insertion des images d'écoles
INSERT INTO school_images (school_id, image_path, is_primary) VALUES
(1, 'images/strasbourg.jpg', 1),
(1, 'images/icn_campus.jpg', 0),
(2, 'images/strasbourg.jpg', 1),
(3, 'images/icn_campus.jpg', 1),
(4, 'images/sciencespo_batiment.jpg', 1),
(5, 'images/uha_campus.jpg', 1),
(6, 'images/INSA Strasbourg.jpg', 1),
(7, 'images/urca_campus.jpg', 1),
(8, 'images/strasbourg.jpg', 1);

-- Insertion des spécialités
INSERT INTO specializations (name, description, category) VALUES
('Informatique', 'Formations en développement, réseaux, intelligence artificielle', 'Technologies'),
('Médecine', 'Formations médicales et paramédicales', 'Santé'),
('Droit', 'Formations juridiques et sciences politiques', 'Droit'),
('Commerce', 'Formations en management et commerce', 'Commerce'),
('Ingénierie', 'Formations d''ingénieurs dans tous domaines', 'Technologies'),
('Arts', 'Formations artistiques et culturelles', 'Arts'),
('Sciences', 'Formations en mathématiques, physique, chimie', 'Sciences'),
('Langues', 'Formations en langues étrangères', 'Langues');

-- Liaison écoles-spécialités
INSERT INTO school_specializations (school_id, specialization_id) VALUES
(1, 1), (1, 3), (1, 7), (1, 8), -- Université de Strasbourg
(2, 1), (2, 4), (2, 5), (2, 7), -- Université de Lorraine
(3, 4), -- ICN Business School
(4, 3), (4, 4), -- Sciences Po Strasbourg
(5, 1), (5, 5), (5, 7), -- Université de Haute-Alsace
(6, 1), (6, 5), -- INSA Strasbourg
(7, 1), (7, 2), (7, 7), -- Université de Reims
(8, 1), (8, 5), (8, 7); -- Université de Troyes

-- Insertion d'événements
INSERT INTO events (title, description, event_date, event_time, location, school_id, is_online) VALUES
('Portes ouvertes', 'Découvrez nos formations et rencontrez nos équipes', '2024-09-27', '09:00:00', 'Nancy', 2, 0),
('Salon étudiant', 'Salon de l''orientation post-bac', '2024-10-05', '10:00:00', 'Strasbourg', NULL, 0),
('Webinaire orientation', 'Conseils pour choisir sa formation', '2024-10-12', '18:00:00', 'En ligne', NULL, 1),
('Journée découverte ICN', 'Immersion dans la vie étudiante', '2024-10-20', '14:00:00', 'Nancy', 3, 0);

-- =================================================================================
-- INDEX POUR OPTIMISER LES PERFORMANCES
-- =================================================================================

CREATE INDEX idx_schools_city ON schools(city_id);
CREATE INDEX idx_schools_type ON schools(type_id);
CREATE INDEX idx_schools_rating ON schools(average_rating);
CREATE INDEX idx_reviews_school ON reviews(school_id);
CREATE INDEX idx_reviews_user ON reviews(user_id);
CREATE INDEX idx_favorites_user ON favorites(user_id);
CREATE INDEX idx_favorites_school ON favorites(school_id);
CREATE INDEX idx_events_date ON events(event_date);
CREATE INDEX idx_users_email ON users(email);

-- =================================================================================
-- VUES UTILES
-- =================================================================================

-- Vue pour les écoles avec toutes les informations
CREATE VIEW schools_complete AS
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
GROUP BY s.id;

-- Vue pour les avis avec informations utilisateur
CREATE VIEW reviews_with_users AS
SELECT 
    r.id,
    r.school_id,
    r.user_id,
    r.rating,
    r.comment,
    r.created_at,
    u.first_name,
    u.last_name,
    u.city as user_city
FROM reviews r
JOIN users u ON r.user_id = u.id; 