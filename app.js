/* Danny's Unreal Book — app logic (no build step; plain script). */
(function () {
  'use strict';

  var DATA = window.SONGBOOK || { categories: [], songs: [] };
  var SONGS = DATA.songs;
  var BY_ID = {};
  SONGS.forEach(function (s) { BY_ID[s.id] = s; });
  var LEVELS = [['easy', 'Easy'], ['inter', 'Intermediate'], ['adv', 'Advanced'], ['study', 'Study'], ['chords', 'Chords']];
  var LEVEL_NAME = {};
  LEVELS.forEach(function (l) { LEVEL_NAME[l[0]] = l[1]; });
  var REQUEST_NOTE = 'Requested · send Claude a photo or PDF of your score to add it';
  var app = document.getElementById('app');

  /* ---------------------------------------------------------------- storage */
  var store = {
    get: function (k, d) {
      try { var v = window.localStorage.getItem('dub:' + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; }
    },
    set: function (k, v) {
      try { window.localStorage.setItem('dub:' + k, JSON.stringify(v)); } catch (e) { /* storage unavailable */ }
    }
  };
  var favs = {};
  (store.get('favs', []) || []).forEach(function (id) { favs[id] = true; });
  var levelPref = store.get('levels', {}) || {};
  var tempoPref = store.get('tempo', {}) || {};
  var ui = { cat: 'All', q: '', libScroll: 0 };
  var lyricsOn = store.get('lyrics', true) !== false;
  function hasWords(a) { return !!(a && /\nw:/.test(a.abc)); }
  function abcOf(a) { return lyricsOn ? a.abc : a.abc.replace(/^w:.*(\n|$)/gm, ''); }
  function versesHtml(s) {
    if (!lyricsOn || !s.verses || !s.verses.length) return '';
    return '<div class="verses">' + s.verses.map(function (v, i) {
      return '<p><b>' + (i + 2) + '.</b> ' + esc(v).replace(/\n/g, ' ') + '</p>';
    }).join('') + (s.wsrc ? '<p class="wsrc">' + esc(s.wsrc) + '</p>' : '') + '</div>';
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function inCat(s, c) { return s.cat === c || (s.also && s.also.indexOf(c) >= 0); }
  function levelsOf(s) { return LEVELS.filter(function (l) { return s.levels && s.levels[l[0]]; }); }
  function playable(s) { return levelsOf(s).length > 0; }
  function toast(msg) {
    var t = document.getElementById('toast');
    t.textContent = msg; t.className = 'show';
    clearTimeout(toast.t); toast.t = setTimeout(function () { t.className = ''; }, 3200);
  }
  function stats() {
    var songs = 0, arr = 0, charts = 0;
    SONGS.forEach(function (s) {
      var n = levelsOf(s).length;
      if (s.kind === 'chart') { charts++; return; }
      if (n) { songs++; arr += n; }
    });
    return { songs: songs, arr: arr, charts: charts };
  }

  /* ---------------------------------------------------------------- routing */
  function route() {
    Player.dispose();
    var h = window.location.hash.replace(/^#\/?/, '');
    var parts = h.split('/');
    if (parts[0] === 'library') renderLibrary();
    else if (parts[0] === 'song' && BY_ID[decodeURIComponent(parts[1] || '')]) renderSong(BY_ID[decodeURIComponent(parts[1])]);
    else if (parts[0] === 'book') renderBook(parts[1] || 'easy');
    else renderHome();
  }
  window.addEventListener('hashchange', route);

  /* ---------------------------------------------------------------- home */
  function renderHome() {
    var st = stats();
    var feat = SONGS.filter(function (s) { return s.featured; })[0];
    document.title = "Danny's Unreal Book";
    app.innerHTML =
      '<main class="home">' +
      '<h1>Danny\'s Unreal Book — a personal songbook for piano</h1>' +
      '<img class="cover" src="cover.jpg" width="900" height="1200" alt="Cover of Danny\'s Unreal Book: a worn teal spiral-bound songbook with a grand piano">' +
      '<p class="tag">Choose a song, choose a level, read the music and play.</p>' +
      '<p class="stats">' + st.songs + ' songs · ' + st.arr + ' arrangements' + (st.charts ? ' · ' + st.charts + ' chord charts' : '') + '</p>' +
      '<a class="btn btn-primary" href="#/library">Open the songbook</a>' +
      (feat ? '<p class="featured">Start with Danny\'s own song: <a href="#/song/' + esc(feat.id) + '">' + esc(feat.title) + '</a></p>' : '') +
      '</main>';
    window.scrollTo(0, 0);
  }

  /* ---------------------------------------------------------------- library */
  function topbar(extra) {
    return '<header class="topbar' + (extra && extra.indexOf('iconbtn') >= 0 ? ' compact' : '') + '"><div class="wrap">' +
      '<a class="brand" href="#/" aria-label="Danny\'s Unreal Book — cover"><span class="s">Danny\'s</span><span class="d">UNREAL BOOK</span></a>' +
      (extra || '') + '</div></header>';
  }
  function matches(s) {
    if (ui.cat === 'Favorites') { if (!favs[s.id]) return false; }
    else if (ui.cat === 'I can play') { if (s.status !== 'play') return false; }
    else if (ui.cat === 'Learning') { if (s.status !== 'learn') return false; }
    else if (ui.cat !== 'All' && !inCat(s, ui.cat)) return false;
    var q = ui.q.trim().toLowerCase();
    if (!q) return true;
    var hay = (s.title + ' ' + (s.composer || '') + ' ' + s.cat + ' ' + (s.badges || []).join(' ')).toLowerCase();
    return q.split(/\s+/).every(function (w) { return hay.indexOf(w) >= 0; });
  }
  function statusPill(s) {
    if (s.status === 'play') return '<span class="pill play">★ I can play</span>';
    if (s.status === 'learn') return '<span class="pill learn">Learning</span>';
    return '';
  }
  function cardHtml(s) {
    var lv = levelsOf(s);
    var pills = '<span class="pill cat">' + esc(s.cat) + '</span>';
    if (s.featured) pills += '<span class="pill feat">Danny\'s song</span>';
    pills += statusPill(s);
    (s.badges || []).forEach(function (b) { pills += '<span class="pill warn">' + esc(b) + '</span>'; });
    if (lv.length) pills += '<span class="pill">' + lv.map(function (l) { return l[1]; }).join(' · ') + '</span>';
    var inner = '<span class="t">' + esc(s.title) + '</span><span class="c">' + esc(s.composer || '') + '</span><span class="m">' + pills + '</span>';
    if (s.kind === 'request' || s.kind === 'chart') inner += '<span class="rq">' + esc(s.rq || REQUEST_NOTE) + '</span>';
    if (!lv.length) return '<div class="card req"><div class="open">' + inner + '</div></div>';
    return '<div class="card"><a class="open" href="#/song/' + esc(s.id) + '">' + inner + '</a>' +
      '<button class="star" data-fav="' + esc(s.id) + '" aria-pressed="' + (favs[s.id] ? 'true' : 'false') + '" aria-label="Favorite ' + esc(s.title) + '">' + (favs[s.id] ? '★' : '☆') + '</button></div>';
  }
  function renderLibrary() {
    document.title = "Library — Danny's Unreal Book";
    var st = stats();
    var cats = ['All', 'Favorites', 'I can play', 'Learning'].concat(DATA.categories);
    app.innerHTML = topbar('<a class="btn btn-small" href="#/">Cover</a>') +
      '<main class="wrap">' +
      '<div class="lib-head"><h2>The Songbook</h2><p>' + st.songs + ' songs · ' + st.arr + ' arrangements. Pick one and play.</p>' +
      '<input class="search" id="q" type="search" placeholder="Search songs, composers, categories…" aria-label="Search songs" value="' + esc(ui.q) + '">' +
      '<div class="chips" id="chips" role="group" aria-label="Categories"></div></div>' +
      '<p class="count" id="count"></p><div class="grid" id="grid"></div>' +
      '<div class="bookbox"><strong>Print the whole book</strong>' +
      '<select id="booklevel" aria-label="Level for the printed book"><option value="easy">Easy</option><option value="inter">Intermediate</option><option value="adv">Advanced</option></select>' +
      '<button class="btn" id="bookgo">Prepare the book</button></div></main>';

    function drawChips() {
      document.getElementById('chips').innerHTML = cats.map(function (c) {
        var n = c === 'All' ? SONGS.length : c === 'Favorites' ? Object.keys(favs).length :
          c === 'I can play' ? SONGS.filter(function (s) { return s.status === 'play'; }).length :
          c === 'Learning' ? SONGS.filter(function (s) { return s.status === 'learn'; }).length :
          SONGS.filter(function (s) { return inCat(s, c); }).length;
        return '<button class="chip" data-cat="' + esc(c) + '" aria-pressed="' + (ui.cat === c ? 'true' : 'false') + '">' + (c === 'Favorites' || c === 'I can play' ? '★ ' : '') + esc(c) + '<span class="n">' + n + '</span></button>';
      }).join('');
    }
    function drawGrid() {
      var list = SONGS.filter(matches);
      if (ui.cat === 'All' && !ui.q.trim()) {
        list = list.filter(function (s) { return s.status === 'learn'; })
          .concat(list.filter(function (s) { return s.status !== 'learn' && s.featured; }))
          .concat(list.filter(function (s) { return s.status !== 'learn' && !s.featured; }));
      }
      document.getElementById('count').textContent = list.length + (list.length === 1 ? ' song' : ' songs') + (ui.cat !== 'All' ? ' in ' + ui.cat : '') + (ui.q.trim() ? ' matching “' + ui.q.trim() + '”' : '');
      document.getElementById('grid').innerHTML = list.length ? list.map(cardHtml).join('') :
        '<p class="empty">' + (ui.cat === 'Favorites' ? 'No favorites yet. Tap the ☆ on any song to keep it here.' : ui.cat === 'I can play' || ui.cat === 'Learning' ? 'Nothing is tagged here yet.' : 'Nothing matches. Try a different word or category.') + '</p>';
    }
    drawChips(); drawGrid();
    document.getElementById('q').addEventListener('input', function (e) { ui.q = e.target.value; drawGrid(); });
    document.getElementById('chips').addEventListener('click', function (e) {
      var b = e.target.closest('[data-cat]'); if (!b) return;
      ui.cat = b.getAttribute('data-cat'); drawChips(); drawGrid();
    });
    document.getElementById('grid').addEventListener('click', function (e) {
      var b = e.target.closest('[data-fav]'); if (!b) return;
      toggleFav(b.getAttribute('data-fav')); drawChips(); drawGrid();
    });
    document.getElementById('bookgo').addEventListener('click', function () {
      window.location.hash = '#/book/' + document.getElementById('booklevel').value;
    });
    window.scrollTo(0, ui.libScroll || 0);
  }
  function toggleFav(id) {
    if (favs[id]) delete favs[id]; else favs[id] = true;
    store.set('favs', Object.keys(favs));
  }

  /* ---------------------------------------------------------------- notation */
  function draw(target, abc, width, opts) {
    opts = opts || {};
    var narrow = width < 560;
    var words = /\nw:/.test(abc);
    var pad = narrow ? 4 : 12;
    var staff = Math.max(220, Math.floor(width) - 2 * pad - 2);
    var res, tries = 0;
    do {
      res = window.ABCJS.renderAbc(target, abc, {
        add_classes: true,
        oneSvgPerLine: !!opts.print,
        staffwidth: staff,
        paddingleft: pad, paddingright: pad, paddingtop: 8, paddingbottom: 8,
        wrap: words ? { minSpacing: 2.2, maxSpacing: 3.4, preferredMeasuresPerLine: narrow ? 2 : 3 } : { minSpacing: 1.5, maxSpacing: 2.6, preferredMeasuresPerLine: narrow ? 2 : 4 },
        format: { gchordfont: 'Georgia 13 bold', annotationfont: 'Georgia 12 italic', vocalfont: 'Georgia 12' }
      });
      var svg = target.querySelector ? target.querySelector('svg') : null;
      var w = svg ? parseFloat(svg.getAttribute('width')) || 0 : 0;
      if (w <= width + 1) break;
      staff -= Math.ceil(w - width);
      tries++;
    } while (tries < 3 && staff > 200);
    return res && res[0];
  }

  /* ---------------------------------------------------------------- player */
  var Player = {
    song: null, level: null, vis: null, synth: null, timing: null, ac: null,
    state: 'idle', warp: 100, baseBpm: 90, scrolling: false, scrollSpeed: 30, raf: 0, gen: 0, cursor: null, lastEls: [],

    dispose: function () {
      this.stop(true);
      this.stopScroll();
      this.song = null; this.vis = null;
      window.removeEventListener('resize', this.onResize);
    },
    setStatus: function (msg) {
      var el = document.getElementById('status'); if (!el) return;
      el.textContent = msg || ''; el.className = 'status' + (msg ? ' show' : '');
    },
    paint: function () {
      var playing = this.state === 'playing';
      var big = document.getElementById('bigplay'), tb = document.getElementById('tplay'), tr = document.getElementById('transport');
      if (big) { big.textContent = playing ? '❚❚ Pause' : (this.song && this.song.kind === 'chart' ? '▶ Play chords' : '▶ Play'); big.className = 'bigplay' + (playing ? ' on' : ''); }
      if (tb) { tb.textContent = playing ? '❚❚' : '▶'; tb.setAttribute('aria-label', playing ? 'Pause' : 'Play'); }
      var bpm = document.getElementById('bpm'); if (bpm) bpm.textContent = Math.round(this.baseBpm * this.warp / 100) + ' BPM';
      var sb = document.getElementById('scrollbtn'); if (sb) sb.setAttribute('aria-pressed', this.scrolling ? 'true' : 'false');
      if (tr) tr.className = 'transport' + (this.scrolling ? ' scrolling' : '');
    },
    render: function () {
      var paper = document.getElementById('paper'); if (!paper || !this.song) return;
      var arr = this.song.levels[this.level];
      var w = paper.clientWidth - 8;
      this.width = w;
      try {
        this.vis = draw(paper, abcOf(arr), w);
      } catch (e) {
        paper.innerHTML = '<p style="padding:1rem">Sorry — this score could not be drawn.</p>'; this.vis = null;
        if (window.console) console.error(e);
      }
      this.baseBpm = arr.bpm || 90;
      this.paint();
    },
    onResize: function () {
      clearTimeout(Player.rt);
      Player.rt = setTimeout(function () {
        var paper = document.getElementById('paper');
        if (!paper || !Player.song || Player.printing) return;
        if (Math.abs(paper.clientWidth - 8 - Player.width) < 12) return;
        Player.stop(true); Player.render();
      }, 200);
    },
    toggle: function () {
      if (this.state === 'playing') return this.pause();
      if (this.state === 'paused') return this.resume();
      if (this.state === 'loading') return;
      return this.start(0);
    },
    start: function (frac) {
      var self = this, A = window.ABCJS;
      if (!this.vis) return Promise.resolve();
      if (!A.synth || !A.synth.supportsAudio()) { toast('Sorry — this browser cannot play audio.'); return Promise.resolve(); }
      var gen = ++this.gen;
      this.stopScroll();
      this.state = 'loading'; this.setStatus('Loading piano sound…'); this.paint();
      try {
        if (!this.ac) { var AC = window.AudioContext || window.webkitAudioContext; this.ac = new AC(); }
        if (this.ac.state === 'suspended') this.ac.resume();
      } catch (e) { /* handled below */ }
      var bpm = this.baseBpm * this.warp / 100;
      var synth = new A.synth.CreateSynth();
      this.synth = synth;
      return synth.init({
        audioContext: this.ac, visualObj: this.vis,
        millisecondsPerMeasure: this.vis.millisecondsPerMeasure(bpm),
        options: { program: 0, pan: [-0.15, 0.15] }
      }).then(function () { return synth.prime(); }).then(function () {
        if (gen !== self.gen) { try { synth.stop(); } catch (e) {} return; }
        self.msPerMeasure = self.vis.millisecondsPerMeasure(bpm);
        self.timing = new A.TimingCallbacks(self.vis, {
          qpm: bpm,
          eventCallback: function (ev) { return self.onEvent(ev, gen); }
        });
        synth.start(); self.timing.start();
        if (frac > 0) { try { synth.seek(frac); self.timing.setProgress(frac); } catch (e) {} }
        self.state = 'playing'; self.setStatus(''); self.paint();
        window.DUB_LAST_PLAY = { ok: true, bpm: bpm, ms: self.msPerMeasure, duration: synth.duration };
      }).catch(function (err) {
        if (gen !== self.gen) return;
        self.state = 'idle'; self.setStatus(''); self.paint();
        window.DUB_LAST_PLAY = { ok: false, error: String(err && err.message || err) };
        toast('The piano sound could not load. Check the internet connection and try again.');
        if (window.console) console.error(err);
      });
    },
    pause: function () {
      if (this.state !== 'playing') return;
      try { this.synth.pause(); this.timing.pause(); } catch (e) {}
      this.state = 'paused'; this.paint();
    },
    resume: function () {
      if (this.state !== 'paused') return;
      try { this.synth.resume(); this.timing.start(); } catch (e) {}
      this.state = 'playing'; this.paint();
    },
    stop: function (quiet) {
      this.gen++;
      try { if (this.timing) this.timing.stop(); } catch (e) {}
      try { if (this.synth) this.synth.stop(); } catch (e) {}
      this.timing = null; this.synth = null;
      this.state = 'idle';
      this.clearMarks();
      this.setStatus('');
      if (!quiet) this.paint();
    },
    clearMarks: function () {
      this.lastEls.forEach(function (el) { el.classList.remove('dub-on'); });
      this.lastEls = [];
      if (this.cursor && this.cursor.parentNode) this.cursor.parentNode.removeChild(this.cursor);
      this.cursor = null;
      var on = document.querySelectorAll('.chart .bar.on');
      for (var i = 0; i < on.length; i++) on[i].classList.remove('on');
    },
    onEvent: function (ev, gen) {
      if (gen !== this.gen) return;
      if (!ev) { this.stop(); return; }
      var self = this;
      this.lastEls.forEach(function (el) { el.classList.remove('dub-on'); });
      this.lastEls = [];
      (ev.elements || []).forEach(function (grp) {
        (grp || []).forEach(function (el) { if (el && el.classList) { el.classList.add('dub-on'); self.lastEls.push(el); } });
      });
      var svg = document.querySelector('#paper svg');
      if (svg && typeof ev.left === 'number') {
        if (!this.cursor || this.cursor.ownerSVGElement !== svg) {
          this.cursor = document.createElementNS('http://www.w3.org/2000/svg', 'line');
          this.cursor.setAttribute('class', 'dub-cursor');
          svg.appendChild(this.cursor);
        }
        this.cursor.setAttribute('x1', ev.left - 2); this.cursor.setAttribute('x2', ev.left - 2);
        this.cursor.setAttribute('y1', ev.top); this.cursor.setAttribute('y2', ev.top + ev.height);
      }
      // follow the line being played
      var el = this.lastEls[0];
      if (el && el.getBoundingClientRect) {
        var r = el.getBoundingClientRect(), vh = window.innerHeight;
        if (r.top < 90 || r.bottom > vh - 190) {
          var y = window.pageYOffset + r.top - Math.max(100, vh * 0.28);
          try { window.scrollTo({ top: y, behavior: 'smooth' }); } catch (e) { window.scrollTo(0, y); }
          if (!('scrollBehavior' in document.documentElement.style)) window.scrollTo(0, y);
        }
      }
      // chord charts: light up the current bar
      if (this.song && this.song.chart && this.msPerMeasure) {
        var idx = Math.floor((ev.milliseconds + 1) / this.msPerMeasure);
        var cells = document.querySelectorAll('.chart .bar');
        for (var i = 0; i < cells.length; i++) cells[i].classList.toggle('on', i === idx);
      }
    },
    setWarp: function (v) {
      this.warp = v;
      if (this.song) { tempoPref[this.song.id] = v; store.set('tempo', tempoPref); }
      this.paint();
      var self = this;
      clearTimeout(this.wt);
      if (this.state === 'playing' || this.state === 'paused') {
        this.wt = setTimeout(function () {
          var frac = 0, was = self.state;
          try { frac = self.timing.currentMillisecond() / (self.timing.lastMoment || 1); } catch (e) {}
          if (!(frac >= 0 && frac < 1)) frac = 0;
          self.stop(true);
          if (was === 'playing') self.start(frac); else self.paint();
        }, 350);
      }
    },
    toggleScroll: function () { if (this.scrolling) this.stopScroll(); else this.startScroll(); this.paint(); },
    startScroll: function () {
      var self = this;
      if (this.state === 'playing') { toast('While the piano is playing, the page follows the music by itself.'); return; }
      this.scrolling = true;
      var last = null, acc = 0;
      function step(ts) {
        if (!self.scrolling) return;
        if (last != null) {
          acc += (ts - last) / 1000 * self.scrollSpeed;
          var px = Math.floor(acc);
          if (px >= 1) {
            acc -= px;
            window.scrollBy(0, px);
            var doc = document.documentElement;
            if (window.innerHeight + window.pageYOffset >= doc.scrollHeight - 2) { self.stopScroll(); self.paint(); return; }
          }
        }
        last = ts;
        self.raf = window.requestAnimationFrame(step);
      }
      this.raf = window.requestAnimationFrame(step);
    },
    stopScroll: function () { this.scrolling = false; if (this.raf) window.cancelAnimationFrame(this.raf); this.raf = 0; }
  };
  window.DUB_PLAYER = Player;

  /* ---------------------------------------------------------------- song view */
  function chartHtml(s) {
    var c = s.chart; if (!c) return '';
    var h = '<section class="chart" aria-label="Chord chart"><p class="kv"><b>Key:</b> ' + esc(c.key) + ' &nbsp;·&nbsp; <b>Feel:</b> ' + esc(c.feel) + '</p>';
    c.sections.forEach(function (sec) {
      h += '<h3>' + esc(sec.name) + '</h3><div class="bars">' + sec.bars.map(function (b) {
        var u = b.filter(function (x, i) { return i === 0 || x !== b[i - 1]; });
        return '<div class="bar' + (u.length > 2 ? ' tight' : '') + '">' + u.map(function (x) { return '<span>' + esc(x) + '</span>'; }).join('') + '</div>';
      }).join('') + '</div>';
    });
    h += '<p class="disc">Chord chart: check against your own sheet music. Chords only — no melody. ' + REQUEST_NOTE + '.</p></section>';
    return h;
  }
  function renderSong(s) {
    var lv = levelsOf(s);
    if (!lv.length) { window.location.hash = '#/library'; return; }
    var level = levelPref[s.id];
    if (!s.levels[level]) level = lv[0][0];
    Player.song = s; Player.level = level;
    Player.warp = Math.min(150, Math.max(40, tempoPref[s.id] || 100));
    Player.scrollSpeed = store.get('scrollSpeed', 30) || 30;
    document.title = s.title + " — Danny's Unreal Book";
    var pills = '<span class="pill cat">' + esc(s.cat) + '</span>';
    if (s.featured) pills += '<span class="pill feat">Danny\'s song</span>';
    pills += statusPill(s);
    (s.badges || []).forEach(function (b) { pills += '<span class="pill warn">' + esc(b) + '</span>'; });
    app.innerHTML = topbar(
      '<a class="btn btn-small" href="#/library" id="back">‹ Songs</a>' +
      '<button class="iconbtn" id="fav" aria-pressed="' + (favs[s.id] ? 'true' : 'false') + '" aria-label="Favorite">' + (favs[s.id] ? '★' : '☆') + '</button>' +
      '<button class="btn btn-small" id="print" title="Print or save as PDF">Print</button>') +
      '<main class="wrap song">' +
      '<div class="song-head"><div class="row"><div><h2>' + esc(s.title) + '</h2><p class="by">' + esc(s.composer || '') + '</p></div>' +
      '<button class="bigplay" id="bigplay">▶ Play</button></div>' +
      '<div class="m">' + pills + '</div>' + (s.note ? '<p class="note">' + esc(s.note) + '</p>' : '') + '</div>' +
      (lv.length > 1 ? '<div class="seg" role="group" aria-label="Level">' + lv.map(function (l) {
        return '<button data-level="' + l[0] + '" aria-pressed="' + (l[0] === level ? 'true' : 'false') + '">' + l[1] + '</button>';
      }).join('') + '</div>' : '') +
      '<p class="info" id="info"></p>' +
      chartHtml(s) +
      (s.chart ? '<h3 class="subh no-print">The chords, written out</h3>' : '') +
      ((s.verses && s.verses.length) || hasWords(s.levels[level]) ? '<p class="no-print lyr"><button class="btn btn-small" id="lyrbtn" aria-pressed="' + (lyricsOn ? 'true' : 'false') + '">' + (lyricsOn ? 'Hide words' : 'Show words') + '</button></p>' : '') +
      '<div class="paper" id="paper"></div>' +
      '<div id="verses">' + versesHtml(s) + '</div>' +
      '</main>' +
      '<div class="status" id="status"></div>' +
      '<div class="transport" id="transport"><div class="wrap">' +
      '<button class="tbtn" id="tplay" aria-label="Play">▶</button>' +
      '<button class="tbtn stop" id="tstop" aria-label="Stop">■</button>' +
      '<div class="tempo tempospeed"><label for="warp"><span>Tempo</span><b id="bpm"></b></label><input id="warp" type="range" min="40" max="150" step="5" value="' + Player.warp + '"></div>' +
      '<div class="tempo scrollspeed"><label for="sspeed"><span>Scroll speed</span><b id="sval"></b></label><input id="sspeed" type="range" min="8" max="120" step="2" value="' + Player.scrollSpeed + '"></div>' +
      '<button class="scrollbtn" id="scrollbtn" aria-pressed="false">Auto<br>scroll</button>' +
      '</div></div>';

    function info() {
      var a = s.levels[Player.level];
      var bits = [];
      if (lv.length === 1 || s.kind === 'chart') bits.push(LEVEL_NAME[Player.level]);
      if (a.key) bits.push('Key of ' + a.key.replace(/m$/, ' minor').replace('b', '♭').replace('#', '♯'));
      if (a.bars) bits.push(a.bars + ' bars');
      if (a.note) bits.push(a.note);
      document.getElementById('info').textContent = bits.join(' · ');
    }
    info();
    Player.render();
    window.addEventListener('resize', Player.onResize);
    window.scrollTo(0, 0);

    document.getElementById('bigplay').addEventListener('click', function () { Player.toggle(); });
    document.getElementById('tplay').addEventListener('click', function () { Player.toggle(); });
    document.getElementById('tstop').addEventListener('click', function () { Player.stop(); Player.stopScroll(); Player.paint(); });
    document.getElementById('warp').addEventListener('input', function (e) { Player.setWarp(+e.target.value); });
    var sval = document.getElementById('sval');
    sval.textContent = Player.scrollSpeed + ' px/s';
    document.getElementById('sspeed').addEventListener('input', function (e) {
      Player.scrollSpeed = +e.target.value; sval.textContent = Player.scrollSpeed + ' px/s'; store.set('scrollSpeed', Player.scrollSpeed);
    });
    document.getElementById('scrollbtn').addEventListener('click', function () { Player.toggleScroll(); });
    document.getElementById('fav').addEventListener('click', function (e) {
      toggleFav(s.id);
      e.currentTarget.setAttribute('aria-pressed', favs[s.id] ? 'true' : 'false');
      e.currentTarget.textContent = favs[s.id] ? '★' : '☆';
    });
    var seg = document.querySelector('.seg');
    if (seg) seg.addEventListener('click', function (e) {
      var b = e.target.closest('[data-level]'); if (!b) return;
      Player.stop(true);
      Player.level = b.getAttribute('data-level');
      levelPref[s.id] = Player.level; store.set('levels', levelPref);
      var bs = seg.querySelectorAll('button');
      for (var i = 0; i < bs.length; i++) bs[i].setAttribute('aria-pressed', bs[i] === b ? 'true' : 'false');
      info(); Player.render();
    });
    document.getElementById('print').addEventListener('click', printSong);
    var lb = document.getElementById('lyrbtn');
    if (lb) lb.addEventListener('click', function () {
      lyricsOn = !lyricsOn; store.set('lyrics', lyricsOn);
      lb.setAttribute('aria-pressed', lyricsOn ? 'true' : 'false');
      lb.textContent = lyricsOn ? 'Hide words' : 'Show words';
      document.getElementById('verses').innerHTML = versesHtml(s);
      Player.stop(true); Player.render();
    });
  }

  /* ---------------------------------------------------------------- printing */
  var PRINT_W = 690;
  function printSong() {
    if (!Player.song) return;
    Player.stop(true); Player.stopScroll(); Player.paint();
    window.print();
  }
  window.addEventListener('beforeprint', function () {
    var paper = document.getElementById('paper');
    if (!paper || !Player.song) return;
    Player.printing = true;
    try { draw(paper, abcOf(Player.song.levels[Player.level]), PRINT_W, { print: true }); } catch (e) {}
  });
  window.addEventListener('afterprint', function () {
    if (!Player.printing) return;
    Player.printing = false;
    Player.stop(true); Player.render();
  });

  function renderBook(level) {
    if (!LEVEL_NAME[level]) level = 'easy';
    document.title = "The whole book — Danny's Unreal Book";
    var list = SONGS.filter(function (s) { return playable(s) && s.kind !== 'chart'; });
    var cats = DATA.categories.filter(function (c) { return list.some(function (s) { return s.cat === c; }); });
    var toc = '';
    cats.forEach(function (c) {
      toc += '<h3>' + esc(c) + '</h3><ol>' + list.filter(function (s) { return s.cat === c; }).map(function (s) {
        return '<li>' + esc(s.title) + '</li>';
      }).join('') + '</ol>';
    });
    app.innerHTML = topbar('<a class="btn btn-small" href="#/library">‹ Songs</a>') +
      '<main class="wrap"><div class="book-tools">' +
      '<button class="btn btn-teal" id="bookprint" disabled>Preparing…</button>' +
      '<p id="bookmsg">Laying out ' + list.length + ' songs at the ' + LEVEL_NAME[level] + ' level. In the print dialog choose “Save as PDF” to keep a copy.</p></div>' +
      '<div id="book">' +
      '<section class="book-page book-cover"><img src="cover.jpg" alt="Danny\'s Unreal Book"></section>' +
      '<section class="book-page book-toc"><h2>Contents</h2><p class="by"><span>' + LEVEL_NAME[level] + ' arrangements</span><span>' + list.length + ' songs</span></p>' + toc + '</section>' +
      '</div></main>';
    var book = document.getElementById('book'), i = 0, token = ++renderBook.token;
    function next() {
      if (token !== renderBook.token || !document.getElementById('book')) return;
      var end = Math.min(i + 4, list.length);
      for (; i < end; i++) {
        var s = list[i], lv = s.levels[level] ? level : levelsOf(s)[0][0], a = s.levels[lv];
        var sec = document.createElement('section');
        sec.className = 'book-page';
        sec.innerHTML = '<h2>' + esc(s.title) + '</h2><p class="by"><span>' + esc(s.composer || '') + '</span><span>' +
          esc(LEVEL_NAME[lv] + ((s.badges || []).length ? ' · ' + s.badges.join(' · ') : '')) + '</span></p><div class="bk"></div>';
        book.appendChild(sec);
        try { draw(sec.querySelector('.bk'), abcOf(a), PRINT_W, { print: true }); } catch (e) { sec.querySelector('.bk').textContent = 'Could not draw this score.'; }
      }
      var btn = document.getElementById('bookprint');
      if (i < list.length) { btn.textContent = 'Preparing… ' + i + ' / ' + list.length; setTimeout(next, 0); }
      else { btn.disabled = false; btn.textContent = 'Print / save as PDF'; window.DUB_BOOK_READY = true; }
    }
    document.getElementById('bookprint').addEventListener('click', function () { window.print(); });
    window.scrollTo(0, 0);
    setTimeout(next, 30);
  }
  renderBook.token = 0;

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a.open');
    if (a) ui.libScroll = window.pageYOffset;
  });

  if (!window.ABCJS) {
    app.innerHTML = '<main class="wrap"><p style="padding:2rem 0">The music-drawing library (abcjs) could not be loaded. Check the internet connection and reload.</p></main>';
  } else {
    route();
  }
})();
