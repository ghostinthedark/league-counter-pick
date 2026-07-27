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

/* ── Analytics: derive scores from existing data ── */

function deriveThreatLevel(ability) {
  const tip = (ability.tip || '').toLowerCase();
  const key = (ability.key || '').toUpperCase();

  if (/the key ability|critical|most important|never stand|don't stay|hard counter/i.test(tip)) {
    return { score: 92, tier: 'critical' };
  }
  if (/never|don't|avoid|respect|deadly|execute|kill range|all-in|burst/i.test(tip)) {
    return { score: 78, tier: 'high' };
  }
  if (key === 'R') return { score: 80, tier: 'high' };
  if (key === 'E' || key === 'Q') return { score: 62, tier: 'medium' };
  if (key === 'W') return { score: 48, tier: 'low' };
  return { score: 40, tier: 'low' };
}

function deriveCounterScore(index, total) {
  const base = 85 - index * 6;
  return Math.max(55, Math.min(95, base));
}

function deriveMatchupDifficulty(guide) {
  const tips = (guide.laning_tips || []).join(' ').toLowerCase();
  const summary = (guide.summary || '').toLowerCase();
  const combined = tips + ' ' + summary;

  if (/very strong|hard to|difficult|snowball|unkillable|never fight|don't fight|deadly|punish/i.test(combined)) {
    return { level: 'hard', label: 'Hard', pct: 90 };
  }
  if (/short trades|respect|careful|poke|kite|dodge/i.test(combined)) {
    return { level: 'medium', label: 'Medium', pct: 60 };
  }
  if (/easy|simple|immobile|no escape|easy to gank|punish when/i.test(combined)) {
    return { level: 'easy', label: 'Easy', pct: 30 };
  }
  return guide.has_full_guide
    ? { level: 'medium', label: 'Medium', pct: 60 }
    : { level: 'medium', label: 'Medium', pct: 50 };
}

function guideBadge(guide) {
  if (guide.is_premium_guide) {
    return '<span class="badge badge--premium">Premium Guide</span>';
  }
  if (guide.has_full_guide) {
    return '<span class="badge badge--full">Full Guide</span>';
  }
  return '';
}

function parsePowerSpikeLevel(text) {
  const m = text.match(/level\s*(\d+)/i);
  if (m) return parseInt(m[1], 10);
  if (/first item|first back/i.test(text)) return 7;
  if (/two item|2 item/i.test(text)) return 11;
  if (/late|scale/i.test(text)) return 16;
  return null;
}

function deriveSpikeIntensity(text, index) {
  let intensity = 50 + index * 12;
  if (/execute|kill|deadly|unkillable|monster/i.test(text)) intensity += 20;
  if (/first item|spike/i.test(text)) intensity += 10;
  return Math.min(100, intensity);
}

/* ── Graph renderers ── */

function renderDifficultyGauge(difficulty) {
  return `<div class="difficulty-gauge">
    <div class="difficulty-gauge__header">
      <span class="difficulty-gauge__label">Matchup Difficulty</span>
      <span class="difficulty-gauge__value ${difficulty.level}">${difficulty.label}</span>
    </div>
    <div class="difficulty-gauge__track">
      <div class="difficulty-gauge__fill ${difficulty.level}" style="width:${difficulty.pct}%"></div>
    </div>
    <div class="difficulty-gauge__markers">
      <span>Easy</span><span>Medium</span><span>Hard</span>
    </div>
  </div>`;
}

function renderCounterBar(score) {
  return `<div class="counter-bar">
    <div class="counter-bar__label">
      <span>Counter effectiveness</span>
      <span>${score}%</span>
    </div>
    <div class="counter-bar__track">
      <div class="counter-bar__fill" style="width:${score}%"></div>
    </div>
  </div>`;
}

function renderThreatMeter(threat) {
  return `<div class="threat-meter">
    <div class="threat-meter__track">
      <div class="threat-meter__fill ${threat.tier}" style="width:${threat.score}%"></div>
    </div>
    <span class="threat-meter__label ${threat.tier}">${threat.tier}</span>
  </div>`;
}

function renderSpikeTimeline(spikes) {
  if (!spikes.length) return '';
  const bars = spikes.slice(0, 5).map((text, i) => {
    const level = parsePowerSpikeLevel(text);
    const intensity = deriveSpikeIntensity(text, i);
    const barHeight = Math.max(16, Math.min(58, Math.round(18 + intensity * 0.42)));
    return `<div class="spike-bar">
      <div class="spike-bar__track">
        <div class="spike-bar__col" style="height:${barHeight}px"></div>
      </div>
      ${level ? `<span class="spike-bar__level">Lv ${level}</span>` : ''}
      <span class="spike-bar__label">${text}</span>
    </div>`;
  }).join('');

  return `<div class="spike-timeline">
    <div class="spike-timeline__chart">${bars}</div>
  </div>`;
}

function renderLoadingSkeleton() {
  return `<div class="loading-skeleton">
    <div class="skeleton skeleton-hero"></div>
    <div class="skeleton skeleton-bar medium"></div>
    <div class="skeleton skeleton-bar short"></div>
    <div class="skeleton skeleton-card"></div>
    <div class="skeleton skeleton-card"></div>
    <div class="skeleton skeleton-card"></div>
  </div>`;
}

/* ── Champion chips ── */

function championChip(champ, onClick) {
  const btn = document.createElement('button');
  btn.className = 'champion-chip';
  btn.innerHTML = `
    <img class="champion-chip__portrait" src="${champ.image_url}" alt="${champ.name}" loading="lazy" />
    <span>${champ.name}</span>`;
  btn.onclick = onClick;
  return btn;
}

/* ── API ── */

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
    hint.innerHTML = '<p>No champions found.</p>';
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
  document.querySelector('.app').classList.remove('guide-active');
  $('#search-view').style.display = 'block';
  $('#guide-view').style.display = 'none';
  $('#search-input').value = '';
  $('#popular-section').style.display = 'block';
  $('#results-grid').style.display = 'none';
  $('#empty-hint').style.display = 'block';
  $('#empty-hint').innerHTML = '<p>Search any champion to see counter picks and ability tips.</p>';
  $('#hero-splash').style.display = '';
  $('#features-section').style.display = '';
}

async function showGuide(championId) {
  document.querySelector('.app').classList.add('guide-active');
  $('#search-view').style.display = 'none';
  const view = $('#guide-view');
  view.style.display = 'block';
  view.innerHTML = renderLoadingSkeleton();
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
  const difficulty = deriveMatchupDifficulty(guide);

  let html = `<div class="guide">
    <button class="back-btn">← Back to search</button>
    <div class="guide-hero">
      <img class="guide-hero__portrait" src="${champion.image_url}" alt="${champion.name}" />
      <div class="guide-hero__info">
        <h2>vs ${champion.name}${guideBadge(guide)}</h2>
        <div class="title">${champion.title}</div>
        <div class="tags">${tags}</div>
      </div>
    </div>
    ${renderDifficultyGauge(difficulty)}
    <div class="summary">${guide.summary}</div>`;

  if (guide.counter_picks.length) {
    html += `<section class="section"><h3 class="section-title">Counter Picks</h3>`;
    guide.counter_picks.forEach((c, i) => {
      const score = c.counter_score || deriveCounterScore(i, guide.counter_picks.length);
      html += `<div class="counter-card">
        <div class="counter-card__header">
          <span class="name">${c.champion}</span>
          <span class="role">${c.role}</span>
        </div>
        <div class="reason">${c.reason}</div>
        ${renderCounterBar(score)}
      </div>`;
    });
    html += `</section>`;
  }

  html += `<section class="section"><h3 class="section-title">Abilities to Respect</h3>`;
  guide.ability_tips.forEach((a) => {
    const threat = a.threat_level
      ? { score: a.threat_level, tier: a.threat_level >= 85 ? 'critical' : a.threat_level >= 65 ? 'high' : a.threat_level >= 45 ? 'medium' : 'low' }
      : deriveThreatLevel(a);
    html += `<div class="ability-card">
      <div class="ability-header">
        <span class="ability-key">${a.key}</span>
        <span class="ability-name">${a.name}</span>
      </div>
      ${renderThreatMeter(threat)}
      <div class="ability-tip">${highlightTip(a.tip)}</div>
    </div>`;
  });
  html += `</section>`;

  if (guide.laning_tips.length) {
    html += `<section class="section"><h3 class="section-title">Laning Tips</h3><ul class="tip-list">`;
    guide.laning_tips.forEach((t) => { html += `<li>${t}</li>`; });
    html += `</ul></section>`;
  }

  if (guide.power_spikes.length) {
    html += `<section class="section"><h3 class="section-title">Power Spikes</h3>`;
    html += renderSpikeTimeline(guide.power_spikes);
    html += `<ul class="tip-list" style="margin-top:12px">`;
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
      $('#empty-hint').innerHTML = '<p>Search any champion to see counter picks and ability tips.</p>';
      return;
    }
    searchTimer = setTimeout(async () => showSearchResults(await loadChampions(q)), 200);
  });
}

init();
