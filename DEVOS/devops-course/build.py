"""Static site generator for the DevOps course (v2: deep-learning-guide format).

Run: python build.py

Inputs
  content/NN_x.py      -> TOPIC = {slug,title,intro,subs:[...]}      (original source material, preserved)
  content_ext/NN_x.py  -> EXT   = {guide:{...}, subs:{slug:{...}}}    (deep-learning additions, optional)

Original sub fields : slug,title,level,intro,diagram,install,examples[(title,code)],
                      problems[(problem,cause,fix) or (problem,cause,check,fix,prevention)],qa[(q,a)]
Sub extension fields (all optional):
  define   : dict(simple, technical, why, without, use, avoid, analogy)
  internals: text explaining the diagram step by step
  realworld: dict(diagram, text)
  lab      : dict(goal, prereq[list], steps[(command, explanation)])
  commands : [(cmd, does, options, output, mistake, troubleshoot)]
  config   : [(title, code, [(line, meaning)])]
  compare  : [(title, headers[list], rows[list of list])]
  practices: {category: [items]}      mistakes: {category: [items]}
  hinglish : text                     mnemonics: [(term, trick)]
  versions : [items]                  callouts : [(kind info|warn|tip, text)]
  qa_extra : [(level, q, a, why, example)]
Guide fields (topic level, all optional):
  bigpicture: dict(problem, chain[list], diagram, text)
  e2e       : dict(diagram, text)
  tools     : dict(rows[(tool,purpose,input,output,where)], why)
  compare   : like sub.compare              client   : dict(s30, m2, m5)
  hinglish, mnemonics, mistakes, practices, versions
  roadmap   : [(stage, [items])]           miniproject: dict(title, arch, steps[(title, code, explain)])
  cheatsheet: {section: [items]}           interview : [(level, q, a, why, example)]
  troubleshooting: [(problem, cause, check, fix, prevention)]
Text supports `inline code` and **bold**; blank line = paragraph break.
"""
import glob, html, importlib.util, json, os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
LEVEL_CLASS = {"Basic": "b", "Intermediate": "i", "Advanced": "a"}
IQ_LEVELS = ["Beginner", "Intermediate", "Advanced", "Scenario-Based", "Troubleshooting-Based"]
SEARCH = []


def esc(s):
    return html.escape(s, quote=False)


def inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)


def txt(s):
    return "</p><p>".join(inline(p.strip()) for p in s.strip().split("\n\n"))


def para(s):
    return f"<p>{txt(s)}</p>"


def ul(items):
    return "<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>"


def code(c):
    return f"<pre><code>{esc(c.strip(chr(10)))}</code></pre>"


def diagram(d):
    return f'<pre class="diagram">{esc(d.strip(chr(10)))}</pre>'


def table(headers, rows):
    h = "".join(f"<th>{inline(x)}</th>" for x in headers)
    r = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>" for row in rows)
    return f'<div class="tw"><table><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table></div>'


def callout(kind, text):
    label = {"info": "Info", "warn": "Warning", "tip": "Tip", "extra": "Additional Concept"}.get(kind, "Note")
    return f'<div class="box {kind}"><b>{label}:</b> {txt(text)}</div>'


def section(title, body, sid, open_=True):
    return (f'<details class="sec" id="{sid}"{" open" if open_ else ""}><summary><h2>{esc(title)}</h2></summary>'
            f'<div class="secbody">{body}</div></details>')


def qa_block(items, start=1):
    out = []
    for n, it in enumerate(items, start):
        q, a = it[0], it[1]
        why = it[2] if len(it) > 2 else ""
        ex = it[3] if len(it) > 3 else ""
        body = f"<p>{txt(a)}</p>"
        if why:
            body += f'<p><b>Why:</b> {txt(why)}</p>'
        if ex:
            body += f'<p><b>Real-world example:</b> {txt(ex)}</p>'
        out.append(f"<details class='qa'><summary>Q{n}. {txt(q)}</summary>{body}</details>")
    return "".join(out)


# ---------- shared section renderers (used by sub pages and guide pages) ----------

def r_compare(items):
    return "".join(f"<h3>{esc(t)}</h3>{table(h, r)}" for t, h, r in items)


def r_cats(d):
    return "".join(f"<h3>{esc(k)}</h3>{ul(v)}" for k, v in d.items())


def r_mnemonics(items):
    return table(["Concept", "Memory trick"], [[a, b] for a, b in items])


def r_problems(items):
    out = []
    for p in items:
        if len(p) == 3:
            pr, cause, fix = p
            out.append(f'<div class="prob"><b>Problem:</b> {txt(pr)}<br><b>Cause:</b> {txt(cause)}<br><b>Fix:</b> {txt(fix)}</div>')
        else:
            pr, cause, check, fix, prev = p
            out.append(f'<div class="prob"><b>Problem:</b> {txt(pr)}<br><b>Possible cause:</b> {txt(cause)}<br>'
                       f'<b>How to check:</b> {txt(check)}<br><b>Fix:</b> {txt(fix)}<br><b>Prevention:</b> {txt(prev)}</div>')
    return "".join(out)


def r_commands(items):
    out = []
    for cmd, does, options, output, mistake, trouble in items:
        out.append(
            f'<div class="cmd">{code(cmd)}<dl><dt>What does it do?</dt><dd>{txt(does)}</dd>'
            f'<dt>Important options</dt><dd>{txt(options)}</dd>'
            f'<dt>Expected output</dt><dd>{txt(output)}</dd>'
            f'<dt>Common mistake</dt><dd>{txt(mistake)}</dd>'
            f'<dt>Troubleshooting</dt><dd>{txt(trouble)}</dd></dl></div>')
    return "".join(out)


def r_config(items):
    out = []
    for title, c, lines in items:
        out.append(f"<h3>{esc(title)}</h3>{code(c)}")
        if lines:
            out.append(table(["Line", "Meaning / WHY it exists"], [[f"`{a}`", b] for a, b in lines]))
    return "".join(out)


def r_lab(lab):
    b = [f"<h3>Lab Goal</h3>{para(lab['goal'])}"]
    if lab.get("prereq"):
        b.append(f"<h3>Prerequisites</h3>{ul(lab['prereq'])}")
    for n, (c, e) in enumerate(lab["steps"], 1):
        b.append(f'<div class="step"><h3>Step {n}</h3>{code(c)}{para(e)}'
                 f'<label class="chk"><input type="checkbox" data-step> done</label></div>')
    return "".join(b)


def r_define(d):
    rows = [("Simple definition", d.get("simple")), ("Technical definition", d.get("technical")),
            ("Why does it exist?", d.get("why")), ("What happens without it?", d.get("without")),
            ("When to use", d.get("use")), ("When NOT to use", d.get("avoid")),
            ("Real-world analogy", d.get("analogy"))]
    return table(["Question", "Answer"], [[k, v] for k, v in rows if v])


def add_index(title, url, text):
    SEARCH.append({"t": title, "u": url, "x": re.sub(r"\s+", " ", text)[:600]})


# ---------- page shell ----------

def sidebar(topics, cur_slug, cur_sub, depth):
    up = "../" * depth
    out = ['<nav class="side" id="side"><input id="sq" type="search" placeholder="Search topics, commands..." autocomplete="off">'
           '<div id="sres"></div><div class="tree">']
    for t in topics:
        openc = " open" if t["slug"] == cur_slug else ""
        out.append(f'<details{openc}><summary>{esc(t["title"].split("(")[0].strip())}</summary><ul>')
        out.append(f'<li><a href="{up}{t["slug"]}/index.html">Overview</a></li>')
        if t.get("guide"):
            cls = ' class="cur"' if (t["slug"] == cur_slug and cur_sub == "guide") else ""
            out.append(f'<li><a{cls} href="{up}{t["slug"]}/guide.html">Deep Guide &amp; Cheat Sheet</a></li>')
        for s in t["subs"]:
            cls = ' class="cur"' if (t["slug"] == cur_slug and s["slug"] == cur_sub) else ""
            out.append(f'<li><a{cls} href="{up}{t["slug"]}/{s["slug"]}.html" data-pid="{t["slug"]}/{s["slug"]}">{esc(s["title"])}</a></li>')
        out.append("</ul></details>")
    out.append("</div></nav>")
    return "".join(out)


def page(title, body, depth, topics, cur_slug="", cur_sub="", crumbs="", prev_next="", pid="", toc=""):
    up = "../" * depth
    side = sidebar(topics, cur_slug, cur_sub, depth)
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | DevOps Course</title>
<script>try{{var t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<link rel="stylesheet" href="{up}assets/style.css"></head>
<body data-up="{up}" data-pid="{pid}">
<header class="top"><button id="menu" aria-label="Menu">&#9776;</button><a class="brand" href="{up}index.html">DevOps Course</a>
<span class="tl"><a href="{up}hld-lld/index.html">HLD/LLD</a><a href="{up}interview.html">Interview Q&amp;A</a>
<button id="theme" aria-label="Toggle dark mode">&#9788;</button></span></header>
<div class="layout">{side}<main>{crumbs}{toc}{body}{prev_next}</main></div>
<footer>DevOps Course &middot; self-paced &middot; practice every command yourself</footer>
<script src="{up}assets/search-index.js"></script><script src="{up}assets/app.js"></script></body></html>"""


def toc_of(ids):
    if not ids:
        return ""
    return ('<div class="toc"><b>On this page</b> <button id="expall" type="button">Expand all</button> '
            '<button id="colall" type="button">Collapse all</button><div>'
            + " ".join(f'<a href="#{i}">{esc(n)}</a>' for i, n in ids) + "</div></div>")


# ---------- sub page ----------

def sub_page(t, s, i, subs, topics):
    x = s.get("ext", {})
    secs = []  # (id, title, body, open)
    meta = f'<h1>{esc(s["title"])}</h1><p class="meta"><span class="lv {LEVEL_CLASS[s["level"]]}">{s["level"]}</span> {esc(t["title"])}</p>'
    secs.append(("concept", "Concept (What & Why)", para(s["intro"]) + "".join(callout(k, v) for k, v in x.get("callouts", [])), True))
    if x.get("define"):
        secs.append(("define", "Definition Deep-Dive", r_define(x["define"]), True))
    if s.get("diagram"):
        b = diagram(s["diagram"])
        if x.get("internals"):
            b += "<h3>How it works internally (diagram explained)</h3>" + para(x["internals"])
        secs.append(("diagram", "Diagram & Internal Working", b, True))
    elif x.get("internals"):
        secs.append(("internals", "How it works internally", para(x["internals"]), True))
    if x.get("realworld"):
        rw = x["realworld"]
        secs.append(("realworld", "Real-World Example", (diagram(rw["diagram"]) if rw.get("diagram") else "") + para(rw["text"]), True))
    if s.get("install"):
        secs.append(("install", "Install / Setup", code(s["install"]), True))
    if x.get("config"):
        secs.append(("config", "Configuration Explained Line by Line", r_config(x["config"]), True))
    if s.get("examples"):
        secs.append(("examples", "Practical Examples", "".join(f"<h3>{esc(a)}</h3>{code(c)}" for a, c in s["examples"]), True))
    if x.get("commands"):
        secs.append(("commands", "Important Commands Explained", r_commands(x["commands"]), False))
    if x.get("lab"):
        secs.append(("lab", "Hands-On Lab", r_lab(x["lab"]), True))
    if x.get("compare"):
        secs.append(("compare", "Comparison Tables", r_compare(x["compare"]), True))
    probs = s.get("problems", [])
    if probs:
        secs.append(("problems", "Real-World Problems & Fixes (Troubleshooting)", r_problems(probs), True))
    if x.get("practices"):
        secs.append(("practices", "Best Practices", r_cats(x["practices"]), False))
    if x.get("mistakes"):
        secs.append(("mistakes", "Common Mistakes", r_cats(x["mistakes"]), False))
    if x.get("hinglish"):
        secs.append(("hinglish", "Hinglish Explanation", para(x["hinglish"]), True))
    if x.get("mnemonics"):
        secs.append(("memory", "Memory Tricks", r_mnemonics(x["mnemonics"]), True))
    if x.get("versions"):
        secs.append(("versions", "Version / Environment Notes", ul(x["versions"]), False))
    qs = [(q, a) for q, a in s.get("qa", [])] + [(q, a, w, e) for _, q, a, w, e in x.get("qa_extra", [])]
    if qs:
        secs.append(("interview", "Interview Questions", qa_block(qs), False))
    body = meta + "".join(section(n, b, sid, o) for sid, n, b, o in secs)
    body += f'<label class="chk done"><input type="checkbox" id="donebox"> Mark this page as completed</label>'
    pn = '<div class="pn">'
    pn += f'<a href="{subs[i-1]["slug"]}.html">&larr; {esc(subs[i-1]["title"])}</a>' if i > 0 else "<span></span>"
    pn += f'<a href="{subs[i+1]["slug"]}.html">{esc(subs[i+1]["title"])} &rarr;</a>' if i < len(subs) - 1 else '<a href="index.html">Topic home &rarr;</a>'
    pn += "</div>"
    crumbs = f'<nav class="crumbs"><a href="../index.html">Home</a> / <a href="index.html">{esc(t["title"])}</a> / {esc(s["title"])}</nav>'
    add_index(f'{s["title"]} - {t["title"]}', f'{t["slug"]}/{s["slug"]}.html', s["intro"] + " " + " ".join(c for _, c in s.get("examples", [])))
    return page(f'{s["title"]} - {t["title"]}', body, 1, topics, t["slug"], s["slug"], crumbs, pn, f'{t["slug"]}/{s["slug"]}', toc_of([(sid, n) for sid, n, _, _ in secs]))


# ---------- guide page ----------

def guide_page(t, topics):
    g = t["guide"]
    secs = []
    if g.get("bigpicture"):
        b = g["bigpicture"]
        body = para(b["problem"])
        if b.get("chain"):
            body += diagram("\n      |\n      v\n".join(b["chain"]))
        if b.get("diagram"):
            body += diagram(b["diagram"])
        if b.get("text"):
            body += para(b["text"])
        secs.append(("bigpicture", "1. The Big Picture: What Problem Does This Solve?", body, True))
    if g.get("e2e"):
        secs.append(("e2e", "2. End-to-End Flow", diagram(g["e2e"]["diagram"]) + para(g["e2e"]["text"]), True))
    if g.get("tools"):
        tl = g["tools"]
        secs.append(("tools", "3. Tool Relationship", table(["Tool", "Purpose", "Input", "Output", "Where used"], tl["rows"]) + (para(tl["why"]) if tl.get("why") else ""), True))
    if g.get("compare"):
        secs.append(("compare", "4. Comparison Tables", r_compare(g["compare"]), True))
    if g.get("troubleshooting"):
        secs.append(("troubleshoot", "5. Troubleshooting Playbook", r_problems(g["troubleshooting"]), False))
    if g.get("practices"):
        secs.append(("practices", "6. Production Best Practices", r_cats(g["practices"]), False))
    if g.get("mistakes"):
        secs.append(("mistakes", "7. Common Mistakes", r_cats(g["mistakes"]), False))
    if g.get("versions"):
        secs.append(("versions", "8. Version / Environment Notes", ul(g["versions"]), False))
    if g.get("hinglish"):
        secs.append(("hinglish", "9. Hinglish Explanation", para(g["hinglish"]), True))
    if g.get("mnemonics"):
        secs.append(("memory", "10. Memory Tricks", r_mnemonics(g["mnemonics"]), True))
    if g.get("client"):
        c = g["client"]
        secs.append(("client", "11. How I Explain This to a Client",
                     f'<h3>30-second explanation</h3>{para(c["s30"])}<h3>2-minute explanation</h3>{para(c["m2"])}<h3>5-minute deep explanation</h3>{para(c["m5"])}', False))
    if g.get("roadmap"):
        r = g["roadmap"]
        rb = diagram("\n      |\n      v\n".join(f"{n.upper()}" for n, _ in r)) + "".join(f"<h3>{esc(n)}</h3>{ul(v)}" for n, v in r)
        secs.append(("roadmap", "12. Learning Roadmap", rb, False))
    if g.get("miniproject"):
        m = g["miniproject"]
        mb = diagram(m["arch"]) + "".join(f"<h3>{esc(a)}</h3>{code(c)}{para(e)}" for a, c, e in m["steps"])
        secs.append(("mini", "13. Mini Project: " + m["title"], mb, False))
    if g.get("interview"):
        ib = ""
        n = 1
        for lv in IQ_LEVELS:
            items = [(q, a, w, e) for l, q, a, w, e in g["interview"] if l == lv]
            if items:
                ib += f"<h3>{lv} ({len(items)})</h3>" + qa_block(items, n)
                n += len(items)
        secs.append(("iq", "14. Interview Preparation (Question, Answer, Why, Real-world example)", ib, False))
    if g.get("cheatsheet"):
        cb = "".join(f"<h3>{esc(k)}</h3>{ul(v)}" for k, v in g["cheatsheet"].items())
        secs.append(("cheat", "15. QUICK REVISION CHEAT SHEET", cb, True))
    body = f'<h1>{esc(t["title"])}: Deep Guide</h1><p class="meta">Big picture, tools, troubleshooting, best practices, client talk, roadmap, mini project, interview prep and cheat sheet.</p>'
    body += "".join(section(n, b, sid, o) for sid, n, b, o in secs)
    crumbs = f'<nav class="crumbs"><a href="../index.html">Home</a> / <a href="index.html">{esc(t["title"])}</a> / Deep Guide</nav>'
    add_index(f'{t["title"]}: Deep Guide', f'{t["slug"]}/guide.html', t["intro"] + " " + (g.get("bigpicture", {}).get("problem", "")))
    return page(f'{t["title"]} Deep Guide', body, 1, topics, t["slug"], "guide", crumbs, "", f'{t["slug"]}/guide', toc_of([(sid, n) for sid, n, _, _ in secs]))


def topic_index(t, topics):
    b = [f'<h1>{esc(t["title"])}</h1><p>{txt(t["intro"])}</p>']
    if t.get("guide"):
        b.append('<div class="box tip"><b>Start here:</b> <a href="guide.html">Deep Guide &amp; Cheat Sheet</a> has the big picture, tool relationships, '
                 'troubleshooting playbook, client explanation, roadmap, mini project and interview prep for this topic.</div>')
    b.append('<h2>Sub-topics (is order mein padho)</h2><ol class="subs">')
    for s in t["subs"]:
        b.append(f'<li><a href="{s["slug"]}.html" data-pid="{t["slug"]}/{s["slug"]}">{esc(s["title"])}</a> <span class="lv {LEVEL_CLASS[s["level"]]}">{s["level"]}</span></li>')
    b.append("</ol>")
    crumbs = f'<nav class="crumbs"><a href="../index.html">Home</a> / {esc(t["title"])}</nav>'
    add_index(t["title"], f'{t["slug"]}/index.html', t["intro"])
    return page(t["title"], "".join(b), 1, topics, t["slug"], "", crumbs)


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def load_topics():
    topics = []
    for f in sorted(glob.glob(os.path.join(ROOT, "content", "*.py"))):
        base = os.path.basename(f)
        t = load(f, base[:-3]).TOPIC
        ef = os.path.join(ROOT, "content_ext", base)
        if os.path.exists(ef):
            ext = load(ef, "ext_" + base[:-3]).EXT
            t["guide"] = ext.get("guide")
            for s in t["subs"]:
                s["ext"] = ext.get("subs", {}).get(s["slug"], {})
            unknown = set(ext.get("subs", {})) - {s["slug"] for s in t["subs"]}
            if unknown:
                raise SystemExit(f"{base}: unknown sub slugs in EXT: {unknown}")
        topics.append(t)
    return topics


def main():
    topics = load_topics()
    total = 0
    for t in topics:
        base = os.path.join(ROOT, t["slug"])
        if os.path.isdir(base):
            shutil.rmtree(base)
        write(os.path.join(base, "index.html"), topic_index(t, topics))
        if t.get("guide"):
            write(os.path.join(base, "guide.html"), guide_page(t, topics))
        for i, s in enumerate(t["subs"]):
            write(os.path.join(base, s["slug"] + ".html"), sub_page(t, s, i, t["subs"], topics))
            total += 1
    cards = "".join(
        f'<a class="card" href="{t["slug"]}/index.html"><h3>{esc(t["title"])}</h3><p>{len(t["subs"])} sub-topics{" + Deep Guide" if t.get("guide") else ""}</p>'
        f'<div class="bar"><i data-topic="{t["slug"]}"></i></div></a>' for t in topics)
    home = ('<h1>DevOps Engineer: Complete Course</h1><p>Har topic ka alag folder: Deep Guide (big picture, tools, troubleshooting, client talk, roadmap, mini project, cheat sheet) '
            'aur har sub-topic ka alag page (concept, diagram, internals, config, commands, lab, problems, best practices, interview Q&amp;A).</p>'
            '<div class="box tip"><b>Progress:</b> <span id="prog">0%</span> of pages completed (saved in this browser).</div>'
            f'<div class="grid">{cards}'
            '<a class="card hl" href="interview.html"><h3>All Interview Q&amp;A</h3><p>Sab topics ek jagah</p></a></div>')
    write(os.path.join(ROOT, "index.html"), page("Home", home, 0, topics))
    b = ["<h1>All Interview Questions</h1><p>Topic-wise. Click karke answer dekho.</p>"]
    for t in topics:
        b.append(f'<h2>{esc(t["title"])}</h2>')
        for s in t["subs"]:
            for q, a in s.get("qa", []):
                b.append(f'<details class="qa"><summary>{txt(q)} <small>({esc(s["title"])})</small></summary><p>{txt(a)}</p></details>')
            for _, q, a, w, e in s.get("ext", {}).get("qa_extra", []):
                b.append(f'<details class="qa"><summary>{txt(q)} <small>({esc(s["title"])})</small></summary><p>{txt(a)}</p>'
                         f'<p><b>Why:</b> {txt(w)}</p><p><b>Real-world example:</b> {txt(e)}</p></details>')
        g = t.get("guide") or {}
        if g.get("interview"):
            b.append(f'<h3>{esc(t["title"])}: level-wise ({len(g["interview"])} questions)</h3>')
            for lv in IQ_LEVELS:
                items = [(q, a, w, e) for l, q, a, w, e in g["interview"] if l == lv]
                if items:
                    b.append(f"<h4>{lv}</h4>" + qa_block(items))
    write(os.path.join(ROOT, "interview.html"), page("Interview", "".join(b), 0, topics))
    write(os.path.join(ROOT, "assets", "search-index.js"), "window.SEARCH=" + json.dumps(SEARCH, ensure_ascii=False) + ";")
    print(f"{len(topics)} topics, {total} sub-topic pages, {sum(1 for t in topics if t.get('guide'))} guides")


if __name__ == "__main__":
    main()
