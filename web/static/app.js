const API = '/api';
const POPULAR = ['Garen', 'Darius', 'Yasuo', 'Lux', 'Zed', 'Ahri', 'Sett', 'Mordekaiser', 'Thresh', 'Jinx'];

let allChampions = [];
let searchTimer = null;

const $ = (sel) => document.querySelector(sel);

function highlightTip(text) {
  return text.replace(
    /(THE KEY ABILITY|NEVER|DON'T|Don't stand|don't stand)/gi,
    '<strong>$1</strong>'
  );
}

function championChip(champ, onClick) {
  const btn = document.createElement('button');
  btn.className = 'champion-chip';
  btn.innerHTML = `<img src="${champ.image_url}" alt="${champ.name}" /><span>${champ.name}</span>`;
  btn.onclick = onClick;
  return btn;
}

async function loadChampions(search) {
  const url = search ? `${API}/champions?search=${encodeURIComponent(search)}` : `${API}/champions`;
  const res = await fetch(url);
  return res.json();
}

function renderPopular() {
  const grid = $('#popular-grid');
  grid.innerHTML = '';
  POPULAR.forEach((name) => {
    const champ = allChampions.find((c) => c.name.toLowerCase() === name.toLowerCase());
    if (champ) grid.appendChild(championChip(champ, () => showGuide(champ.id)));
  });
}

function showSearchResults(champions) {
  const popular = $('#popular-section');
  const results = $('#results-grid');
  const hint = $('#empty-hint');
  if (champions.length === 0) {
    popular.style.display = 'none';
    results.style.display = 'none';
    hint.textContent = 'No champions found.';
    hint.style.display = 'block';
    return;
  }
  hint.style.display = 'none';
  popular.style.display = 'none';
  results.style.display = 'grid';
  results.innerHTML = '';
  champions.forEach((c) => results.appendChild(championChip(c, () => showGuide(c.id))));
}

function showSearchView() {
  $('#search-view').style.display = 'block';
  $('#guide-view').style.display = 'none';
  $('#search-input').value = '';
  $('#popular-section').style.display = 'block';
  $('#results-grid').style.display = 'none';
  $('#empty-hint').style.display = 'block';
  $('#empty-hint').textContent = 'Search any champion to see counter picks and ability tips.';
}

async function showGuide(championId) {
  $('#search-view').style.display = 'none';
  const view = $('#guide-view');
  view.style.display = 'block';
  view.innerHTML = '<div class="loading">Loading matchup guide…</div>';
  try {
    const res = await fetch(`${API}/counter/${encodeURIComponent(championId)}`);
    if (!res.ok) throw new Error('Champion not found');
    const guide = await res.json();
    view.innerHTML = renderGuide(guide);
    view.querySelector('.back-btn').onclick = showSearchView;
    window.scrollTo(0, 0);
  } catch (e) {
    view.innerHTML = `<div class="error">${e.message}</div>`;
  }
}

function renderGuide(guide) {
  const { champion } = guide;
  const tags = champion.tags.map((t) => `<span class="tag">${t}</span>`).join('');
  let html = `<div class="guide"><button class="back-btn">← Back to search</button>
    <div class="hero"><img src="${champion.image_url}" alt="${champion.name}" />
    <div class="hero-info"><h2>vs ${champion.name}${guide.has_curated_guide ? '<span class="badge">Guide</span>' : ''}</h2>
    <div class="title">${champion.title}</div><div class="tags">${tags}</div></div></div>
    <div class="summary">${guide.summary}</div>`;
  if (guide.counter_picks.length) {
    html += `<section class="section"><h3 class="section-title">Counter Picks</h3>`;
    guide.counter_picks.forEach((c) => {
      html += `<div class="counter-card"><div class="name">${c.champion}</div><div class="role">${c.role}</div><div class="reason">${c.reason}</div></div>`;
    });
    html += `</section>`;
  }
  html += `<section class="section"><h3 class="section-title">Abilities to Respect</h3>`;
  guide.ability_tips.forEach((a) => {
    html += `<div class="ability-card"><div class="ability-header"><span class="ability-key">${a.key}</span><span class="ability-name">${a.name}</span></div><div class="ability-tip">${highlightTip(a.tip)}</div></div>`;
  });
  html += `</section>`;
  if (guide.laning_tips.length) {
    html += `<section class="section"><h3 class="section-title">Laning Tips</h3><ul class="tip-list">`;
    guide.laning_tips.forEach((t) => { html += `<li>${t}</li>`; });
    html += `</ul></section>`;
  }
  if (guide.power_spikes.length) {
    html += `<section class="section"><h3 class="section-title">Power Spikes</h3><ul class="tip-list">`;
    guide.power_spikes.forEach((t) => { html += `<li>${t}</li>`; });
    html += `</ul></section>`;
  }
  if (guide.items_to_consider.length) {
    html += `<section class="section"><h3 class="section-title">Items to Consider</h3><div class="item-pills">`;
    guide.items_to_consider.forEach((item) => { html += `<span class="item-pill">${item}</span>`; });
    html += `</div></section>`;
  }
  html += `</div>`;
  return html;
}

async function init() {
  allChampions = await loadChampions();
  renderPopular();
  $('#search-input').addEventListener('input', (e) => {
    clearTimeout(searchTimer);
    const q = e.target.value.trim();
    if (!q) {
      $('#popular-section').style.display = 'block';
      $('#results-grid').style.display = 'none';
      $('#empty-hint').style.display = 'block';
      $('#empty-hint').textContent = 'Search any champion to see counter picks and ability tips.';
      return;
    }
    searchTimer = setTimeout(async () => showSearchResults(await loadChampions(q)), 200);
  });
}

init();
