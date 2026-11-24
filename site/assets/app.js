(() => {
  const body = document.body;
  const page = body.dataset.page || 'reader';
  const catalogUrl = body.dataset.catalog || 'catalog.json';
  const root = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const themeGlyph = document.querySelector('.theme-glyph');

  function currentTheme() {
    return root.dataset.theme || (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  }
  function applyTheme(theme, save = true) {
    if (theme === 'system') {
      delete root.dataset.theme;
      if (save) localStorage.setItem('theme', 'system');
    } else {
      root.dataset.theme = theme;
      if (save) localStorage.setItem('theme', theme);
    }
    if (themeGlyph) themeGlyph.textContent = currentTheme() === 'dark' ? '☾' : '☼';
    document.querySelectorAll('[data-theme-choice]').forEach(button => {
      button.classList.toggle('selected', button.dataset.themeChoice === (localStorage.getItem('theme') || 'light'));
    });
  }
  try {
    const saved = localStorage.getItem('theme');
    if (saved === 'light' || saved === 'dark') applyTheme(saved, false);
    else if (saved === 'system') applyTheme('system', false);
    else applyTheme('light', false);
  } catch (_) { applyTheme('light', false); }

  themeToggle?.addEventListener('click', () => applyTheme(currentTheme() === 'dark' ? 'light' : 'dark'));
  document.querySelectorAll('[data-theme-choice]').forEach(button => button.addEventListener('click', () => applyTheme(button.dataset.themeChoice)));
  window.matchMedia?.('(prefers-color-scheme: dark)').addEventListener?.('change', () => {
    if (localStorage.getItem('theme') === 'system') applyTheme('system', false);
  });

  const subjectMeta = {
    Informatique: { icon: '⌘', tone: 'violet', description: 'Programmation, systèmes & numérique' },
    Mathematiques: { icon: '∑', tone: 'blue', description: 'Outils et raisonnement mathématique' },
    Mathématiques: { icon: '∑', tone: 'blue', description: 'Outils et raisonnement mathématique' },
    Anglais: { icon: '文', tone: 'coral', description: 'Langue & communication' },
    Physique: { icon: '◉', tone: 'amber', description: 'Sciences et phénomènes physiques' },
    CGE: { icon: '✎', tone: 'green', description: 'Culture générale & expression' }
  };
  const metaFor = subject => subjectMeta[subject] || { icon: '▤', tone: 'slate', description: 'Supports et ressources de cours' };
  const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const courseCard = course => `
    <article class="course-card">
      <div class="course-card-top"><span class="course-type">COURS</span><span class="course-arrow">↗</span></div>
      <h3>${esc(course.title)}</h3>
      <div class="course-card-bottom"><span class="course-subject">${esc(course.subject)}</span><div class="course-actions"><a href="${encodeURI(course.url)}">Ouvrir <span>→</span></a><a class="pdf-link" href="${encodeURI(course.pdf)}" download aria-label="Télécharger le PDF">PDF ↓</a></div></div>
    </article>`;

  async function loadCourses() {
    const response = await fetch(catalogUrl);
    if (!response.ok) throw new Error('Catalogue indisponible');
    return response.json();
  }

  if (page === 'home') {
    const target = document.getElementById('recentCourses');
    loadCourses().then(courses => {
      const latest = [...courses].reverse().slice(0, 4);
      target.innerHTML = latest.length ? latest.map(courseCard).join('') : '<p class="empty-state">Aucun cours publié pour le moment.</p>';
    }).catch(() => { if (target) target.innerHTML = '<p class="empty-state">Impossible de charger les cours pour le moment.</p>'; });
  }

  if (page === 'library') {
    const content = document.getElementById('libraryContent');
    const input = document.getElementById('searchInput');
    const count = document.getElementById('courseCount');
    const filters = document.getElementById('subjectFilters');
    const clear = document.getElementById('clearSearch');
    let allCourses = [];
    let activeSubject = 'Toutes';
    const normalize = value => String(value).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('fr');

    function render() {
      const query = normalize(input.value.trim());
      const visible = allCourses.filter(course => (activeSubject === 'Toutes' || course.subject === activeSubject) && normalize(course.title + ' ' + course.subject).includes(query));
      count.textContent = `${visible.length} cours${visible.length > 1 ? '' : ''} ${query || activeSubject !== 'Toutes' ? 'trouvé' + (visible.length > 1 ? 's' : '') : 'dans la bibliothèque'}`;
      clear.hidden = !input.value && activeSubject === 'Toutes';
      if (!visible.length) {
        content.innerHTML = `<div class="empty-library"><div class="empty-illustration">⌕</div><h2>Aucun cours trouvé</h2><p>Essaie un autre nom ou change de matière.</p></div>`;
        return;
      }
      const groups = new Map();
      visible.forEach(course => { if (!groups.has(course.subject)) groups.set(course.subject, []); groups.get(course.subject).push(course); });
      content.innerHTML = [...groups.entries()].sort(([a],[b]) => a.localeCompare(b, 'fr')).map(([subject, courses]) => {
        const meta = metaFor(subject);
        return `<section class="subject-section"><div class="subject-heading"><div class="subject-icon ${meta.tone}">${meta.icon}</div><div class="subject-heading-copy"><h2>${esc(subject)}</h2><p>${esc(meta.description)}</p></div><span class="subject-count">${courses.length} cours</span></div><div class="course-grid library-course-grid">${courses.map(courseCard).join('')}</div></section>`;
      }).join('');
    }
    loadCourses().then(courses => {
      allCourses = courses;
      const subjects = [...new Set(courses.map(course => course.subject))].sort((a,b) => a.localeCompare(b, 'fr'));
      filters.innerHTML = ['Toutes', ...subjects].map(subject => `<button class="filter-chip ${subject === 'Toutes' ? 'active' : ''}" type="button" data-subject="${esc(subject)}">${subject === 'Toutes' ? 'Tout voir' : esc(subject)}</button>`).join('');
      filters.querySelectorAll('[data-subject]').forEach(button => button.addEventListener('click', () => {
        activeSubject = button.dataset.subject;
        filters.querySelectorAll('.filter-chip').forEach(chip => chip.classList.toggle('active', chip === button));
        render();
      }));
      render();
    }).catch(() => { content.innerHTML = '<p class="empty-state">Impossible de charger la bibliothèque. Réessaie dans un instant.</p>'; count.textContent = 'Catalogue indisponible'; });
    input.addEventListener('input', render);
    clear.addEventListener('click', () => { input.value = ''; activeSubject = 'Toutes'; filters.querySelectorAll('.filter-chip').forEach(chip => chip.classList.toggle('active', chip.dataset.subject === 'Toutes')); render(); input.focus(); });
    document.addEventListener('keydown', event => { if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); input.focus(); } if (event.key === 'Escape' && document.activeElement === input) { input.value = ''; render(); input.blur(); } });
  }
})();
