(function () {
  var d = document, root = d.documentElement, up = d.body.dataset.up || "", pid = d.body.dataset.pid || "";
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  // theme
  d.getElementById("theme").onclick = function () {
    var dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme:dark)").matches;
    root.dataset.theme = dark ? "light" : "dark"; set("theme", root.dataset.theme);
  };
  d.getElementById("menu").onclick = function () { d.getElementById("side").classList.toggle("open"); };

  // copy buttons
  d.querySelectorAll("pre:not(.diagram)").forEach(function (p) {
    var b = d.createElement("button"); b.className = "cp"; b.textContent = "Copy"; b.type = "button";
    b.onclick = function () {
      var t = p.querySelector("code").innerText;
      (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () { b.textContent = "Copied"; }, function () { b.textContent = "Press Ctrl+C"; });
      setTimeout(function () { b.textContent = "Copy"; }, 1500);
    };
    p.appendChild(b);
  });

  // expand / collapse all
  function all(open) { d.querySelectorAll("details.sec").forEach(function (x) { x.open = open; }); }
  var ea = d.getElementById("expall"), ca = d.getElementById("colall");
  if (ea) ea.onclick = function () { all(true); };
  if (ca) ca.onclick = function () { all(false); };
  d.querySelectorAll(".toc a").forEach(function (a) {
    a.addEventListener("click", function () { var t = d.querySelector(a.getAttribute("href")); if (t) t.open = true; });
  });
  if (location.hash) { var h = d.getElementById(location.hash.slice(1)); if (h && h.tagName === "DETAILS") h.open = true; }

  // progress
  var done = {}; try { done = JSON.parse(get("done") || "{}"); } catch (e) {}
  d.querySelectorAll("a[data-pid]").forEach(function (a) { if (done[a.dataset.pid]) a.classList.add("done"); });
  var box = d.getElementById("donebox");
  if (box) {
    box.checked = !!done[pid];
    box.onchange = function () {
      if (box.checked) done[pid] = 1; else delete done[pid];
      set("done", JSON.stringify(done));
      d.querySelectorAll('a[data-pid="' + pid + '"]').forEach(function (a) { a.classList.toggle("done", box.checked); });
    };
  }
  d.querySelectorAll("input[data-step]").forEach(function (c, i) {
    var k = "step:" + pid + ":" + i; c.checked = get(k) === "1"; c.onchange = function () { set(k, c.checked ? "1" : "0"); };
  });
  var prog = d.getElementById("prog");
  if (prog) {
    var total = (window.SEARCH || []).filter(function (s) { return /\/[^/]+\.html$/.test(s.u) && !/index\.html$|guide\.html$/.test(s.u); });
    var n = total.filter(function (s) { return done[s.u.replace(".html", "")]; }).length;
    prog.textContent = Math.round(100 * n / Math.max(total.length, 1)) + "% (" + n + "/" + total.length + ")";
    d.querySelectorAll(".bar i").forEach(function (i) {
      var pre = i.dataset.topic + "/", tt = total.filter(function (s) { return s.u.indexOf(pre) === 0; });
      var nn = tt.filter(function (s) { return done[s.u.replace(".html", "")]; }).length;
      i.style.width = (100 * nn / Math.max(tt.length, 1)) + "%";
    });
  }

  // search
  var q = d.getElementById("sq"), res = d.getElementById("sres");
  q.oninput = function () {
    var v = q.value.trim().toLowerCase(); res.innerHTML = "";
    if (v.length < 2) return;
    var hits = (window.SEARCH || []).filter(function (s) { return (s.t + " " + s.x).toLowerCase().indexOf(v) >= 0; }).slice(0, 12);
    hits.forEach(function (s) { var a = d.createElement("a"); a.href = up + s.u; a.textContent = s.t; res.appendChild(a); });
    if (!hits.length) res.textContent = "No results";
  };
  d.addEventListener("keydown", function (e) { if (e.key === "/" && d.activeElement !== q) { e.preventDefault(); q.focus(); } });
})();
