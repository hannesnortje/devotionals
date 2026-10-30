/* Devotionals – reading flow, progress and menu.
   All state lives only in this browser (localStorage key "dev-state"):
   { lang, active, progress: { <series>: { read: [day…], last: { day, date } } } } */
(function () {
  'use strict';
  var DEV = window.DEV || {};
  var ROOT = DEV.root || '';
  var KEY = 'dev-state';
  var LANGS = DEV.langs || ['de', 'en', 'af'];

  // ---------------------------------------------------------------- state
  function load() {
    var s = null;
    try { s = JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) {}
    s = s || {};
    s.progress = s.progress || {};
    if (!s.migrated) migrate(s);
    return s;
  }
  function save(s) { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {} }
  function migrate(s) { // progress from the first version of the site (per language)
    try {
      LANGS.forEach(function (l) {
        var a = JSON.parse(localStorage.getItem('jona-read-' + l) || '[]');
        if (a.length) {
          var p = prog(s, 'jona');
          a.forEach(function (n) { if (p.read.indexOf(n) < 0) p.read.push(n); });
          s.active = s.active || 'jona';
        }
      });
      var ol = localStorage.getItem('jona-lang');
      if (ol && !s.lang) s.lang = ol;
    } catch (e) {}
    s.migrated = 1;
  }
  function prog(s, slug) { return s.progress[slug] || (s.progress[slug] = { read: [], last: null }); }
  function today() {
    var d = new Date();
    return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2);
  }
  function total(slug) {
    var c = (DEV.catalog || []).filter(function (x) { return x.slug === slug; })[0];
    return c ? c.total : 0;
  }
  // The day a reader should land on: the day just read stays "today's" until midnight,
  // otherwise the first unread day; 'done' when everything is read.
  function nextDay(s, slug) {
    var p = prog(s, slug), T = total(slug);
    if (p.last && p.last.date === today() && p.read.indexOf(p.last.day) > -1) return p.last.day;
    for (var n = 1; n <= T; n++) if (p.read.indexOf(n) < 0) return n;
    return T ? 'done' : 1;
  }
  function pad(n) { return ('0' + n).slice(-2); }
  function dayUrl(slug, lang, n) {
    return ROOT + slug + '/' + lang + '/' + (n === 'done' ? 'done.html' : DEV.dayword[lang] + '-' + pad(n) + '.html');
  }
  function detectLang() {
    var list = navigator.languages || [navigator.language || 'en'];
    for (var i = 0; i < list.length; i++) {
      var c = String(list[i]).slice(0, 2).toLowerCase();
      if (LANGS.indexOf(c) > -1) return c;
    }
    return 'en';
  }
  function known(slug) { return total(slug) > 0; }

  var state = load();

  // ---------------------------------------------------------------- routers
  if (DEV.page === 'router') {
    var lang = state.lang || detectLang();
    var target = (state.active && known(state.active))
      ? dayUrl(state.active, lang, nextDay(state, state.active))
      : ROOT + 'home/' + lang + '.html';
    location.replace(target);
    return;
  }
  if (DEV.page === 'series-router') {
    location.replace((state.lang || detectLang()) + '/index.html');
    return;
  }

  // ---------------------------------------------------------------- every page
  if (DEV.lang) { state.lang = DEV.lang; save(state); }
  document.querySelectorAll('[data-set-lang]').forEach(function (a) {
    a.addEventListener('click', function () { state.lang = a.getAttribute('data-set-lang'); save(state); });
  });

  function paintTicks(root, slug) {
    var p = prog(state, slug);
    root.querySelectorAll('li[data-day]').forEach(function (li) {
      li.classList.toggle('read', p.read.indexOf(+li.getAttribute('data-day')) > -1);
    });
  }
  function paintProgress(el, slug) {
    if (!el) return;
    var n = prog(state, slug).read.length, T = total(slug) || 10;
    var label = el.querySelector('.label'), bar = el.querySelector('.bar span');
    if (label) label.textContent = el.getAttribute('data-progress-template').replace('{n}', n).replace('{total}', T);
    if (bar) bar.style.width = Math.round(100 * n / T) + '%';
  }

  // series overview
  if (DEV.series) {
    var list = document.querySelector('.days');
    if (list) paintTicks(list, DEV.series);
    paintProgress(document.querySelector('.plan .progress'), DEV.series);
  }

  // day page
  var article = document.querySelector('article.day[data-day]');
  var btn = document.querySelector('.mark-read:not([data-restart])');
  if (DEV.page === 'day' && article && btn) {
    var day = +article.getAttribute('data-day');
    var note = document.querySelector('[data-read-note]');
    state.active = DEV.series; save(state);
    var paint = function () {
      var on = prog(state, DEV.series).read.indexOf(day) > -1;
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      btn.textContent = on ? btn.getAttribute('data-done') : btn.getAttribute('data-label');
      if (note) note.hidden = !on;
    };
    btn.addEventListener('click', function () {
      var p = prog(state, DEV.series), i = p.read.indexOf(day);
      if (i > -1) { p.read.splice(i, 1); if (p.last && p.last.day === day) p.last = null; }
      else { p.read.push(day); p.last = { day: day, date: today() }; }
      save(state); paint(); paintDrawer();
    });
    paint();
  }

  // completed page: read again
  var restart = document.querySelector('[data-restart]');
  if (restart) restart.addEventListener('click', function () {
    var slug = restart.getAttribute('data-restart');
    state.progress[slug] = { read: [], last: null }; state.active = slug; save(state);
    location.href = restart.getAttribute('data-href');
  });

  // home page tiles
  document.querySelectorAll('[data-series-tile]').forEach(function (tile) {
    var slug = tile.getAttribute('data-series-tile');
    var p = prog(state, slug), go = tile.querySelector('[data-tile-go]');
    var n = nextDay(state, slug), started = p.read.length > 0 || p.last;
    paintProgress(tile.querySelector('.progress'), slug);
    tile.querySelector('.progress').hidden = !started;
    go.href = dayUrl(slug, DEV.lang, n);
    go.textContent = n === 'done' ? go.getAttribute('data-done')
      : started ? go.getAttribute('data-continue').replace('{n}', n) : go.getAttribute('data-start');
    var lost = tile.querySelector('[data-lost]');
    if (lost && !started) {
      lost.hidden = false;
      lost.addEventListener('submit', function (e) {
        e.preventDefault();
        var k = +lost.querySelector('select').value, q = prog(state, slug);
        q.read = []; for (var i = 1; i < k; i++) q.read.push(i);
        q.last = null; state.active = slug; save(state);
        location.href = dayUrl(slug, DEV.lang, k);
      });
    }
  });
  var tip = document.querySelector('[data-install-tip]');
  if (tip && ((window.matchMedia && matchMedia('(display-mode: standalone)').matches) || navigator.standalone)) tip.hidden = true;

  // ---------------------------------------------------------------- menu
  var drawer = document.getElementById('drawer');
  var menuBtn = document.querySelector('.menu-btn');
  var overlay = document.querySelector('.drawer-overlay');
  function paintDrawer() {
    if (!drawer) return;
    var cont = drawer.querySelector('[data-continue]');
    if (cont && state.active && known(state.active)) {
      var n = nextDay(state, state.active);
      cont.href = dayUrl(state.active, DEV.lang, n);
      var lbl = cont.querySelector('[data-continue-label]');
      if (lbl) lbl.textContent = n === 'done' ? '✓' : '· ' + (lbl.getAttribute('data-dayword') || '') + ' ' + n;
      cont.hidden = false;
    }
    var days = drawer.querySelector('[data-series-days]');
    if (days) paintTicks(days, days.getAttribute('data-series-days'));
    drawer.querySelectorAll('[data-series-progress]').forEach(function (el) {
      var slug = el.getAttribute('data-series-progress'), r = prog(state, slug).read.length;
      el.textContent = r ? r + '/' + el.getAttribute('data-total') : '';
    });
  }
  function openDrawer() {
    paintDrawer();
    drawer.removeAttribute('inert'); drawer.setAttribute('aria-hidden', 'false');
    drawer.classList.add('open'); overlay.hidden = false;
    requestAnimationFrame(function () { overlay.classList.add('show'); });
    menuBtn.setAttribute('aria-expanded', 'true');
    document.documentElement.classList.add('no-scroll');
    var cur = drawer.querySelector('[aria-current="page"] a') || drawer.querySelector('a');
    if (cur) { cur.focus({ preventScroll: true }); if (cur.scrollIntoView) cur.scrollIntoView({ block: 'center' }); }
  }
  function closeDrawer() {
    drawer.classList.remove('open'); overlay.classList.remove('show');
    drawer.setAttribute('aria-hidden', 'true'); drawer.setAttribute('inert', '');
    menuBtn.setAttribute('aria-expanded', 'false');
    document.documentElement.classList.remove('no-scroll');
    setTimeout(function () { overlay.hidden = true; }, 250);
    menuBtn.focus({ preventScroll: true });
  }
  if (drawer && menuBtn) {
    menuBtn.addEventListener('click', function () { drawer.classList.contains('open') ? closeDrawer() : openDrawer(); });
    document.querySelectorAll('[data-drawer-close]').forEach(function (el) { el.addEventListener('click', closeDrawer); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && drawer.classList.contains('open')) closeDrawer(); });
    paintDrawer();
    var reset = drawer.querySelector('[data-reset]');
    if (reset) {
      var label = reset.textContent, armed = false;
      reset.addEventListener('click', function () {
        if (!armed) { armed = true; reset.textContent = reset.getAttribute('data-confirm'); reset.classList.add('armed'); return; }
        var slug = reset.getAttribute('data-series');
        if (slug) state.progress[slug] = { read: [], last: null };
        else { state.progress = {}; state.active = null; }
        save(state); armed = false; reset.classList.remove('armed');
        reset.textContent = reset.getAttribute('data-done');
        paintDrawer();
        if (DEV.series) { var l = document.querySelector('.days'); if (l) paintTicks(l, DEV.series); paintProgress(document.querySelector('.plan .progress'), DEV.series); }
        var b = document.querySelector('.mark-read:not([data-restart])'); if (b && DEV.page === 'day') { b.setAttribute('aria-pressed', 'false'); b.textContent = b.getAttribute('data-label'); var nt = document.querySelector('[data-read-note]'); if (nt) nt.hidden = true; }
        setTimeout(function () { reset.textContent = label; }, 2500);
      });
    }
  }

  // ---------------------------------------------------------------- offline support
  // Updates: pages always come fresh from the network when online. When a new version is
  // published, the service worker swaps the offline copy. An installed app is often resumed
  // rather than reloaded, so check for updates whenever it comes back to the foreground.
  if ('serviceWorker' in navigator && (location.protocol === 'https:' || location.hostname === 'localhost')) {
    var hadController = !!navigator.serviceWorker.controller, resumedAt = Date.now(), reloading = false;
    window.addEventListener('load', function () {
      navigator.serviceWorker.register(ROOT + 'sw.js').then(function (reg) {
        document.addEventListener('visibilitychange', function () {
          if (document.visibilityState === 'visible') { resumedAt = Date.now(); reg.update().catch(function () {}); }
        });
        setInterval(function () { reg.update().catch(function () {}); }, 60 * 60 * 1000);
      }).catch(function () {});
    });
    navigator.serviceWorker.addEventListener('controllerchange', function () {
      if (!hadController) { hadController = true; return; }   // first install: nothing to refresh
      if (reloading) return;
      var justResumed = Date.now() - resumedAt < 8000, atTop = window.scrollY < 300;
      if (justResumed || atTop) { reloading = true; location.reload(); return; }
      var toast = document.querySelector('[data-update]');
      if (toast) { toast.hidden = false; toast.addEventListener('click', function () { location.reload(); }); }
    });
  }
})();
