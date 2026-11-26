const KEY = 'noel2026';
const STATUSES = ['À trouver', 'Sélectionné', 'Commandé', 'Reçu', 'Emballé'];
const COMMITTED_STATUSES = ['Commandé', 'Reçu', 'Emballé'];
const PAGE_SIZE = 36;

const CATEGORIES = [
  { key: 'Tous', label: '✨ Tous', icon: '🎁' },
  { key: 'High-tech et électronique', label: '📱 High-tech et électronique', icon: '📱' },
  { key: 'Maison et décoration', label: '🏡 Maison et décoration', icon: '🏡' },
  { key: 'Beauté et soins', label: '💄 Beauté et soins', icon: '💄' },
  { key: 'Mode et accessoires', label: '👜 Mode et accessoires', icon: '👜' },
  { key: 'Bijoux', label: '💎 Bijoux', icon: '💎' },
  { key: 'Livres', label: '📚 Livres', icon: '📚' },
  { key: 'Jeux de société', label: '🎲 Jeux de société', icon: '🎲' },
  { key: 'Jouets et jeux pour enfants', label: '🧸 Jouets et jeux pour enfants', icon: '🧸' },
  { key: 'Loisirs créatifs', label: '🎨 Loisirs créatifs', icon: '🎨' },
  { key: 'Sport et bien-être', label: '🧘 Sport et bien-être', icon: '🧘' },
  { key: 'Jardinage', label: '🌱 Jardinage', icon: '🌱' },
  { key: 'Gastronomie et gourmandises', label: '🍫 Gastronomie et gourmandises', icon: '🍫' },
  { key: 'Produits artisanaux', label: '🏺 Produits artisanaux', icon: '🏺' },
  { key: 'Cadeaux originaux et personnalisés', label: '🎀 Cadeaux originaux et personnalisés', icon: '🎀' }
];

let data = loadData();
let catalogProducts = [];
let catalogUpdatedAt = '';
let currentCategory = 'Tous';
let visibleCatalogLimit = PAGE_SIZE;
let pendingCatalogProduct = null;

function normalizeSearch(str) {
  return String(str || '')
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '');
}

function sanitizeHttpUrl(rawUrl) {
  if (!rawUrl || typeof rawUrl !== 'string') return '';
  const trimmed = rawUrl.trim();
  if (!trimmed) return '';
  try {
    const parsed = new URL(trimmed);
    if (parsed.protocol === 'http:' || parsed.protocol === 'https:') {
      return parsed.href;
    }
    return '';
  } catch (e) {
    return '';
  }
}

function loadData() {
  try {
    const raw = JSON.parse(localStorage.getItem(KEY) || '{}');
    const budget = Number(raw.budget);
    const people = Array.isArray(raw.people)
      ? raw.people.map((p) => ({
          name: typeof p.name === 'string' && p.name.trim() ? p.name.trim() : 'Sans nom',
          age: p.age !== undefined && p.age !== null ? String(p.age) : '',
          taste: typeof p.taste === 'string' ? p.taste : '',
          notes: typeof p.notes === 'string' ? p.notes : '',
          budget: Number.isFinite(Number(p.budget)) ? Math.max(0, Number(p.budget)) : 0,
          gifts: Array.isArray(p.gifts)
            ? p.gifts.map((g) => ({
                name: typeof g.name === 'string' ? g.name : '',
                price: Number.isFinite(Number(g.price)) ? Math.max(0, Number(g.price)) : 0,
                status: STATUSES.includes(g.status) ? g.status : 'À trouver',
                favorite: Boolean(g.favorite),
                url: sanitizeHttpUrl(g.url || ''),
                note: typeof g.note === 'string' ? g.note : ''
              }))
            : []
        }))
      : [];

    return {
      budget: Number.isFinite(budget) ? Math.max(0, budget) : 0,
      people
    };
  } catch (e) {
    return { budget: 0, people: [] };
  }
}

function save() {
  localStorage.setItem(KEY, JSON.stringify(data));
  render();
}

function money(amount) {
  return Number(amount || 0).toLocaleString('fr-FR', {
    style: 'currency',
    currency: 'EUR'
  });
}

function formatCatalogPrice(price) {
  if (typeof price === 'number' && Number.isFinite(price) && price > 0) {
    return money(price);
  }
  return 'Prix à vérifier';
}

function spent() {
  return data.people.reduce((sum, person) => {
    const personCommitted = person.gifts
      .filter((gift) => COMMITTED_STATUSES.includes(gift.status))
      .reduce((acc, gift) => acc + (Number(gift.price) || 0), 0);
    return sum + personCommitted;
  }, 0);
}

function showPage(pageId) {
  document.querySelectorAll('.page').forEach((section) => {
    section.classList.toggle('hidden', section.id !== pageId);
  });
  document.querySelectorAll('nav button').forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.page === pageId);
  });
  if (pageId === 'ideas') {
    renderCatalog();
  }
}

document.querySelectorAll('nav button').forEach((btn) => {
  btn.addEventListener('click', () => showPage(btn.dataset.page));
});

function addPerson() {
  const nameInput = document.getElementById('pName');
  const name = nameInput.value.trim();
  if (!name) {
    alert('Merci d’indiquer un prénom.');
    nameInput.focus();
    return;
  }

  const ageRaw = document.getElementById('pAge').value.trim();
  const taste = document.getElementById('pTaste').value.trim();
  const notes = document.getElementById('pNotes').value.trim();
  const budgetVal = Math.max(0, Number(document.getElementById('pBudget').value) || 0);

  data.people.push({
    name,
    age: ageRaw,
    taste,
    notes,
    budget: budgetVal,
    gifts: []
  });

  ['pName', 'pAge', 'pTaste', 'pNotes', 'pBudget'].forEach((id) => {
    document.getElementById(id).value = '';
  });

  save();
}

function addGift(personIndex) {
  const person = data.people[personIndex];
  if (!person) return;

  const giftName = prompt('Quel cadeau envisages-tu pour ' + person.name + ' ?');
  if (!giftName || !giftName.trim()) return;

  const priceInput = prompt('Prix en euros (0 ou montant estimé) :', '0');
  if (priceInput === null) return;
  const price = Math.max(0, Number(priceInput.replace(',', '.')) || 0);

  const rawUrl = prompt('Lien vers la boutique (http/https, facultatif) :', '');
  const safeUrl = sanitizeHttpUrl(rawUrl || '');
  if (rawUrl && rawUrl.trim() && !safeUrl) {
    alert('Le lien n’a pas été enregistré car seules les adresses commençant par http:// ou https:// sont autorisées.');
  }

  const noteInput = prompt('Note personnelle (facultatif) :', '');

  person.gifts.push({
    name: giftName.trim(),
    price,
    url: safeUrl,
    status: 'À trouver',
    favorite: false,
    note: noteInput ? noteInput.trim() : ''
  });

  save();
}

function removePerson(personIndex) {
  const person = data.people[personIndex];
  if (!person) return;
  if (confirm('Supprimer « ' + person.name + ' » et tous ses cadeaux ?')) {
    data.people.splice(personIndex, 1);
    save();
  }
}

function removeGift(personIndex, giftIndex) {
  const gift = data.people[personIndex]?.gifts[giftIndex];
  if (!gift) return;
  if (confirm('Supprimer le cadeau « ' + gift.name + ' » ?')) {
    data.people[personIndex].gifts.splice(giftIndex, 1);
    save();
  }
}

function updateStatus(personIndex, giftIndex, value) {
  if (!STATUSES.includes(value)) return;
  data.people[personIndex].gifts[giftIndex].status = value;
  save();
}

function toggleFavorite(personIndex, giftIndex) {
  const gift = data.people[personIndex].gifts[giftIndex];
  gift.favorite = !gift.favorite;
  save();
}

function updateGiftNote(personIndex, giftIndex, value) {
  data.people[personIndex].gifts[giftIndex].note = value;
  localStorage.setItem(KEY, JSON.stringify(data));
}

function editPersonInfo(personIndex) {
  const person = data.people[personIndex];
  if (!person) return;

  const nextTaste = prompt('Passions et centres d’intérêt :', person.taste || '');
  if (nextTaste === null) return;

  const nextNotes = prompt('Goûts, préférences et notes personnelles :', person.notes || '');
  if (nextNotes === null) return;

  const nextBudgetRaw = prompt('Budget individuel (€) :', String(person.budget || 0));
  if (nextBudgetRaw === null) return;
  const nextBudget = Math.max(0, Number(nextBudgetRaw.replace(',', '.')) || 0);

  person.taste = nextTaste.trim();
  person.notes = nextNotes.trim();
  person.budget = nextBudget;
  save();
}

function saveBudget() {
  const raw = Number(document.getElementById('budgetInput').value);
  data.budget = Number.isFinite(raw) && raw >= 0 ? raw : 0;
  save();
}

function renderCategoryButtons() {
  const container = document.getElementById('catalogCategories');
  if (!container) return;
  container.innerHTML = '';

  const countsByCategory = {};
  catalogProducts.forEach((p) => {
    countsByCategory[p.category] = (countsByCategory[p.category] || 0) + 1;
  });

  CATEGORIES.forEach((cat) => {
    const count = cat.key === 'Tous' ? catalogProducts.length : (countsByCategory[cat.key] || 0);
    if (cat.key !== 'Tous' && count === 0) return;

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.textContent = cat.label + ' (' + count + ')';
    btn.className = currentCategory === cat.key ? 'gold' : 'light';
    btn.addEventListener('click', () => {
      currentCategory = cat.key;
      visibleCatalogLimit = PAGE_SIZE;
      renderCategoryButtons();
      renderCatalog();
    });
    container.appendChild(btn);
  });
}

function getCategoryIcon(categoryName) {
  const found = CATEGORIES.find((c) => c.key === categoryName);
  return found ? found.icon : '🎁';
}

function setCatalogBanner(message) {
  const banner = document.getElementById('catalogStatusBanner');
  if (!banner) return;
  if (!message) {
    banner.textContent = '';
    banner.classList.add('hidden');
  } else {
    banner.textContent = message;
    banner.classList.remove('hidden');
  }
}

async function loadCatalog() {
  try {
    const response = await fetch('./catalogue.json?v=' + Date.now(), { cache: 'no-store' });
    if (!response.ok) {
      throw new Error('HTTP ' + response.status);
    }
    const payload = await response.json();
    const items = Array.isArray(payload) ? payload : Array.isArray(payload.products) ? payload.products : [];
    catalogUpdatedAt = typeof payload.updated_at === 'string' ? payload.updated_at : '';

    catalogProducts = items
      .filter((item) => item && typeof item.name === 'string' && item.name.trim())
      .map((item, idx) => ({
        id: typeof item.id === 'string' && item.id.trim() ? item.id.trim() : 'cat-' + (idx + 1),
        name: item.name.trim(),
        category: typeof item.category === 'string' && item.category.trim() ? item.category.trim() : 'Cadeaux originaux et personnalisés',
        brand: typeof item.brand === 'string' && item.brand.trim() ? item.brand.trim() : 'Marque / Référence française',
        merchant: typeof item.merchant === 'string' && item.merchant.trim() ? item.merchant.trim() : 'Marché français',
        merchant_type: typeof item.merchant_type === 'string' ? item.merchant_type.trim() : '',
        description: typeof item.description === 'string' ? item.description.trim() : '',
        price: typeof item.price === 'number' && Number.isFinite(item.price) && item.price > 0 ? item.price : null,
        image: sanitizeHttpUrl(item.image || ''),
        image_license: typeof item.image_license === 'string' ? item.image_license.trim() : '',
        url: sanitizeHttpUrl(item.url || ''),
        source: typeof item.source === 'string' ? item.source.trim() : ''
      }));

    // Prioriser les fiches disposant d'une photo
    catalogProducts.sort((a, b) => Number(Boolean(b.image)) - Number(Boolean(a.image)));

    const withPhotosCount = catalogProducts.filter((p) => Boolean(p.image)).length;
    if (!catalogProducts.length) {
      setCatalogBanner('Le catalogue est vide. Exécute le workflow GitHub Actions pour remplir catalogue.json.');
    } else if (withPhotosCount === 0) {
      setCatalogBanner('⚠️ Aucune photo n’est encore enregistrée dans catalogue.json : va sur ton dépôt GitHub → onglet Actions → « Actualiser le catalogue et publier sur GitHub Pages » → Run workflow pour importer les centaines d’articles et leurs photos Open Data.');
    } else {
      setCatalogBanner('');
    }
  } catch (err) {
    catalogProducts = [];
    setCatalogBanner('Le catalogue externe n’a pas pu être chargé pour le moment. Les autres fonctionnalités (proches, cadeaux, budgets, sauvegardes) restent pleinement disponibles.');
  }

  renderCategoryButtons();
  renderCatalog();
}

function resetAndRenderCatalog() {
  visibleCatalogLimit = PAGE_SIZE;
  renderCatalog();
}

function showMoreCatalog() {
  visibleCatalogLimit += PAGE_SIZE;
  renderCatalog();
}

function renderCatalog() {
  const container = document.getElementById('productCatalog');
  const countEl = document.getElementById('catalogCount');
  const updatedEl = document.getElementById('catalogUpdatedAt');
  const loadMoreBtn = document.getElementById('loadMoreBtn');
  if (!container || !countEl) return;

  container.innerHTML = '';
  const queryNorm = normalizeSearch(document.getElementById('productSearch')?.value || '').trim();
  const onlyWithPhoto = Boolean(document.getElementById('onlyWithPhoto')?.checked);

  const filtered = catalogProducts.filter((product) => {
    if (onlyWithPhoto && !product.image) return false;
    const matchesCategory = currentCategory === 'Tous' || product.category === currentCategory;
    if (!matchesCategory) return false;
    if (!queryNorm) return true;

    const haystack = normalizeSearch(
      [
        product.name,
        product.category,
        product.brand,
        product.merchant,
        product.merchant_type,
        product.description
      ].join(' ')
    );
    return queryNorm.split(/\s+/).every((word) => haystack.includes(word));
  });

  const shown = filtered.slice(0, visibleCatalogLimit);
  const withPhotosTotal = catalogProducts.filter((p) => Boolean(p.image)).length;
  countEl.textContent =
    shown.length +
    ' affiché(s) sur ' +
    filtered.length +
    ' résultat(s) (' +
    catalogProducts.length +
    ' références · ' +
    withPhotosTotal +
    ' avec photo)';

  if (updatedEl) {
    updatedEl.textContent = catalogUpdatedAt ? 'Dernière actualisation : ' + catalogUpdatedAt : '';
  }

  if (loadMoreBtn) {
    loadMoreBtn.classList.toggle('hidden', shown.length >= filtered.length);
  }

  if (!shown.length) {
    const empty = document.createElement('p');
    empty.className = 'empty';
    empty.textContent = onlyWithPhoto
      ? 'Aucun produit avec photo ne correspond à cette recherche. Décoche « Avec photo uniquement » ou lance le workflow GitHub Actions pour importer les photos Open Data.'
      : 'Aucun produit ne correspond à ce filtre. Essaie une autre catégorie ou un autre mot-clé.';
    container.appendChild(empty);
    return;
  }

  shown.forEach((product) => {
    const card = document.createElement('article');
    card.className = 'product-card';

    const mediaBox = document.createElement('div');
    mediaBox.className = 'product-media';

    if (product.image) {
      const img = document.createElement('img');
      img.src = product.image;
      img.alt = product.name;
      img.loading = 'lazy';
      img.referrerPolicy = 'no-referrer';
      img.addEventListener('error', () => {
        const fallback = document.createElement('div');
        fallback.className = 'product-emblem';
        fallback.textContent = getCategoryIcon(product.category);
        mediaBox.innerHTML = '';
        mediaBox.appendChild(fallback);
      });
      mediaBox.appendChild(img);
    } else {
      const emblem = document.createElement('div');
      emblem.className = 'product-emblem';
      emblem.textContent = getCategoryIcon(product.category);
      mediaBox.appendChild(emblem);
    }

    card.appendChild(mediaBox);

    const info = document.createElement('div');
    info.className = 'product-info';

    const topMeta = document.createElement('div');
    topMeta.className = 'product-meta-top';

    const tag = document.createElement('span');
    tag.className = 'tag';
    tag.textContent = product.category;

    const brand = document.createElement('span');
    brand.className = 'product-brand';
    brand.textContent = product.brand;

    topMeta.append(tag, brand);

    const title = document.createElement('h3');
    title.textContent = product.name;

    const merchant = document.createElement('div');
    merchant.className = 'product-merchant';
    merchant.textContent = product.merchant_type
      ? product.merchant + ' · ' + product.merchant_type
      : product.merchant;

    const desc = document.createElement('p');
    desc.className = 'product-desc';
    desc.textContent = product.description;

    const sourceLine = document.createElement('div');
    sourceLine.className = 'product-source';
    sourceLine.textContent = product.source
      ? 'Source : ' + product.source + (product.image_license ? ' (' + product.image_license + ')' : '')
      : '';

    const priceEl = document.createElement('div');
    priceEl.className = 'product-price';
    priceEl.textContent = formatCatalogPrice(product.price);

    info.append(topMeta, title, merchant, desc, sourceLine, priceEl);

    if (product.url) {
      const link = document.createElement('a');
      link.className = 'product-link';
      link.href = product.url;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.textContent = 'Voir la fiche / le site marchand ↗';
      info.appendChild(link);
    }

    const addBtn = document.createElement('button');
    addBtn.type = 'button';
    addBtn.className = 'gold';
    addBtn.textContent = '🎁 Ajouter à mes cadeaux';
    addBtn.addEventListener('click', () => openAddGiftModal(product));

    info.appendChild(addBtn);
    card.appendChild(info);
    container.appendChild(card);
  });
}

function openAddGiftModal(product) {
  if (!data.people.length) {
    alert('Ajoute d’abord un proche dans « Mes proches » pour lui attribuer ce cadeau.');
    showPage('people');
    return;
  }

  pendingCatalogProduct = product;
  const select = document.getElementById('modalRecipient');
  select.innerHTML = '';

  data.people.forEach((person, idx) => {
    const opt = document.createElement('option');
    opt.value = String(idx);
    opt.textContent = person.name + (person.age ? ' (' + person.age + ' ans)' : '');
    select.appendChild(opt);
  });

  document.getElementById('modalGiftSubtitle').textContent =
    product.name + ' — ' + product.brand;
  document.getElementById('modalPrice').value =
    typeof product.price === 'number' && Number.isFinite(product.price) && product.price > 0 ? String(product.price) : '';
  document.getElementById('modalNote').value =
    product.merchant ? 'Enseigne / distributeur : ' + product.merchant : '';

  document.getElementById('addGiftModal').classList.remove('hidden');
}

function closeAddGiftModal() {
  pendingCatalogProduct = null;
  document.getElementById('addGiftModal').classList.add('hidden');
}

function confirmAddCatalogGift() {
  if (!pendingCatalogProduct) return;

  const recipientIdx = Number(document.getElementById('modalRecipient').value);
  const person = data.people[recipientIdx];
  if (!person) {
    alert('Merci de sélectionner un proche valide.');
    return;
  }

  const rawPrice = document.getElementById('modalPrice').value.trim();
  const parsedPrice = rawPrice === '' ? 0 : Number(rawPrice.replace(',', '.'));
  if (!Number.isFinite(parsedPrice) || parsedPrice < 0) {
    alert('Merci d’indiquer un montant valide en euros.');
    return;
  }

  const customNote = document.getElementById('modalNote').value.trim();

  person.gifts.push({
    name: pendingCatalogProduct.name,
    price: parsedPrice,
    url: sanitizeHttpUrl(pendingCatalogProduct.url || ''),
    status: 'À trouver',
    favorite: false,
    note: customNote || pendingCatalogProduct.description || ''
  });

  const addedName = pendingCatalogProduct.name;
  closeAddGiftModal();
  save();
  alert('🎁 « ' + addedName + ' » a été ajouté à la liste de ' + person.name + ' (statut : À trouver).');
  showPage('people');
}

function render() {
  const totalBudget = Number(data.budget) || 0;
  const committedAmount = spent();
  const remainingBudget = totalBudget - committedAmount;

  ['total', 'budgetTotal'].forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.textContent = money(totalBudget);
  });

  ['spent', 'budgetSpent'].forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.textContent = money(committedAmount);
  });

  ['remaining', 'budgetLeft'].forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.textContent = money(remainingBudget);
  });

  const budgetInput = document.getElementById('budgetInput');
  if (budgetInput) {
    budgetInput.value = data.budget || '';
  }

  const totalGifts = data.people.reduce((sum, p) => sum + p.gifts.length, 0);
  const wrappedGifts = data.people.reduce(
    (sum, p) => sum + p.gifts.filter((g) => g.status === 'Emballé').length,
    0
  );

  const totalGiftsEl = document.getElementById('totalGiftsCount');
  const wrappedGiftsEl = document.getElementById('wrappedGiftsCount');
  const peopleCountEl = document.getElementById('peopleCount');
  if (totalGiftsEl) totalGiftsEl.textContent = String(totalGifts);
  if (wrappedGiftsEl) wrappedGiftsEl.textContent = String(wrappedGifts);
  if (peopleCountEl) peopleCountEl.textContent = String(data.people.length);

  const progressText = document.getElementById('progressText');
  const progressBar = document.getElementById('progress');
  const progressTrack = progressBar?.parentElement;
  const pct = totalGifts ? Math.round((wrappedGifts / totalGifts) * 100) : 0;

  if (progressText) {
    progressText.textContent = totalGifts
      ? wrappedGifts + ' cadeau(x) emballé(s) sur ' + totalGifts + ' (' + pct + '%)'
      : 'Aucun cadeau enregistré.';
  }
  if (progressBar) {
    progressBar.style.width = (totalGifts ? (wrappedGifts / totalGifts) * 100 : 0) + '%';
  }
  if (progressTrack) {
    progressTrack.setAttribute('aria-valuenow', String(pct));
  }

  const peopleContainer = document.getElementById('peopleList');
  peopleContainer.innerHTML = '';

  if (!data.people.length) {
    const empty = document.createElement('div');
    empty.className = 'empty';
    empty.textContent = 'Ajoute ton premier proche ❤️';
    peopleContainer.appendChild(empty);
  }

  data.people.forEach((person, pIdx) => {
    const box = document.createElement('div');
    box.className = 'person';

    const header = document.createElement('div');
    header.className = 'person-header';

    const title = document.createElement('h3');
    title.style.margin = '0';
    title.textContent = '🎁 ' + person.name + (person.age ? ' · ' + person.age + ' ans' : '');

    const budgetBadge = document.createElement('span');
    budgetBadge.className = 'tag';
    budgetBadge.textContent = 'Budget : ' + money(person.budget);

    header.append(title, budgetBadge);

    const tasteLine = document.createElement('p');
    tasteLine.className = 'person-meta';
    tasteLine.textContent = 'Passions / centres d’intérêt : ' + (person.taste || 'Non renseigné');

    const notesLine = document.createElement('small');
    notesLine.className = 'person-notes';
    notesLine.textContent = 'Goûts & notes : ' + (person.notes || 'Aucune note');

    box.append(header, tasteLine, notesLine);

    const actions = document.createElement('div');
    actions.className = 'actions';

    const addGiftBtn = document.createElement('button');
    addGiftBtn.type = 'button';
    addGiftBtn.textContent = '+ Ajouter un cadeau';
    addGiftBtn.addEventListener('click', () => addGift(pIdx));

    const editBtn = document.createElement('button');
    editBtn.type = 'button';
    editBtn.className = 'light';
    editBtn.textContent = 'Modifier profil / budget';
    editBtn.addEventListener('click', () => editPersonInfo(pIdx));

    const delBtn = document.createElement('button');
    delBtn.type = 'button';
    delBtn.className = 'red';
    delBtn.textContent = 'Supprimer';
    delBtn.addEventListener('click', () => removePerson(pIdx));

    actions.append(addGiftBtn, editBtn, delBtn);
    box.appendChild(actions);

    person.gifts.forEach((gift, gIdx) => {
      const line = document.createElement('div');
      line.className = 'gift';

      const left = document.createElement('div');
      const giftTitle = document.createElement('strong');
      giftTitle.textContent = (gift.favorite ? '⭐ ' : '🎁 ') + gift.name;

      const giftPrice = document.createElement('div');
      giftPrice.textContent = 'Montant : ' + money(gift.price);

      left.append(giftTitle, giftPrice);

      const safeUrl = sanitizeHttpUrl(gift.url);
      if (safeUrl) {
        const link = document.createElement('a');
        link.className = 'product-link';
        link.href = safeUrl;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.textContent = 'Voir la boutique / fiche ↗';
        left.appendChild(link);
      }

      const noteInput = document.createElement('input');
      noteInput.type = 'text';
      noteInput.className = 'gift-note-input';
      noteInput.placeholder = 'Note personnelle sur ce cadeau...';
      noteInput.value = gift.note || '';
      noteInput.addEventListener('change', (e) => updateGiftNote(pIdx, gIdx, e.target.value));
      left.appendChild(noteInput);

      const right = document.createElement('div');
      right.className = 'gift-controls';

      const statusSelect = document.createElement('select');
      STATUSES.forEach((st) => {
        const opt = document.createElement('option');
        opt.value = st;
        opt.textContent = st;
        statusSelect.appendChild(opt);
      });
      statusSelect.value = gift.status;
      statusSelect.addEventListener('change', (e) => updateStatus(pIdx, gIdx, e.target.value));

      const favBtn = document.createElement('button');
      favBtn.type = 'button';
      favBtn.className = gift.favorite ? 'gold' : 'light';
      favBtn.textContent = gift.favorite ? '★ Favori' : '☆ Favori';
      favBtn.addEventListener('click', () => toggleFavorite(pIdx, gIdx));

      const delGiftBtn = document.createElement('button');
      delGiftBtn.type = 'button';
      delGiftBtn.className = 'red';
      delGiftBtn.textContent = 'Supprimer';
      delGiftBtn.addEventListener('click', () => removeGift(pIdx, gIdx));

      right.append(statusSelect, favBtn, delGiftBtn);
      line.append(left, right);
      box.appendChild(line);
    });

    peopleContainer.appendChild(box);
  });

  const dashList = document.getElementById('dashboardList');
  dashList.innerHTML = '';
  if (!data.people.length) {
    const p = document.createElement('p');
    p.className = 'muted-text';
    p.textContent = 'Aucun proche ajouté pour le moment.';
    dashList.appendChild(p);
  } else {
    data.people.forEach((person) => {
      const wrapped = person.gifts.filter((g) => g.status === 'Emballé').length;
      const recordedTotal = person.gifts.reduce((acc, g) => acc + (Number(g.price) || 0), 0);
      const line = document.createElement('p');
      line.className = 'person-meta';
      line.textContent =
        '🎁 ' +
        person.name +
        ' : ' +
        person.gifts.length +
        ' cadeau(x) (' +
        wrapped +
        ' emballé(s)) · Prévu : ' +
        money(recordedTotal) +
        ' / Budget : ' +
        money(person.budget);
      dashList.appendChild(line);
    });
  }

  const budgetPeople = document.getElementById('budgetPeople');
  budgetPeople.innerHTML = '';
  if (!data.people.length) {
    const p = document.createElement('p');
    p.className = 'muted-text';
    p.textContent = 'Ajoute des proches pour voir la répartition par personne.';
    budgetPeople.appendChild(p);
  } else {
    data.people.forEach((person) => {
      const recordedSum = person.gifts.reduce((acc, g) => acc + (Number(g.price) || 0), 0);
      const committedSum = person.gifts
        .filter((g) => COMMITTED_STATUSES.includes(g.status))
        .reduce((acc, g) => acc + (Number(g.price) || 0), 0);
      const row = document.createElement('div');
      row.className = 'budget-person-row';
      row.textContent =
        person.name +
        ' · Budget : ' +
        money(person.budget) +
        ' · Enregistré : ' +
        money(recordedSum) +
        ' · Engagé : ' +
        money(committedSum);
      budgetPeople.appendChild(row);
    });
  }

  renderCatalog();
}

function exportData() {
  const payload = JSON.stringify(data, null, 2);
  const blob = new Blob([payload], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'mon-noel-organise.json';
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function importData() {
  const fileInput = document.getElementById('importFile');
  const file = fileInput.files && fileInput.files[0];
  if (!file) {
    alert('Merci de choisir un fichier de sauvegarde JSON.');
    return;
  }

  const reader = new FileReader();
  reader.onload = () => {
    try {
      const parsed = JSON.parse(String(reader.result || ''));
      if (!parsed || !Array.isArray(parsed.people) || typeof parsed.budget !== 'number') {
        throw new Error('Format invalide');
      }
      if (confirm('Remplacer les données actuelles par cette sauvegarde ?')) {
        localStorage.setItem(KEY, JSON.stringify(parsed));
        data = loadData();
        render();
        fileInput.value = '';
        alert('Sauvegarde importée avec succès !');
      }
    } catch (e) {
      alert('Ce fichier ne semble pas être une sauvegarde JSON valide de Mon Noël organisé.');
    }
  };
  reader.readAsText(file);
}

function clearData() {
  if (confirm('Effacer définitivement toutes tes données enregistrées dans ce navigateur ?')) {
    data = { budget: 0, people: [] };
    save();
  }
}

document.getElementById('addGiftModal')?.addEventListener('click', (e) => {
  if (e.target.id === 'addGiftModal') {
    closeAddGiftModal();
  }
});

render();
loadCatalog();
