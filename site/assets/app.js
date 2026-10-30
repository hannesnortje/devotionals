// Reading progress, stored only in this browser.
(function () {
  var lang = document.body.getAttribute('data-lang');
  var series = document.body.getAttribute('data-series') || 'jona';
  if (!lang) return;
  var KEY = series + '-read-' + lang;
  function load() { try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { return []; } }
  function save(a) { try { localStorage.setItem(KEY, JSON.stringify(a)); } catch (e) {} }
  try { localStorage.setItem(series + '-lang', lang); } catch (e) {}

  var read = load();

  // Overview page
  var items = document.querySelectorAll('.days li[data-day]');
  if (items.length) {
    items.forEach(function (li) {
      if (read.indexOf(+li.getAttribute('data-day')) > -1) li.classList.add('read');
    });
    var p = document.querySelector('.progress');
    if (p) {
      var n = read.length;
      p.querySelector('.label').textContent = p.getAttribute('data-progress-template').replace('{n}', n);
      p.querySelector('.bar span').style.width = (n * 10) + '%';
    }
  }

  // Day page
  var article = document.querySelector('article.day[data-day]');
  var btn = document.querySelector('.mark-read');
  if (article && btn) {
    var day = +article.getAttribute('data-day');
    function paint() {
      var on = read.indexOf(day) > -1;
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      btn.textContent = on ? btn.getAttribute('data-done') : btn.getAttribute('data-label');
    }
    btn.addEventListener('click', function () {
      var i = read.indexOf(day);
      if (i > -1) read.splice(i, 1); else read.push(day);
      save(read); paint();
    });
    paint();
  }
})();
