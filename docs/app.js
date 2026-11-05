(function () {
  var $ = function (id) { return document.getElementById(id); };
  var stato = $("stato");

  function el(tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt) e.textContent = txt; return e; }
  function dl(href, nome, label, ghost) {
    var a = el("a", "btn" + (ghost ? " ghost" : ""), label);
    a.href = href; a.setAttribute("download", nome);
    return a;
  }

  fetch("catalogo.json").then(function (r) { return r.json(); }).then(function (cat) {
    $("zip-nota").textContent = "Logo ufficiale, varianti e banner in PNG e SVG, in un unico ZIP (" + cat.zip_mb + " MB).";
    var box = $("gruppi");
    cat.gruppi.forEach(function (g, gi) {
      var s = el("section", "grp");
      s.appendChild(el("h2", "", g.gruppo));
      s.appendChild(el("p", "grp-d", g.descrizione));
      var grid = el("div", "grid");
      g.voci.forEach(function (v) {
        var largo = /banner-linkedin/.test(v.nome);
        var c = el("article", "card" + (largo ? " largo" : ""));
        var t = el("div", "thumb" + (v.sfondo === "scuro" ? " scuro" : ""));
        var im = el("img"); im.src = v.png; im.alt = v.titolo; im.loading = gi === 0 ? "eager" : "lazy"; im.decoding = "async";
        t.appendChild(im); c.appendChild(t);
        var i = el("div", "info");
        i.appendChild(el("h3", "", v.titolo)); i.appendChild(el("p", "", v.nota));
        var r = el("div", "row");
        r.appendChild(dl(v.png, v.nome + ".png", "Scarica PNG", false));
        r.appendChild(dl(v.svg, v.nome + ".svg", "Scarica SVG", true));
        i.appendChild(r); c.appendChild(i); grid.appendChild(c);
      });
      s.appendChild(grid); box.appendChild(s);
    });
  }).catch(function () { stato.textContent = "Non riesco a caricare l'elenco dei file. Riprova più tardi."; });

  // Installazione come app
  var standalone = window.matchMedia("(display-mode: standalone)").matches || navigator.standalone;
  var ios = /iphone|ipad|ipod/i.test(navigator.userAgent);
  var prompt = null;
  window.addEventListener("beforeinstallprompt", function (e) {
    e.preventDefault(); prompt = e;
    $("installa").hidden = false; $("installa-btn").hidden = false;
  });
  $("installa-btn").addEventListener("click", function () {
    if (!prompt) return;
    prompt.prompt(); prompt.userChoice.finally(function () { prompt = null; $("installa").hidden = true; });
  });
  if (ios && !standalone) {
    $("installa-testo").textContent = "Per avere l'app: tocca Condividi, poi \"Aggiungi alla schermata Home\".";
    $("installa").hidden = false;
  }
  window.addEventListener("appinstalled", function () { $("installa").hidden = true; });

  // Service worker (funzionamento offline)
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("sw.js").then(function () {
      return navigator.serviceWorker.ready;
    }).then(function () { stato.textContent = "Pronta anche senza connessione."; })
      .catch(function () {});
  }
})();
