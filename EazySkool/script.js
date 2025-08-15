// =================================================================================
// EazySkool - script.js
// Logique principale de l'application
// =================================================================================

// --- DONNÉES : Liste des écoles du Grand Est ---
const ECOLES_GRAND_EST = [
  {
    id: 1,
    nom: "Université de Strasbourg",
    ville: "Strasbourg",
    type: "Université",
    description: "L'Université de Strasbourg est l'une des plus grandes universités de France, reconnue pour la qualité de son enseignement et de sa recherche.",
    avis: 4.6,
    photo: "images/strasbourg.jpg",
    coords: [48.5839, 7.7455],
    contact: {
      email: "contact@unistra.fr",
      tel: "03 68 85 00 00",
      site: "https://www.unistra.fr/"
    }
  },
  {
    id: 2,
    nom: "Université de Lorraine",
    ville: "Nancy",
    type: "Université",
    description: "L'Université de Lorraine propose une offre de formation complète et innovante dans de nombreux domaines.",
    avis: 4.3,
    photo: "images/strasbourg.jpg",
    coords: [48.6921, 6.1844],
    contact: {
      email: "contact@univ-lorraine.fr",
      tel: "03 72 74 00 00",
      site: "https://www.univ-lorraine.fr/"
    }
  },
  {
    id: 3,
    nom: "ICN Business School",
    ville: "Nancy",
    type: "École de commerce",
    description: "ICN Business School est une grande école de management reconnue internationalement.",
    avis: 4.5,
    photo: "images/strasbourg.jpg",
    coords: [48.6937, 6.1843],
    contact: {
      email: "contact@icn-artem.com",
      tel: "03 54 50 25 00",
      site: "https://www.icn-artem.com/"
    }
  },
  {
    id: 4,
    nom: "Sciences Po Strasbourg",
    ville: "Strasbourg",
    type: "Institut d'études politiques",
    description: "Sciences Po Strasbourg forme les futurs cadres de la fonction publique et du secteur privé.",
    avis: 4.7,
    photo: "images/strasbourg.jpg",
    coords: [48.5846, 7.7616],
    contact: {
      email: "contact@sciencespo-strasbourg.fr",
      tel: "03 68 85 84 00",
      site: "https://www.sciencespo-strasbourg.fr/"
    }
  },
  {
    id: 5,
    nom: "Université de Haute-Alsace",
    ville: "Mulhouse",
    type: "Université",
    description: "L'Université de Haute-Alsace est reconnue pour ses formations en sciences, technologies et ingénierie.",
    avis: 4.2,
    photo: "images/strasbourg.jpg",
    coords: [47.7508, 7.3359],
    contact: {
      email: "contact@uha.fr",
      tel: "03 89 33 64 00",
      site: "https://www.uha.fr/"
    }
  }
];

// --- VARIABLES GLOBALES ET CONSTANTES ---
const SCHOOLS_PER_PAGE = 6;
let currentPage = 1;
let ecoleData = []; // La liste des écoles actuellement affichées (filtrées/triées)
let modalMap = null;
let modalMarkers = [];

// =================================================================================
// --- FONCTIONS GLOBALES (HELPERS) ---
// Ces fonctions ne manipulent pas le DOM et peuvent être appelées de n'importe où.
// =================================================================================

// --- Helpers pour l'Authentification ---
function getUsers() { return JSON.parse(localStorage.getItem('eazyskool_users') || '{}'); }
function setUsers(users) { localStorage.setItem('eazyskool_users', JSON.stringify(users)); }
function getCurrentUser() { return localStorage.getItem('eazyskool_current_user'); }
function setCurrentUser(email) { if(email) localStorage.setItem('eazyskool_current_user', email); else localStorage.removeItem('eazyskool_current_user'); }
function logout() { setCurrentUser(null); }

// --- Helpers pour les Favoris ---
function getFavs() { return JSON.parse(localStorage.getItem('eazyskool_favs') || '[]'); }
function setFavs(favs) { localStorage.setItem('eazyskool_favs', JSON.stringify(favs)); }
function isFav(id) { return getFavs().includes(id); }

// --- Helpers pour les Images ---
function getEcoleImages(ecole) {
  if (Array.isArray(ecole.photos)) return ecole.photos;
  if (ecole.photo) return [ecole.photo];
  return [];
}

// =================================================================================
// --- INITIALISATION DE L'APPLICATION ---
// Le code ne s'exécute que lorsque le DOM est entièrement chargé.
// =================================================================================

document.addEventListener('DOMContentLoaded', function() {

  // --- SÉLECTION DE TOUS LES ÉLÉMENTS DU DOM ---
  const splash = document.getElementById('splash-screen');
  const navLinks = document.querySelectorAll('.nav-link');
  const spaSections = document.querySelectorAll('.spa-section');
  const userInfo = document.getElementById('user-info');
  // Modales
  const modalLogin = document.getElementById('modal-login');
  const modalRegister = document.getElementById('modal-register');
  const schoolModal = document.getElementById('school-modal');
  const schoolModalBody = document.getElementById('school-modal-body');
  const mapModal = document.getElementById('map-modal');
  // Formulaires
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');
  const searchForm = document.getElementById('school-search-form');
  // Boutons
  const openLoginBtnAccount = document.getElementById('open-login-btn-account');
  const openRegisterBtnAccount = document.getElementById('open-register-btn-account');
  const closeLogin = document.getElementById('close-login');
  const closeRegister = document.getElementById('close-register');
  const switchToRegister = document.getElementById('switch-to-register');
  const switchToLogin = document.getElementById('switch-to-login');
  const closeSchoolModal = document.getElementById('close-school-modal');
  const mapWidgetHeader = document.querySelector('#map-widget h3');
  const openBigMapBtn = document.getElementById('open-big-map');
  const closeMapModal = document.getElementById('close-map-modal');
  const sortBy = document.getElementById('sort-by');
  const resetFiltersBtn = document.getElementById('reset-filters');
  // Conteneurs
  const schoolsList = document.getElementById('schools-list');
  const paginationContainer = document.getElementById('pagination-container');
  const favoritesList = document.getElementById('favorites-list');


  // =================================================================================
  // --- FONCTIONS PRINCIPALES (manipulent le DOM) ---
  // =================================================================================

  function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    let icon = 'fa-solid fa-circle-info';
    if (type === 'success') icon = 'fa-solid fa-check-circle';
    if (type === 'error') icon = 'fa-solid fa-times-circle';
    toast.innerHTML = `<i class="${icon}"></i> ${message}`;
    toastContainer.appendChild(toast);
    setTimeout(() => { toast.remove(); }, 4000);
  }

  function openModal(modal) { if(modal) modal.style.display = 'flex'; }
  function closeModal(modal) { if(modal) modal.style.display = 'none'; }

  function showSection(sectionId) {
    spaSections.forEach(sec => {
      sec.style.display = (sec.id === 'section-' + sectionId) ? '' : 'none';
    });
    navLinks.forEach(link => {
      link.classList.toggle('active', link.dataset.section === sectionId);
    });
  }

  function updateUserInfo() {
    const email = getCurrentUser();
    if (email) {
      userInfo.innerHTML = `<span style='color:var(--primary);font-weight:600'><i class='fa-solid fa-user'></i> ${email}</span> <button class='btn btn-secondary' id='logout-btn' style='margin-left:10px;'><i class="fa-solid fa-right-from-bracket"></i></button>`;
      userInfo.style.display = 'flex';
      const logoutBtn = document.getElementById('logout-btn');
      if (logoutBtn) logoutBtn.onclick = () => {
        logout();
        updateUserInfo();
        showSection('home');
        showToast('Vous avez été déconnecté.', 'info');
      };
    } else {
      userInfo.style.display = 'none';
    }
  }

  function renderSchoolsListTo(list, container) {
    if (!container) {
      console.error('[EazySkool] Container non trouvé pour l\'affichage des écoles');
      return;
    }
    if (!list || list.length === 0) {
      container.innerHTML = `<div class="empty-state"><i class="fa-solid fa-magnifying-glass"></i><h3>Aucun résultat</h3><p>Essayez de modifier vos filtres.</p></div>`;
      console.warn('[EazySkool] Liste des écoles vide');
      return;
    }
    console.log('[EazySkool] Affichage de', list.length, 'écoles');
    container.innerHTML = list.map(ecole => {
      const images = getEcoleImages(ecole);
      return `
      <div class="school-card big-card">
        <div class="school-card-header">
          <div class="school-card-slider"><div class="slider-wrapper">
            ${images.map((img, idx) => `<img src="${img}" alt="${ecole.nom}" class="slider-img${idx === 0 ? ' active' : ''}" />`).join('')}
            <span class="badge badge-ville badge-ville-on-img" data-ville="${ecole.ville}"><i class="fa-solid fa-location-dot"></i> ${ecole.ville}</span>
          </div></div>
          <h3 class="school-card-title">${ecole.nom}</h3>
        </div>
        <div class="school-card-body">
          <div class="school-card-meta"><span class="badge badge-type"><i class="fa-solid fa-graduation-cap"></i> ${ecole.type}</span></div>
          <div class="school-card-desc">${ecole.description}</div>
          <div class="school-card-avis"><i class="fa-solid fa-star" style="color:gold;"></i> ${ecole.avis} / 5</div>
          <div class="school-card-actions">
            <button class="btn btn-secondary btn-fav" data-id="${ecole.id}"><i class="fa-solid fa-heart${isFav(ecole.id) ? ' text-danger' : ''}"></i> Favoris</button>
            <button class="btn btn-primary btn-details" data-id="${ecole.id}"><i class="fa-solid fa-circle-info"></i> Voir détails</button>
          </div>
        </div>
      </div>`;
    }).join('');
  }

  function renderFavoritesList() {
    if (!favoritesList) return;
    const favs = getFavs();
    if (favs.length === 0) {
      favoritesList.innerHTML = `<div class="empty-state"><i class="fa-regular fa-star"></i><h3>Aucun favori</h3><p>Cliquez sur le coeur d'une école pour l'ajouter.</p></div>`;
      return;
    }
    const favSchools = ECOLES_GRAND_EST.filter(school => favs.includes(school.id));
    renderSchoolsListTo(favSchools, favoritesList);
  }

  function openSchoolModal(schoolId) {
    if (!schoolModal || !schoolModalBody) return;
    const ecole = ECOLES_GRAND_EST.find(e => e.id === schoolId);
    if (!ecole) return;
    schoolModalBody.innerHTML = `
      <div class="school-modal-title">${ecole.nom}</div>
      <p>${ecole.description}</p>
      <p><strong>Avis:</strong> ${ecole.avis} / 5</p>`;
    openModal(schoolModal);
  }

  function openMapModal() {
    console.log('[EazySkool] openMapModal triggered.');
    if (!mapModal) {
      console.error('[EazySkool] The map modal element (#map-modal) was not found in the DOM.');
      return;
    }
    openModal(mapModal);
    setTimeout(() => {
      if (!modalMap) {
        console.log('[EazySkool] Initializing the large map for the first time.');
        initModalMap();
      } else {
        console.log('[EazySkool] Refreshing the existing large map.');
        modalMap.invalidateSize();
        updateModalMapMarkers();
      }
    }, 10);
  }

  // --- Initialisation de la grande carte dans la modale ---
  function initModalMap() {
    const modalMapDiv = document.getElementById('modal-map');
    if (!modalMapDiv) return;
    modalMap = L.map(modalMapDiv, { zoomControl: true });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      minZoom: 5,
    }).addTo(modalMap);
    updateModalMapMarkers();
  }

  function updateModalMapMarkers() {
    if (!modalMap) return;
    if (modalMarkers && modalMarkers.length) {
      modalMarkers.forEach(m => modalMap.removeLayer(m));
    }
    modalMarkers = [];

    const markerData = ECOLES_GRAND_EST.filter(ecole => ecole.coords);

    if (markerData.length === 0) return;

    markerData.forEach(ecole => {
      const marker = L.marker(ecole.coords);
      marker.bindPopup(`<b>${ecole.nom}</b><br>${ecole.ville}`);
      modalMarkers.push(marker);
    });

    const featureGroup = L.featureGroup(modalMarkers).addTo(modalMap);
    modalMap.fitBounds(featureGroup.getBounds().pad(0.1));
  }

  // --- Appel de l'init de la carte au chargement ---
  setTimeout(() => {
    try {
      // initMap(); // Supprimé
    } catch (e) {
      console.error('Erreur lors de l\'initialisation de la carte :', e);
    }
  }, 500);

  function toggleFavAndRefresh(id) {
    let favs = getFavs();
    if (favs.includes(id)) {
      favs = favs.filter(f => f !== id);
    } else {
      favs.push(id);
    }
    setFavs(favs);
    // Rafraîchir toutes les listes potentiellement visibles
    applyFiltersAndSort(); 
    renderFavoritesList();
  }


  // =================================================================================
  // --- ÉVÉNEMENTS ---
  // =================================================================================

  // --- Navigation principale ---
  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      showSection(link.dataset.section);
    });
  });

  // --- Modales d'authentification ---
  if (openLoginBtnAccount) openLoginBtnAccount.addEventListener('click', () => openModal(modalLogin));
  if (openRegisterBtnAccount) openRegisterBtnAccount.addEventListener('click', () => openModal(modalRegister));
  if (closeLogin) closeLogin.addEventListener('click', () => closeModal(modalLogin));
  if (closeRegister) closeRegister.addEventListener('click', () => closeModal(modalRegister));
  if (switchToRegister) switchToRegister.addEventListener('click', () => { closeModal(modalLogin); openModal(modalRegister); });
  if (switchToLogin) switchToLogin.addEventListener('click', () => { closeModal(modalRegister); openModal(modalLogin); });

  // --- Formulaires ---
  if (loginForm) loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = e.target.email.value;
    const password = e.target.password.value;
    let users = getUsers();
    if (users[email] && users[email].password === password) {
      setCurrentUser(email);
      updateUserInfo();
      closeModal(modalLogin);
      showSection('account');
      showToast('Connexion réussie !', 'success');
    } else {
      showToast('Email ou mot de passe incorrect.', 'error');
    }
  });
  if (registerForm) registerForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = e.target.email.value;
    const password = e.target.password.value;
    let users = getUsers();
    if (users[email]) {
      showToast('Cet utilisateur existe déjà.', 'error');
    } else {
      users[email] = { password };
      setUsers(users);
      setCurrentUser(email);
      updateUserInfo();
      closeModal(modalRegister);
      showSection('account');
      showToast('Compte créé avec succès !', 'success');
    }
  });

  // --- Clics délégués pour les éléments dynamiques ---
  document.body.addEventListener('click', function(e) {
    const detailsButton = e.target.closest('.btn-details');
    if (detailsButton) {
      openSchoolModal(parseInt(detailsButton.dataset.id));
      return;
    }
    const favButton = e.target.closest('.btn-fav');
    if (favButton) {
      toggleFavAndRefresh(parseInt(favButton.dataset.id));
      return;
    }
  });
  
  // --- Autres événements ---
  if (closeSchoolModal) closeSchoolModal.addEventListener('click', () => closeModal(schoolModal));
  if (mapWidgetHeader) {
    mapWidgetHeader.addEventListener('click', openMapModal);
  } else {
    console.error('[EazySkool] L\'en-tête du widget de carte n\'a pas été trouvé.');
  }
  if (openBigMapBtn) {
    openBigMapBtn.addEventListener('click', () => {
      console.log('Bouton "Voir la carte" cliqué !');
      openMapModal();
    });
  } else {
    console.error('[EazySkool] Le bouton pour ouvrir la grande carte n\'a pas été trouvé.');
  }
  if (closeMapModal) closeMapModal.addEventListener('click', () => closeModal(mapModal));
  window.addEventListener('click', function(event) {
    if (event.target === modalLogin) closeModal(modalLogin);
    if (event.target === modalRegister) closeModal(modalRegister);
    if (event.target === schoolModal) closeModal(schoolModal);
    if (event.target === mapModal) closeModal(mapModal);
  });

  const scrollToTopBtn = document.getElementById('scroll-to-top');
  if(scrollToTopBtn) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 300) {
        scrollToTopBtn.classList.add('show');
      } else {
        scrollToTopBtn.classList.remove('show');
      }
    });
    scrollToTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // --- Filtres et Recherche (temporairement désactivés pour la stabilité) ---
  function applyFiltersAndSort() {
     renderSchoolsListTo(ECOLES_GRAND_EST, schoolsList);
  }
  function renderFavoritesList() {
    // A remplir
  }


  // =================================================================================
  // --- INITIALISATION DE LA PAGE ---
  // =================================================================================
  // Splash screen : on le masque toujours après 1s, même si erreur JS
  if (splash) {
    setTimeout(() => {
      splash.classList.add('hide');
      setTimeout(() => { splash.style.display = 'none'; }, 500);
    }, 1000);
  }
  updateUserInfo();
  renderSchoolsListTo(ECOLES_GRAND_EST, schoolsList);
  renderFavoritesList();
  showSection('home');
}); 