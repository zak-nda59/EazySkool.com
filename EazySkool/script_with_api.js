// =================================================================================
// EazySkool - script_with_api.js
// Version modifiée pour utiliser l'API au lieu des données statiques
// =================================================================================

// Configuration de l'API
const API_BASE_URL = 'http://localhost:5000/api';

// --- VARIABLES GLOBALES ET CONSTANTES ---
const SCHOOLS_PER_PAGE = 6;
let currentPage = 1;
let ecoleData = []; // La liste des écoles actuellement affichées (filtrées/triées)
let modalMap = null;
let modalMarkers = [];

// =================================================================================
// --- FONCTIONS API ---
// =================================================================================

// Fonction pour faire des appels API
async function apiCall(endpoint, options = {}) {
    try {
        const url = `${API_BASE_URL}${endpoint}`;
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erreur API:', error);
        return { success: false, error: error.message };
    }
}

// Récupère toutes les écoles depuis l'API
async function loadSchoolsFromAPI() {
    const result = await apiCall('/schools');
    if (result.success) {
        return result.data;
    } else {
        console.error('Erreur lors du chargement des écoles:', result.error);
        return [];
    }
}

// Recherche des écoles via l'API
async function searchSchoolsFromAPI(query, city, schoolType) {
    const params = new URLSearchParams();
    if (query) params.append('q', query);
    if (city) params.append('city', city);
    if (schoolType) params.append('type', schoolType);
    
    const result = await apiCall(`/schools/search?${params.toString()}`);
    if (result.success) {
        return result.data;
    } else {
        console.error('Erreur lors de la recherche:', result.error);
        return [];
    }
}

// Récupère une école par son ID
async function getSchoolByIdFromAPI(schoolId) {
    const result = await apiCall(`/schools/${schoolId}`);
    if (result.success) {
        return result.data;
    } else {
        console.error('Erreur lors du chargement de l\'école:', result.error);
        return null;
    }
}

// Récupère les villes depuis l'API
async function loadCitiesFromAPI() {
    const result = await apiCall('/cities');
    if (result.success) {
        return result.data;
    } else {
        console.error('Erreur lors du chargement des villes:', result.error);
        return [];
    }
}

// Récupère les types d'écoles depuis l'API
async function loadSchoolTypesFromAPI() {
    const result = await apiCall('/types');
    if (result.success) {
        return result.data;
    } else {
        console.error('Erreur lors du chargement des types:', result.error);
        return [];
    }
}

// Récupère les événements depuis l'API
async function loadEventsFromAPI() {
    const result = await apiCall('/events');
    if (result.success) {
        return result.data;
    } else {
        console.error('Erreur lors du chargement des événements:', result.error);
        return [];
    }
}

// Authentification utilisateur
async function loginUser(email, password) {
    const result = await apiCall('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
    });
    
    if (result.success) {
        return result.data;
    } else {
        throw new Error(result.error || 'Erreur de connexion');
    }
}

// Création de compte utilisateur
async function registerUser(userData) {
    const result = await apiCall('/auth/register', {
        method: 'POST',
        body: JSON.stringify(userData)
    });
    
    if (result.success) {
        return result.data;
    } else {
        throw new Error(result.error || 'Erreur de création de compte');
    }
}

// Gestion des favoris via l'API
async function getUserFavorites(userId) {
    const result = await apiCall('/favorites', {
        method: 'POST',
        body: JSON.stringify({ user_id: userId })
    });
    
    if (result.success) {
        return result.data;
    } else {
        console.error('Erreur lors du chargement des favoris:', result.error);
        return [];
    }
}

async function addFavorite(userId, schoolId) {
    const result = await apiCall('/favorites', {
        method: 'POST',
        body: JSON.stringify({ user_id: userId, school_id: schoolId })
    });
    
    return result.success;
}

async function removeFavorite(userId, schoolId) {
    const result = await apiCall('/favorites', {
        method: 'DELETE',
        body: JSON.stringify({ user_id: userId, school_id: schoolId })
    });
    
    return result.success;
}

// Ajout d'un avis
async function addReview(schoolId, userId, rating, comment) {
    const result = await apiCall('/reviews', {
        method: 'POST',
        body: JSON.stringify({
            school_id: schoolId,
            user_id: userId,
            rating: rating,
            comment: comment
        })
    });
    
    return result.success;
}

// =================================================================================
// --- FONCTIONS GLOBALES (HELPERS) ---
// =================================================================================

// --- Helpers pour l'Authentification ---
function getUsers() { return JSON.parse(localStorage.getItem('eazyskool_users') || '{}'); }
function setUsers(users) { localStorage.setItem('eazyskool_users', JSON.stringify(users)); }
function getCurrentUser() { return localStorage.getItem('eazyskool_current_user'); }
function setCurrentUser(user) { 
    if (user) {
        localStorage.setItem('eazyskool_current_user', JSON.stringify(user));
    } else {
        localStorage.removeItem('eazyskool_current_user');
    }
}
function logout() { setCurrentUser(null); }

// --- Helpers pour les Favoris ---
function getFavs() { return JSON.parse(localStorage.getItem('eazyskool_favs') || '[]'); }
function setFavs(favs) { localStorage.setItem('eazyskool_favs', JSON.stringify(favs)); }
function isFav(id) { return getFavs().includes(id); }

// --- Helpers pour les Images ---
function getEcoleImages(ecole) {
    // Utilise les images de la base de données si disponibles
    if (ecole.images && ecole.images.length > 0) {
        return ecole.images.map(img => img.path);
    }
    
    // Fallback vers les images statiques
    const imageMap = {
        'Université de Strasbourg': ['images/strasbourg.jpg'],
        'Université de Lorraine': ['images/strasbourg.jpg'],
        'ICN Business School': ['images/icn_campus.jpg'],
        'Sciences Po Strasbourg': ['images/sciencespo_batiment.jpg'],
        'Université de Haute-Alsace': ['images/uha_campus.jpg'],
        'INSA Strasbourg': ['images/INSA Strasbourg.jpg'],
        'Université de Reims Champagne-Ardenne': ['images/urca_campus.jpg'],
        'Université de Troyes': ['images/strasbourg.jpg']
    };
    
    return imageMap[ecole.name] || ['images/strasbourg.jpg'];
}

// =================================================================================
// --- FONCTIONS UTILITAIRES ---
// =================================================================================

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    const container = document.getElementById('toast-container');
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => container.removeChild(toast), 300);
    }, 3000);
}

function openModal(modal) { if(modal) modal.style.display = 'flex'; }
function closeModal(modal) { if(modal) modal.style.display = 'none'; }

function showSection(sectionId) {
    document.querySelectorAll('.spa-section').forEach(section => {
        section.style.display = 'none';
    });
    document.getElementById(sectionId).style.display = 'block';
    
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    document.querySelector(`[data-section="${sectionId.replace('section-', '')}"]`).classList.add('active');
}

function updateUserInfo() {
    const userInfo = document.getElementById('user-info');
    const currentUser = getCurrentUser();
    
    if (currentUser) {
        const user = JSON.parse(currentUser);
        userInfo.innerHTML = `
            <span>Bonjour, ${user.first_name || user.email}</span>
            <button onclick="logout()" class="btn btn-secondary btn-sm">Déconnexion</button>
        `;
        userInfo.style.display = 'block';
    } else {
        userInfo.style.display = 'none';
    }
}

// =================================================================================
// --- FONCTIONS D'AFFICHAGE ---
// =================================================================================

async function renderSchoolsListTo(list, container) {
    container.innerHTML = '';
    
    if (list.length === 0) {
        container.innerHTML = '<div class="empty-state"><i class="fa-solid fa-search"></i><h3>Aucune école trouvée</h3><p>Aucune école ne correspond à vos critères de recherche.</p></div>';
        return;
    }
    
    const startIndex = (currentPage - 1) * SCHOOLS_PER_PAGE;
    const endIndex = startIndex + SCHOOLS_PER_PAGE;
    const schoolsToShow = list.slice(startIndex, endIndex);
    
    schoolsToShow.forEach(ecole => {
        const images = getEcoleImages(ecole);
        const isFavorite = isFav(ecole.id);
        
        const schoolCard = document.createElement('div');
        schoolCard.className = 'school-card';
        schoolCard.innerHTML = `
            <div class="school-card-image">
                <img src="${images[0]}" alt="${ecole.name}" />
                <button class="favorite-btn ${isFavorite ? 'favorited' : ''}" onclick="toggleFavAndRefresh(${ecole.id})">
                    <i class="fa-solid fa-star"></i>
                </button>
            </div>
            <div class="school-card-content">
                <h3>${ecole.name}</h3>
                <div class="school-meta">
                    <span class="school-type">${ecole.type_name}</span>
                    <span class="school-location"><i class="fa-solid fa-map-marker-alt"></i> ${ecole.city_name}</span>
                </div>
                <div class="school-rating">
                    <div class="stars">
                        ${'★'.repeat(Math.floor(ecole.average_rating))}${'☆'.repeat(5 - Math.floor(ecole.average_rating))}
                    </div>
                    <span class="rating-text">${ecole.average_rating.toFixed(1)} (${ecole.total_reviews} avis)</span>
                </div>
                <p class="school-description">${ecole.description.substring(0, 120)}...</p>
                <button class="btn btn-primary" onclick="openSchoolModal(${ecole.id})">
                    Voir les détails
                </button>
            </div>
        `;
        
        container.appendChild(schoolCard);
    });
    
    // Pagination
    renderPagination(list.length);
}

async function renderFavoritesList() {
    const container = document.getElementById('favorites-list');
    const currentUser = getCurrentUser();
    
    if (!currentUser) {
        container.innerHTML = '<div class="empty-state"><i class="fa-solid fa-star"></i><h3>Connectez-vous</h3><p>Connectez-vous pour voir vos écoles favorites.</p></div>';
        return;
    }
    
    const user = JSON.parse(currentUser);
    const favorites = await getUserFavorites(user.id);
    
    if (favorites.length === 0) {
        container.innerHTML = '<div class="empty-state"><i class="fa-solid fa-star"></i><h3>Aucun favori</h3><p>Vous n\'avez pas encore d\'écoles favorites.</p></div>';
        return;
    }
    
    container.innerHTML = '';
    favorites.forEach(favorite => {
        const favoriteCard = document.createElement('div');
        favoriteCard.className = 'favorite-card';
        favoriteCard.innerHTML = `
            <div class="favorite-card-content">
                <h3>${favorite.name}</h3>
                <div class="favorite-meta">
                    <span class="favorite-type">${favorite.type_name}</span>
                    <span class="favorite-location">${favorite.city_name}</span>
                </div>
                <div class="favorite-rating">
                    <div class="stars">
                        ${'★'.repeat(Math.floor(favorite.average_rating))}${'☆'.repeat(5 - Math.floor(favorite.average_rating))}
                    </div>
                    <span>${favorite.average_rating.toFixed(1)} (${favorite.total_reviews} avis)</span>
                </div>
                <button class="btn btn-primary" onclick="openSchoolModal(${favorite.id})">
                    Voir les détails
                </button>
            </div>
        `;
        container.appendChild(favoriteCard);
    });
}

// =================================================================================
// --- FONCTIONS D'INTERACTION ---
// =================================================================================

async function openSchoolModal(schoolId) {
    const school = await getSchoolByIdFromAPI(schoolId);
    if (!school) {
        showToast('Erreur lors du chargement de l\'école', 'error');
        return;
    }
    
    const modal = document.getElementById('school-modal');
    const modalBody = document.getElementById('school-modal-body');
    const template = document.getElementById('school-modal-template');
    
    // Clone le template
    const modalContent = template.content.cloneNode(true);
    
    // Remplit les données
    modalContent.querySelector('.school-modal-title').textContent = school.name;
    modalContent.querySelector('.school-modal-avg-rating').innerHTML = `
        <div class="stars">
            ${'★'.repeat(Math.floor(school.average_rating))}${'☆'.repeat(5 - Math.floor(school.average_rating))}
        </div>
        <span>${school.average_rating.toFixed(1)} (${school.total_reviews} avis)</span>
    `;
    
    modalContent.querySelector('.school-modal-meta').innerHTML = `
        <div class="school-modal-info">
            <div><i class="fa-solid fa-graduation-cap"></i> ${school.type_name}</div>
            <div><i class="fa-solid fa-map-marker-alt"></i> ${school.city_name}</div>
            <div><i class="fa-solid fa-globe"></i> <a href="${school.website}" target="_blank">Site web</a></div>
        </div>
    `;
    
    modalContent.querySelector('.school-modal-desc').innerHTML = `
        <h4>Description</h4>
        <p>${school.description}</p>
        ${school.specializations.length > 0 ? `
            <h4>Spécialités</h4>
            <div class="specializations">
                ${school.specializations.map(spec => `<span class="specialization-tag">${spec}</span>`).join('')}
            </div>
        ` : ''}
    `;
    
    modalContent.querySelector('.school-modal-contact').innerHTML = `
        <h4>Contact</h4>
        <div class="contact-info">
            <div><i class="fa-solid fa-envelope"></i> ${school.email}</div>
            <div><i class="fa-solid fa-phone"></i> ${school.phone}</div>
            <div><i class="fa-solid fa-map-marker-alt"></i> ${school.address}</div>
        </div>
    `;
    
    modalContent.querySelector('.school-modal-actions').innerHTML = `
        <button class="btn btn-primary" onclick="toggleFavAndRefresh(${school.id})">
            <i class="fa-solid fa-star"></i> ${isFav(school.id) ? 'Retirer des favoris' : 'Ajouter aux favoris'}
        </button>
        <button class="btn btn-secondary" onclick="window.open('${school.website}', '_blank')">
            <i class="fa-solid fa-external-link-alt"></i> Visiter le site
        </button>
    `;
    
    // Affiche les avis
    const reviewsContainer = modalContent.querySelector('#reviews-list');
    if (school.reviews && school.reviews.length > 0) {
        school.reviews.forEach(review => {
            const reviewElement = document.createElement('div');
            reviewElement.className = 'review-item';
            reviewElement.innerHTML = `
                <div class="review-header">
                    <div class="review-author">${review.user_name}</div>
                    <div class="review-rating">
                        ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}
                    </div>
                </div>
                <div class="review-comment">${review.comment}</div>
                <div class="review-date">${new Date(review.created_at).toLocaleDateString()}</div>
            `;
            reviewsContainer.appendChild(reviewElement);
        });
    } else {
        reviewsContainer.innerHTML = '<p>Aucun avis pour le moment.</p>';
    }
    
    // Remplace le contenu de la modal
    modalBody.innerHTML = '';
    modalBody.appendChild(modalContent);
    
    openModal(modal);
}

// =================================================================================
// --- FONCTIONS DE FILTRAGE ET RECHERCHE ---
// =================================================================================

async function applyFiltersAndSort() {
    const searchInput = document.getElementById('school-search-input');
    const sortSelect = document.getElementById('sort-by');
    
    const query = searchInput.value.trim();
    const sortBy = sortSelect.value;
    
    // Récupère les écoles depuis l'API
    ecoleData = await searchSchoolsFromAPI(query);
    
    // Applique le tri
    if (sortBy === 'avis-desc') {
        ecoleData.sort((a, b) => b.average_rating - a.average_rating);
    } else if (sortBy === 'nom-asc') {
        ecoleData.sort((a, b) => a.name.localeCompare(b.name));
    } else if (sortBy === 'nom-desc') {
        ecoleData.sort((a, b) => b.name.localeCompare(a.name));
    }
    
    currentPage = 1;
    renderSchoolsListTo(ecoleData, document.getElementById('schools-list'));
}

async function toggleFavAndRefresh(id) {
    const currentUser = getCurrentUser();
    if (!currentUser) {
        showToast('Connectez-vous pour ajouter des favoris', 'warning');
        return;
    }
    
    const user = JSON.parse(currentUser);
    const isCurrentlyFav = isFav(id);
    
    let success;
    if (isCurrentlyFav) {
        success = await removeFavorite(user.id, id);
        if (success) {
            const favs = getFavs().filter(favId => favId !== id);
            setFavs(favs);
            showToast('École retirée des favoris', 'success');
        }
    } else {
        success = await addFavorite(user.id, id);
        if (success) {
            const favs = [...getFavs(), id];
            setFavs(favs);
            showToast('École ajoutée aux favoris', 'success');
        }
    }
    
    if (success) {
        // Rafraîchit l'affichage
        applyFiltersAndSort();
        renderFavoritesList();
    }
}

// =================================================================================
// --- INITIALISATION ---
// =================================================================================

async function initializeApp() {
    console.log('Initialisation de EazySkool avec API...');
    
    // Charge les données depuis l'API
    ecoleData = await loadSchoolsFromAPI();
    
    // Initialise l'affichage
    applyFiltersAndSort();
    updateUserInfo();
    
    // Charge les événements
    const events = await loadEventsFromAPI();
    console.log(`${events.length} événements chargés`);
    
    showToast('Application chargée avec succès !', 'success');
}

// =================================================================================
// --- ÉVÉNEMENTS ---
// =================================================================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM chargé, initialisation...');
    
    // Initialise l'application
    initializeApp();
    
    // Gestionnaires d'événements pour la navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const section = this.getAttribute('data-section');
            showSection(`section-${section}`);
            
            if (section === 'favorites') {
                renderFavoritesList();
            }
        });
    });
    
    // Gestionnaire de recherche
    const searchForm = document.getElementById('school-search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            applyFiltersAndSort();
        });
    }
    
    // Gestionnaire de tri
    const sortSelect = document.getElementById('sort-by');
    if (sortSelect) {
        sortSelect.addEventListener('change', applyFiltersAndSort);
    }
    
    // Gestionnaire de réinitialisation
    const resetBtn = document.getElementById('school-search-reset');
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            document.getElementById('school-search-input').value = '';
            applyFiltersAndSort();
        });
    }
    
    // Gestionnaires des modales
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        const closeBtn = modal.querySelector('.modal-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => closeModal(modal));
        }
        
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal(this);
            }
        });
    });
    
    // Gestionnaires d'authentification
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;
            
            try {
                const user = await loginUser(email, password);
                setCurrentUser(user);
                updateUserInfo();
                closeModal(document.getElementById('modal-login'));
                showToast('Connexion réussie !', 'success');
            } catch (error) {
                showToast(error.message, 'error');
            }
        });
    }
    
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const email = document.getElementById('register-email').value;
            const password = document.getElementById('register-password').value;
            
            try {
                await registerUser({ email, password });
                closeModal(document.getElementById('modal-register'));
                showToast('Compte créé avec succès !', 'success');
            } catch (error) {
                showToast(error.message, 'error');
            }
        });
    }
    
    // Gestionnaires des boutons d'ouverture de modales
    const openLoginBtn = document.getElementById('open-login-btn-account');
    if (openLoginBtn) {
        openLoginBtn.addEventListener('click', () => openModal(document.getElementById('modal-login')));
    }
    
    const openRegisterBtn = document.getElementById('open-register-btn-account');
    if (openRegisterBtn) {
        openRegisterBtn.addEventListener('click', () => openModal(document.getElementById('modal-register')));
    }
    
    // Gestionnaires de switch entre login/register
    const switchToRegister = document.getElementById('switch-to-register');
    if (switchToRegister) {
        switchToRegister.addEventListener('click', function() {
            closeModal(document.getElementById('modal-login'));
            openModal(document.getElementById('modal-register'));
        });
    }
    
    const switchToLogin = document.getElementById('switch-to-login');
    if (switchToLogin) {
        switchToLogin.addEventListener('click', function() {
            closeModal(document.getElementById('modal-register'));
            openModal(document.getElementById('modal-login'));
        });
    }
    
    console.log('Événements initialisés');
});

console.log('Script API chargé'); 