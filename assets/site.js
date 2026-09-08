// モバイル用ナビゲーションの開閉
(function () {
  var btn = document.querySelector('.menu-btn');
  var scrim = document.querySelector('.scrim');
  if (!btn) return;
  function close() {
    document.body.classList.remove('nav-open');
    btn.setAttribute('aria-expanded', 'false');
  }
  btn.addEventListener('click', function () {
    var open = document.body.classList.toggle('nav-open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  if (scrim) scrim.addEventListener('click', close);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') close();
  });
})();

// 手順ページの絞り込み（tejun.html のみ）
(function () {
  var form = document.getElementById('chooser');
  if (!form) return;
  var out = document.getElementById('chooser-result');
  var link = document.getElementById('chooser-link');

  function val(name) {
    var el = form.querySelector('input[name="' + name + '"]:checked');
    return el ? el.value : null;
  }
  function update() {
    var waku = val('waku');
    if (waku === 'tsujo') {
      link.href = 'tejun-tsujo.html';
      link.textContent = '通常枠の入力手順を開く';
      out.hidden = false;
      return;
    }
    var kubun = val('kubun'), pc = val('pc'), pos = val('pos');
    if (!waku || !kubun || !pc || !pos) { out.hidden = true; return; }
    link.href = 'tejun-inv-' + kubun + '-pc' + pc + '-pos' + pos + '.html';
    link.textContent = 'あてはまる入力手順を開く';
    out.hidden = false;
  }
  form.addEventListener('change', function () {
    var tsujo = val('waku') === 'tsujo';
    form.querySelectorAll('fieldset[data-inv]').forEach(function (fs) {
      fs.hidden = tsujo;
    });
    var msg = document.getElementById('chooser-msg');
    if (msg) msg.hidden = !tsujo;
    update();
  });
  update();
})();
