/* ===== Senior Dev Notes — shared script ===== */

/* ---- Site map: used to build the sidebar on every page ---- */
const SITE = {
  topics: [
    { id: "01-system-design", title: "System Design", chapters: [
      "01-fundamentals","02-networking","03-load-balancing","04-caching",
      "05-databases","06-database-scaling","07-transactions","08-message-queues",
      "09-microservices","10-api-design","11-resilience","12-lld-design-patterns",
      "13-hld-case-studies","14-interview-framework"
    ], titles: [
      "Fundamentals","Networking Basics","Load Balancing & Reverse Proxies","Caching",
      "Databases","Database Scaling","Transactions","Message Queues & Event-Driven",
      "Microservices vs Monolith","API Design","Resilience Patterns","LLD: SOLID & Design Patterns",
      "HLD Case Studies","Interview Framework"
    ]},
    { id: "02-typescript-advanced", title: "TypeScript Advanced", chapters: [
      "01-type-system","02-generics","03-utility-types","04-conditional-mapped-template",
      "05-type-safe-patterns","06-tsconfig-monorepo"
    ], titles: [
      "Type System Deep Dive","Generics In Depth","Utility Types","Conditional / Mapped / Template Literal Types",
      "Type-Safe Patterns for React & Node","tsconfig, Strict Mode, Monorepos"
    ]},
    { id: "03-react-nextjs-advanced", title: "React & Next.js Advanced", chapters: [
      "01-react-internals","02-hooks-deep-dive","03-state-management","04-performance",
      "05-concurrent-react","06-nextjs-app-router","07-server-client-components",
      "08-rendering-strategies","09-core-web-vitals","10-frontend-architecture","11-accessibility-seo"
    ], titles: [
      "React Internals: Fiber & Reconciliation","Hooks Deep Dive","State Management","React Performance",
      "Concurrent React","Next.js App Router","Server vs Client Components",
      "Rendering Strategies (CSR/SSR/SSG/ISR/PPR)","Core Web Vitals","Frontend Architecture","Accessibility & SEO"
    ]},
    { id: "04-nodejs-advanced", title: "Node.js Advanced", chapters: [
      "01-event-loop","02-streams-buffers","03-worker-threads","04-memory-gc",
      "05-error-handling","06-production-apis","07-authentication","08-background-jobs","09-scaling-node"
    ], titles: [
      "Event Loop Internals & libuv","Streams, Buffers, Backpressure","Worker Threads & Clustering",
      "Memory Management & GC","Error Handling Strategy","Production APIs (Express/Fastify/Nest)",
      "Authentication (JWT/OAuth2/SSO)","Background Jobs & Scheduling","Scaling Node in Production"
    ]},
    { id: "05-testing", title: "Testing", chapters: [
      "01-testing-strategy","02-unit-testing","03-react-testing-library",
      "04-api-integration-testing","05-e2e-playwright","06-tdd-coverage-ci"
    ], titles: [
      "Testing Strategy & Pyramid","Unit Testing (Jest/Vitest)","React Testing Library",
      "API & Integration Testing","E2E Testing with Playwright","TDD, Coverage, CI"
    ]},
    { id: "06-cloud-aws-docker-k8s", title: "Cloud, AWS, Docker & K8s", chapters: [
      "01-docker-deep-dive","02-docker-compose","03-kubernetes-core","04-aws-core",
      "05-serverless","06-infrastructure-as-code","07-advanced-cicd"
    ], titles: [
      "Docker Deep Dive","Docker Compose","Kubernetes Core","AWS Core (IAM/VPC/EC2/S3/RDS)",
      "Serverless (Lambda, API Gateway)","Infrastructure as Code (Terraform)","Advanced CI/CD"
    ]},
    { id: "07-observability-security", title: "Observability & Security", chapters: [
      "01-logging","02-metrics-monitoring","03-distributed-tracing",
      "04-owasp-top-10","05-secure-auth-secrets","06-incident-handling"
    ], titles: [
      "Logging & Centralized Logging","Metrics, Monitoring & Alerting","Distributed Tracing",
      "OWASP Top 10","Secure Auth, Secrets, CORS/CSP/XSS/CSRF","Incident Handling & Post-Mortems"
    ]},
    { id: "08-python-intermediate", title: "Python Intermediate", chapters: [
      "01-python-for-js-devs","02-data-structures","03-oop-dataclasses",
      "04-async-python","05-fastapi","06-venv-packaging-pytest"
    ], titles: [
      "Python for JS Developers","Data Structures, Comprehensions, Generators","OOP, Dataclasses, Type Hints",
      "Async Python (asyncio)","FastAPI in Production","Virtual Envs, Packaging, pytest"
    ]},
    { id: "09-ai-integration", title: "AI Integration", chapters: [
      "01-how-llms-work","02-llm-apis","03-embeddings-vector-db",
      "04-rag","05-ai-agents","06-ai-in-production","07-ai-features-react-node"
    ], titles: [
      "How LLMs Work","Using LLM APIs","Embeddings & Vector Databases",
      "RAG: Architecture & Evaluation","AI Agents & Workflows","AI in Production","AI Features in React/Node"
    ]},
    { id: "10-soft-skills-leadership", title: "Soft Skills & Leadership", chapters: [
      "01-design-docs-rfcs","02-code-reviews","03-mentoring",
      "04-estimation-planning","05-stakeholder-communication","06-decision-making","07-behavioral-interviews"
    ], titles: [
      "Writing Design Docs & RFCs","Code Reviews That Improve Teams","Mentoring Juniors",
      "Estimation, Planning & Risk","Stakeholder Communication","Technical Decision Making","Behavioral Interviews (STAR)"
    ]},
    { id: "11-web-fundamentals", title: "Web Fundamentals", chapters: [
      "01-html-css-fundamentals","02-javascript-fundamentals","03-dom-and-browser",
      "04-http-and-networking-basics","05-git-and-version-control","06-bash-and-terminal-basics"
    ], titles: [
      "HTML & CSS Fundamentals","JavaScript Fundamentals","The DOM & Browser Environment",
      "HTTP & Networking Basics","Git & Version Control","Bash & Terminal Basics"
    ]},
    { id: "12-react-fundamentals", title: "React Fundamentals", chapters: [
      "01-react-basics-jsx-components","02-props-state-events","03-hooks-basics",
      "04-forms-and-controlled-components","05-routing-react-router","06-project-structure-and-tooling"
    ], titles: [
      "React Basics: JSX & Components","Props, State & Events","Hooks Basics (useState/useEffect)",
      "Forms & Controlled Components","Routing with React Router","Project Structure & Tooling"
    ]},
    { id: "13-nodejs-fundamentals", title: "Node.js Fundamentals", chapters: [
      "01-nodejs-basics-runtime-modules","02-npm-and-package-management","03-fs-path-os-core-modules",
      "04-http-module-and-basic-servers","05-express-basics-routing-middleware","06-rest-api-fundamentals"
    ], titles: [
      "Node.js Basics: Runtime & Modules","npm & Package Management","Core Modules: fs, path, os",
      "HTTP Module & Basic Servers","Express Basics: Routing & Middleware","REST API Fundamentals"
    ]},
    { id: "14-python-fundamentals", title: "Python Fundamentals", chapters: [
      "01-python-syntax-and-basics","02-control-flow-and-functions","03-data-types-and-collections",
      "04-file-io-and-modules","05-error-handling-and-debugging","06-intro-to-web-with-flask-fastapi"
    ], titles: [
      "Python Syntax & Basics","Control Flow & Functions","Data Types & Collections",
      "File I/O & Modules","Error Handling & Debugging","Intro to Web with Flask/FastAPI"
    ]},
    { id: "15-machine-learning-ai", title: "Machine Learning & AI", chapters: [
      "01-ml-math-and-foundations","02-ai-history-and-landscape","03-neural-networks-from-scratch",
      "04-pytorch-and-tensors","05-cnns-rnns-sequence-models","06-attention-and-transformers",
      "07-huggingface-ecosystem","08-llm-observability-tracing","09-vector-databases-and-rag",
      "10-context-engineering","11-ai-agents-from-first-principles","12-agent-frameworks-memory-mcp",
      "13-finetuning-and-rl","14-evals-advanced-topics-multimodal"
    ], titles: [
      "ML Math & Foundations","AI History & Landscape","Neural Networks from Scratch",
      "PyTorch & Tensors","CNNs, RNNs & Sequence Models","Attention & Transformers",
      "HuggingFace Ecosystem","LLM Observability & Tracing","Vector Databases & RAG",
      "Context Engineering","AI Agents from First Principles","Agent Frameworks, Memory & MCP",
      "Fine-tuning & RL","Evals, Advanced Topics & Multimodal"
    ]}
  ]
};

/* ---- Theme ---- */
function initTheme() {
  const saved = localStorage.getItem("sdn-theme");
  if (saved) document.documentElement.setAttribute("data-theme", saved);
  else if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
    document.documentElement.setAttribute("data-theme", "dark");
  }
}
function toggleTheme() {
  const cur = document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
  const next = cur === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem("sdn-theme", next);
  const btn = document.getElementById("theme-toggle");
  if (btn) btn.textContent = next === "dark" ? "☀️" : "🌙";
  if (window.mermaid) try { location.reload(); } catch (e) {}
}
initTheme();

/* ---- Progress (localStorage) ---- */
function getDoneSet() {
  try { return new Set(JSON.parse(localStorage.getItem("sdn-done") || "[]")); }
  catch (e) { return new Set(); }
}
function saveDoneSet(set) {
  localStorage.setItem("sdn-done", JSON.stringify([...set]));
}
function isChapterDone(key) { return getDoneSet().has(key); }
function setChapterDone(key, done) {
  const set = getDoneSet();
  if (done) set.add(key); else set.delete(key);
  saveDoneSet(set);
}
function topicProgress(topicId) {
  const topic = SITE.topics.find(t => t.id === topicId);
  if (!topic) return { done: 0, total: 0 };
  const done = getDoneSet();
  let count = 0;
  topic.chapters.forEach(c => { if (done.has(topicId + "/" + c)) count++; });
  return { done: count, total: topic.chapters.length };
}
function overallProgress() {
  let done = 0, total = 0;
  SITE.topics.forEach(t => { const p = topicProgress(t.id); done += p.done; total += p.total; });
  return { done, total };
}

/* ---- Sidebar rendering ---- */
function buildSidebar(rootPrefix, currentTopic, currentChapterKey) {
  const nav = document.getElementById("sidebar-nav");
  if (!nav) return;
  const done = getDoneSet();
  let html = "";
  SITE.topics.forEach(topic => {
    const isCurrent = topic.id === currentTopic;
    html += `<details ${isCurrent ? "open" : ""}><summary>${topic.title}</summary><ul>`;
    html += `<li><a href="${rootPrefix}${topic.id}/index.html"${isCurrent && !currentChapterKey ? ' class="active"' : ""}>▦ Overview</a></li>`;
    topic.chapters.forEach((ch, i) => {
      const key = topic.id + "/" + ch;
      const isActive = isCurrent && currentChapterKey === ch;
      const doneCls = done.has(key) ? " done" : "";
      html += `<li><a href="${rootPrefix}${topic.id}/${ch}.html" class="${isActive ? "active" : ""}${doneCls}">${topic.titles[i]}</a></li>`;
    });
    html += `</ul></details>`;
  });
  nav.innerHTML = html;
}

/* ---- Done checkbox wiring (on chapter pages) ---- */
function wireDoneToggle(chapterKey) {
  const cb = document.getElementById("done-checkbox");
  if (!cb) return;
  cb.checked = isChapterDone(chapterKey);
  cb.addEventListener("change", () => {
    setChapterDone(chapterKey, cb.checked);
    const link = document.querySelector(`#sidebar-nav a[href$="${chapterKey.split("/")[1]}.html"]`);
    if (link) link.classList.toggle("done", cb.checked);
  });
}

/* ---- Auto TOC from h2/h3 inside .content ---- */
function buildTOC() {
  const container = document.getElementById("toc-list");
  if (!container) return;
  const content = document.querySelector(".content");
  const headings = content.querySelectorAll("h2[id], h3[id]");
  let html = "";
  headings.forEach(h => {
    const indent = h.tagName === "H3" ? ' style="margin-left:14px;font-size:.88em;"' : "";
    html += `<li${indent}><a href="#${h.id}">${h.textContent}</a></li>`;
  });
  container.innerHTML = html || "<li>—</li>";
}

/* ---- Copy buttons on code blocks ---- */
function wireCopyButtons() {
  document.querySelectorAll("pre > code").forEach(code => {
    const pre = code.parentElement;
    if (pre.parentElement.classList.contains("code-wrap")) return;
    const wrap = document.createElement("div");
    wrap.className = "code-wrap";
    pre.replaceWith(wrap);
    wrap.appendChild(pre);
    const btn = document.createElement("button");
    btn.className = "copy-btn";
    btn.textContent = "Copy";
    btn.addEventListener("click", () => {
      navigator.clipboard.writeText(code.textContent).then(() => {
        btn.textContent = "Copied!";
        setTimeout(() => (btn.textContent = "Copy"), 1200);
      });
    });
    wrap.appendChild(btn);
  });
}

/* ---- Mobile sidebar toggle ---- */
function wireMenuToggle() {
  const btn = document.getElementById("menu-toggle");
  const sidebar = document.querySelector(".sidebar");
  if (!btn || !sidebar) return;
  btn.addEventListener("click", () => sidebar.classList.toggle("open"));
  document.addEventListener("click", (e) => {
    if (sidebar.classList.contains("open") && !sidebar.contains(e.target) && e.target !== btn) {
      sidebar.classList.remove("open");
    }
  });
}

/* ---- Global search (home page) ---- */
function buildSearchIndex() {
  const index = [];
  SITE.topics.forEach(topic => {
    topic.chapters.forEach((ch, i) => {
      index.push({
        title: topic.titles[i],
        topic: topic.title,
        href: `${topic.id}/${ch}.html`
      });
    });
  });
  return index;
}
function wireSearch(rootPrefix) {
  const input = document.getElementById("global-search");
  const results = document.getElementById("search-results");
  if (!input || !results) return;
  const index = buildSearchIndex();
  input.addEventListener("input", () => {
    const q = input.value.trim().toLowerCase();
    if (!q) { results.innerHTML = ""; results.style.display = "none"; return; }
    const matches = index.filter(e => e.title.toLowerCase().includes(q) || e.topic.toLowerCase().includes(q)).slice(0, 12);
    results.style.display = matches.length ? "block" : "none";
    results.innerHTML = matches.map(m =>
      `<li><a href="${rootPrefix}${m.href}"><strong>${m.title}</strong><span> — ${m.topic}</span></a></li>`
    ).join("");
  });
}

/* ---- Init helper called by every page ---- */
function initPage(opts) {
  const { rootPrefix = "", topic = null, chapterKey = null } = opts || {};
  buildSidebar(rootPrefix, topic, chapterKey);
  wireMenuToggle();
  const themeBtn = document.getElementById("theme-toggle");
  if (themeBtn) {
    themeBtn.textContent = document.documentElement.getAttribute("data-theme") === "dark" ? "☀️" : "🌙";
    themeBtn.addEventListener("click", toggleTheme);
  }
  if (chapterKey) wireDoneToggle(topic + "/" + chapterKey);
  buildTOC();
  wireCopyButtons();
  wireSearch(rootPrefix);
  if (window.mermaid) window.mermaid.initialize({ startOnLoad: true, theme: document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "default" });
  renderProgressCards();
}

/* ---- Progress cards on home page ---- */
function renderProgressCards() {
  const grid = document.getElementById("topic-cards");
  if (!grid) return;
  let html = "";
  SITE.topics.forEach(topic => {
    const p = topicProgress(topic.id);
    const pct = p.total ? Math.round((p.done / p.total) * 100) : 0;
    html += `
    <a class="card" href="${topic.id}/index.html" style="text-decoration:none;">
      <h3>${topic.title}</h3>
      <p>${topic.chapters.length} chapters</p>
      <div class="progress-bar"><span style="width:${pct}%"></span></div>
      <div class="card-footer"><span>${p.done}/${p.total} done</span><span>${pct}%</span></div>
    </a>`;
  });
  grid.innerHTML = html;
  const overallEl = document.getElementById("overall-progress");
  if (overallEl) {
    const o = overallProgress();
    const pct = o.total ? Math.round((o.done / o.total) * 100) : 0;
    overallEl.textContent = `${o.done} / ${o.total} chapters complete (${pct}%)`;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  if (!window.__sdn_init_called) renderProgressCards();
});
