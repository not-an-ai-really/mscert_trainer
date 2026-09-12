/* MS-Cert Trainer — PWA logic. Vanilla JS, no dependencies, fully
   client-side: the question bank ships in bank.js and all progress
   lives in localStorage. Works offline once loaded (see sw.js). */
"use strict";

const APP_VERSION = "1.1.0";

const DOMAIN_LABELS = {
  conceptual: "Concepts",
  clinical: "Assessment & Intervention",
  advocacy: "Advocacy",
  education: "Education",
  research: "Research",
};
const DOMAIN_ORDER = ["clinical", "conceptual", "advocacy", "education", "research"];
const LETTERS = "ABCDE";
const PROGRESS_KEY = "mscert.progress.v1";

const $ = (s) => document.querySelector(s);

const views = {
  home: $("#view-home"),
  quiz: $("#view-quiz"),
  results: $("#view-results"),
};

const state = {
  domains: [],
  diffs: [],
  count: 10,
  questions: [],
  idx: 0,
  answers: [], // {qid, domain, chosen, correct, ok}
  missedIds: [],
  sessionFromMisses: false,
};

/* ------------------------------------------------------------- progress */

function loadProgress() {
  try {
    const raw = localStorage.getItem(PROGRESS_KEY);
    if (!raw) return null;
    const p = JSON.parse(raw);
    if (typeof p !== "object" || !p) return null;
    return p;
  } catch (e) {
    return null;
  }
}

function saveProgress(p) {
  try {
    localStorage.setItem(PROGRESS_KEY, JSON.stringify(p));
  } catch (e) {
    /* private mode / quota — progress simply not persisted */
  }
}

function recordAttempt(domain, ok) {
  const p = loadProgress() || {
    n: 0, ok: 0,
    domains: {
      clinical: { n: 0, ok: 0 }, conceptual: { n: 0, ok: 0 },
      advocacy: { n: 0, ok: 0 }, education: { n: 0, ok: 0 },
      research: { n: 0, ok: 0 },
    },
  };
  p.n += 1;
  if (ok) p.ok += 1;
  if (!p.domains[domain]) p.domains[domain] = { n: 0, ok: 0 };
  p.domains[domain].n += 1;
  if (ok) p.domains[domain].ok += 1;
  saveProgress(p);
  return p;
}

function renderProgressStrip() {
  const p = loadProgress();
  const strip = $("#progress-strip");
  if (!p || !p.n) {
    strip.hidden = true;
    $("#reset-progress").hidden = true;
    return;
  }
  strip.hidden = false;
  $("#reset-progress").hidden = false;
  $("#ps-accuracy").textContent = Math.round((p.ok / p.n) * 100) + "%";
  $("#ps-attempts").textContent = p.n;
  let worst = null, worstName = "–";
  for (const d of DOMAIN_ORDER) {
    const s = p.domains[d];
    if (!s || !s.n) continue;
    const acc = s.ok / s.n;
    if (worst === null || acc < worst) {
      worst = acc;
      worstName = (DOMAIN_LABELS[d] || d).split(" ")[0];
    }
  }
  $("#ps-weakest").textContent = worstName;
}

/* -------------------------------------------------------------- filters */

function poolCount() {
  return QUESTION_BANK.filter((q) =>
    (state.domains.length === 0 || state.domains.includes(q.domain)) &&
    (state.diffs.length === 0 || state.diffs.includes(q.difficulty))
  ).length;
}

function updatePoolHint() {
  const n = poolCount();
  $("#pool-hint").textContent = n
    ? n + " questions match your filters"
    : "No questions match those filters.";
}

function buildDomainChips() {
  const wrap = $("#domain-filters");
  wrap.innerHTML = "";
  for (const key of DOMAIN_ORDER) {
    const n = QUESTION_BANK.filter((q) => q.domain === key).length;
    const b = document.createElement("button");
    b.className = "chip";
    b.innerHTML =
      `${DOMAIN_LABELS[key]} <small>(${n})</small>`;
    b.onclick = () => {
      const i = state.domains.indexOf(key);
      if (i >= 0) state.domains.splice(i, 1);
      else state.domains.push(key);
      b.classList.toggle("on");
      updatePoolHint();
    };
    wrap.appendChild(b);
  }
  for (const chip of document.querySelectorAll("#difficulty-filters .chip")) {
    chip.onclick = () => {
      const v = chip.dataset.diff;
      const i = state.diffs.indexOf(v);
      if (i >= 0) state.diffs.splice(i, 1);
      else state.diffs.push(v);
      chip.classList.toggle("on");
      updatePoolHint();
    };
  }
}

/* ----------------------------------------------------------------- quiz */

function pickQuestions(count, onlyIds) {
  const idset = onlyIds ? new Set(onlyIds) : null;
  const pool = QUESTION_BANK.filter((q) =>
    (!idset || idset.has(q.id)) &&
    (state.domains.length === 0 || state.domains.includes(q.domain)) &&
    (state.diffs.length === 0 || state.diffs.includes(q.difficulty))
  );
  for (let i = pool.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [pool[i], pool[j]] = [pool[j], pool[i]];
  }
  return pool.slice(0, count);
}

function show(view) {
  for (const k in views) views[k].hidden = k !== view;
}

function startQuiz(onlyIds) {
  state.questions = pickQuestions(state.count, onlyIds);
  if (!state.questions.length) {
    alert("No questions match those filters — relax the filters and retry.");
    return;
  }
  state.idx = 0;
  state.answers = [];
  state.missedIds = [];
  state.sessionFromMisses = !!onlyIds;
  show("quiz");
  renderQuestion();
}

function renderQuestion() {
  const q = state.questions[state.idx];
  $("#progress-bar").style.width =
    (state.idx / state.questions.length) * 100 + "%";
  $("#progress-label").textContent =
    (state.idx + 1) + " / " + state.questions.length;
  $("#quiz-tags").innerHTML =
    `<span class="tag">${DOMAIN_LABELS[q.domain] || q.domain}</span>` +
    `<span class="tag" data-d="${q.difficulty}">${q.difficulty}</span>` +
    (state.sessionFromMisses ? `<span class="tag">review</span>` : "");
  $("#stem").textContent = q.stem;

  const box = $("#options");
  box.classList.remove("locked");
  box.innerHTML = "";
  q.options.forEach((opt, i) => {
    const b = document.createElement("button");
    b.className = "opt";
    const letter = document.createElement("span");
    letter.className = "letter";
    letter.textContent = LETTERS[i] || "?";
    const text = document.createElement("span");
    text.textContent = opt;
    b.appendChild(letter);
    b.appendChild(text);
    b.onclick = () => answer(i, b);
    box.appendChild(b);
  });

  $("#explanation").hidden = true;
  $("#next-btn").hidden = true;
}

function answer(choice, btn) {
  const q = state.questions[state.idx];
  const correct = q.correct_answer;
  const ok = choice === correct;

  $("#options").classList.add("locked");
  const all = document.querySelectorAll("#options .opt");
  all.forEach((o, i) => {
    if (i === correct) o.classList.add("correct");
    else if (i === choice) o.classList.add("wrong");
  });

  state.answers.push({
    qid: q.id, domain: q.domain,
    chosen: choice, correct, ok,
  });
  if (!ok) state.missedIds.push(q.id);
  recordAttempt(q.domain, ok);

  const banner = $("#result-banner");
  banner.className = "banner " + (ok ? "ok" : "no");
  banner.textContent = ok
    ? "Correct."
    : "Incorrect — the answer is " + (LETTERS[correct] || "?") + ".";
  $("#rationale").textContent = q.rationale;
  $("#explanation").hidden = false;
  const next = $("#next-btn");
  next.hidden = false;
  next.textContent = state.idx + 1 >= state.questions.length
    ? "See results"
    : "Next →";
  next.scrollIntoView({ block: "nearest" });
}

/* --------------------------------------------------------------- results */

function renderResults() {
  const total = state.answers.length;
  const correct = state.answers.filter((a) => a.ok).length;
  const pct = total ? Math.round((correct / total) * 100) : 0;
  $("#score-pct").textContent = pct + "%";
  $("#score-frac").textContent = correct + " of " + total + " correct";
  const ring = $("#ring-fg");
  const circ = 2 * Math.PI * 52;
  ring.style.strokeDasharray = String(circ);
  ring.style.strokeDashoffset = String(circ);
  ring.style.stroke = pct >= 70 ? "var(--good)" : pct >= 50 ? "var(--warn)" : "var(--bad)";
  requestAnimationFrame(() => {
    ring.style.strokeDashoffset = String(circ * (1 - pct / 100));
  });

  const byDomain = {};
  for (const a of state.answers) {
    byDomain[a.domain] = byDomain[a.domain] || { ok: 0, n: 0 };
    byDomain[a.domain].n += 1;
    if (a.ok) byDomain[a.domain].ok += 1;
  }
  const bd = $("#breakdown");
  bd.innerHTML = "";
  for (const d of DOMAIN_ORDER) {
    const s = byDomain[d];
    if (!s) continue;
    const row = document.createElement("div");
    row.className = "bd-row";
    const span = document.createElement("span");
    span.textContent = DOMAIN_LABELS[d] || d;
    const frac = document.createElement("span");
    frac.className = "frac " + (s.ok === s.n ? "good" : s.ok / s.n >= 0.5 ? "warn" : "bad");
    frac.textContent = s.ok + " / " + s.n + " · " + Math.round((s.ok / s.n) * 100) + "%";
    row.appendChild(span);
    row.appendChild(frac);
    bd.appendChild(row);
  }

  $("#progress-bar").style.width = "100%";
  const retry = $("#retry-missed-btn");
  if (state.missedIds.length) {
    retry.hidden = false;
    retry.textContent = "Review " + state.missedIds.length + " missed";
  } else {
    retry.hidden = true;
  }
  show("results");
  renderProgressStrip();
}

/* ---------------------------------------------------------------- misc */

function registerSW() {
  if (!("serviceWorker" in navigator) || !window.isSecureContext) return;
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("sw.js").catch(() => {
      /* http on a LAN IP or file:// — app still works, just no install */
    });
  });
  const note = $("#offline-note");
  const showNote = () => { note.hidden = navigator.onLine; };
  window.addEventListener("online", showNote);
  window.addEventListener("offline", showNote);
  showNote();
}

function init() {
  if (typeof QUESTION_BANK === "undefined" || !Array.isArray(QUESTION_BANK) || !QUESTION_BANK.length) {
    document.body.innerHTML =
      "<p style='padding:20px'>Question bank failed to load (js/bank.js). " +
      "Regenerate it with tools\\build_bank_js.py.</p>";
    return;
  }
  $("#ver").textContent = "v" + APP_VERSION;
  $("#bank-tag").textContent = QUESTION_BANK.length + " questions";
  buildDomainChips();
  updatePoolHint();
  renderProgressStrip();

  $("#count-up").onclick = () => {
    state.count = Math.min(50, state.count + 5);
    $("#count-val").textContent = String(state.count);
  };
  $("#count-down").onclick = () => {
    state.count = Math.max(5, state.count - 5);
    $("#count-val").textContent = String(state.count);
  };
  $("#start-btn").onclick = () => startQuiz(null);
  $("#next-btn").onclick = () => {
    state.idx += 1;
    if (state.idx >= state.questions.length) renderResults();
    else renderQuestion();
  };
  $("#quit-btn").onclick = () => {
    if (window.confirm("Quit this session? Progress so far is kept.")) {
      renderProgressStrip();
      show("home");
    }
  };
  $("#retry-missed-btn").onclick = () => startQuiz(state.missedIds.slice());
  const goSetup = () => {
    updatePoolHint();
    show("home");
  };
  $("#new-session-btn").onclick = () => startQuiz(null);
  $("#home-btn").onclick = goSetup;
  $("#reset-progress").onclick = () => {
    if (window.confirm("Forget all saved practice progress?")) {
      try { localStorage.removeItem(PROGRESS_KEY); } catch (e) { /* ignore */ }
      renderProgressStrip();
    }
  };
  registerSW();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
