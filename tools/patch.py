import sys
p=sys.argv[1]; s=open(p).read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(s.count(a),a[:70])
    s=s.replace(a,b)

rep('''const TOTAL = 45 * 60;                 // 15 questions x 3 minutes
const MAX_SCORE = 5 * (POINTS.A + POINTS.B + POINTS.C);
''','''const maxOf = items => items.reduce((s, q) => s + POINTS[q.part], 0);
const pct = (a, b) => b ? Math.round(a / b * 100) : 0;
''')
rep('''mode: "mixed", year: YEARS[0], strict''','''mode: "mixed", year: YEARS[0], topic: "algo", part: "A", strict''')

a=s.index('/* Mixed mock:'); b=s.index('/* ---------- home ---------- */')
s=s[:a]+r'''const keyOf = q => `${q.y}-${q.n}`;
const byPart = (a, b) => a.part.localeCompare(b.part);
const getLog = () => store.get("bccMockLog", {});   // every answer you've given, per question
/* Take n questions from a pool, using ones you haven't seen first. */
function take(pool, n) {
  const seen = new Set(store.get("bccMockSeen", []));
  return [...shuffle(pool.filter(q => !seen.has(keyOf(q)))), ...shuffle(pool.filter(q => seen.has(keyOf(q))))].slice(0, n);
}
/* Mixed mock: 5 real questions from each part, from different years where possible. */
function pickMixed() {
  const out = [];
  for (const part of "ABC") {
    const ranked = take(INDEX.filter(q => q.part === part), 999), chosen = [], years = new Set();
    for (const q of ranked) if (chosen.length < 5 && !years.has(q.y)) { chosen.push(q); years.add(q.y); }
    for (const q of ranked) if (chosen.length < 5 && !chosen.includes(q)) chosen.push(q);
    out.push(...chosen);
  }
  return out;
}
/* Questions whose most recent answer was wrong or blank. */
function missedList() {
  const log = getLog();
  return INDEX.filter(q => { const a = log[keyOf(q)]; return a && a.length && !a[a.length - 1].ok; });
}
function choose() {
  const m = state.mode;
  if (m === "mixed") return [pickMixed(), "Mixed mock contest"];
  if (m === "year") return [INDEX.filter(q => q.y === state.year).sort((a, b) => a.n - b.n), `${state.year} contest`];
  if (m === "topic") return [take(INDEX.filter(q => q.topic === state.topic), 15).sort(byPart), `Topic: ${TOPICS[state.topic]}`];
  if (m === "part") return [take(INDEX.filter(q => q.part === state.part), 15), `Part ${state.part} practice`];
  return [shuffle(missedList()).slice(0, 15).sort(byPart), "Missed questions"];
}

async function start() {
  const [picked, name] = choose();
  if (!picked.length) { alert("No missed questions right now. Nice!"); return; }
  app.innerHTML = `<p class="loading">Getting your contest ready…</p>`;
  let items;
  try { items = await Promise.all(picked.map(q => loadQ(q.y, q.n))); }
  catch (e) {
    app.innerHTML = `<div class="panel"><h2>Couldn't load the questions</h2><p>Keep <b>index.html</b> in the same folder as the <b>q</b> folder, then open it again.</p><div><button class="btn" data-go="home">Back</button></div></div>`;
    return;
  }
  state.quiz = {
    name, mode: state.mode, strict: state.strict, items, idx: 0, total: items.length * PER_QUESTION,
    picks: items.map(() => null), spent: items.map(() => 0), locked: items.map(() => false),
    elapsed: 0, last: Date.now()
  };
  state.view = "quiz"; renderQuiz(); window.scrollTo(0, 0);
}

/* Weak points: your newest answer to every question you've tried, grouped by topic and by part. */
function weakPoints() {
  const log = getLog(), topic = {}, part = {};
  let tried = 0;
  INDEX.forEach(q => {
    const a = log[keyOf(q)]; if (!a || !a.length) return;
    const last = a[a.length - 1]; tried++;
    for (const [g, k] of [[topic, q.topic], [part, q.part]]) {
      const x = g[k] = g[k] || { tried: 0, right: 0, secs: 0 };
      x.tried++; x.right += last.ok ? 1 : 0; x.secs += last.spent || 0;
    }
  });
  return { tried, topic, part };
}
function weakPanel() {
  const w = weakPoints(), missed = missedList().length;
  if (!w.tried) return `<section class="panel"><h2>Your weak points</h2><p class="muted">Finish a contest and this will show how you're doing in each topic and each part, weakest first.</p></section>`;
  const rows = (g, label, attr) => Object.entries(g).sort((a, b) => a[1].right / a[1].tried - b[1].right / b[1].tried || b[1].tried - a[1].tried).map(([k, x]) => {
    const p = pct(x.right, x.tried);
    return `<tr><td>${label(k)}</td><td>${x.right}/${x.tried}</td><td class="${p === 100 ? "ok" : p >= 70 ? "blank" : "no"}">${p}%</td><td>${mmss(Math.round(x.secs / x.tried))}</td><td><button class="clear" ${attr}="${k}">Practise</button></td></tr>`;
  }).join("");
  return `<section class="panel"><div class="row spread"><h2>Your weak points</h2><span class="small muted">${w.tried} of ${INDEX.length} questions tried</span></div>
    <div class="tablewrap"><table class="sheet"><tr><th>Topic (weakest first)</th><th>Right</th><th>%</th><th>Avg time</th><th></th></tr>${rows(w.topic, k => TOPICS[k], "data-ptopic")}</table></div>
    <div class="tablewrap"><table class="sheet"><tr><th>Part</th><th>Right</th><th>%</th><th>Avg time</th><th></th></tr>${rows(w.part, k => "Part " + k, "data-ppart")}</table></div>
    ${missed ? `<div class="row"><button class="btn" data-pmissed="1">Redo my ${missed} missed question${missed === 1 ? "" : "s"}</button><span class="small muted">Get one right and it comes off the list.</span></div>` : `<p class="small muted">No missed questions waiting. Everything you've tried, you've now got right.</p>`}
  </section>`;
}

'''+s[b:]

rep('''<p class="small muted">A wrong answer scores 0, so if you really can't narrow it down, leaving it blank is worth more than a wild guess. Maximum score: ${MAX_SCORE}.</p>
    </section>''','''<p class="small muted">A wrong answer scores 0, so if you really can't narrow it down, leaving it blank is worth more than a wild guess. A full contest is out of 90.</p>
    </section>
    ${weakPanel()}''')
rep('''<h2>Which contest?</h2>''','''<h2>What do you want to practise?</h2>''')
rep('''${YEARS.map(y => `<option ${y === state.year ? "selected" : ""}>${y}</option>`).join("")}</select></small></span></label>
''','''${YEARS.map(y => `<option ${y === state.year ? "selected" : ""}>${y}</option>`).join("")}</select></small></span></label>
        <label class="opt"><input type="radio" name="mode" value="topic" ${state.mode === "topic" ? "checked" : ""}><span><b>One topic</b><small>Up to 15 questions about <select id="topic" aria-label="Topic">${Object.entries(TOPICS).map(([k, v]) => `<option value="${k}" ${k === state.topic ? "selected" : ""}>${v} (${INDEX.filter(q => q.topic === k).length})</option>`).join("")}</select></small></span></label>
        <label class="opt"><input type="radio" name="mode" value="part" ${state.mode === "part" ? "checked" : ""}><span><b>One part</b><small>15 questions all from <select id="part" aria-label="Part">${["A", "B", "C"].map(p => `<option value="${p}" ${p === state.part ? "selected" : ""}>Part ${p} (${p === "A" ? "easiest" : p === "B" ? "medium" : "hardest"})</option>`).join("")}</select></small></span></label>
        <label class="opt"><input type="radio" name="mode" value="missed" ${state.mode === "missed" ? "checked" : ""}><span><b>Missed questions</b><small>Redo the questions you last got wrong or left blank (${missedList().length} waiting).</small></span></label>
''')
rep('''The 3:00 clock turns red when you go over, but nothing locks. The contest still ends at 45:00.''','''The 3:00 clock turns red when you go over, but nothing locks. The contest still ends when the whole-contest clock runs out (45:00 for 15 questions).''')
rep('''<td><b>${h.score}</b>/${MAX_SCORE}</td>''','''<td><b>${h.score}</b>/${h.max || 90} · ${pct(h.score, h.max || 90)}%</td>''')

# quiz strip
rep('''<div class="strip">${z.items.map(''','''<div class="strip ${std ? "std" : ""}" style="grid-template-columns:repeat(${z.items.length},1fr)">${z.items.map(''')
rep('''<div class="striplabels"><span>Part A · ${POINTS.A} pts</span><span>Part B · ${POINTS.B} pts</span><span>Part C · ${POINTS.C} pts</span></div>''','''${std ? `<div class="striplabels"><span>Part A · ${POINTS.A} pts</span><span>Part B · ${POINTS.B} pts</span><span>Part C · ${POINTS.C} pts</span></div>` : ""}''')
rep('''const z = state.quiz, i = z.idx, q = z.items[i], locked = z.locked[i];''','''const z = state.quiz, i = z.idx, q = z.items[i], locked = z.locked[i];
  const std = z.items.length === 15 && z.items.map(x => x.part).join("") === "AAAAABBBBBCCCCC";''')
rep('''.dot:nth-child(5), .dot:nth-child(10) { margin-right: 6px; }''','''.strip.std .dot:nth-child(5), .strip.std .dot:nth-child(10) { margin-right: 6px; }''')
rep('''total = TOTAL - Math.floor(z.elapsed)''','''total = z.total - Math.floor(z.elapsed)''')
rep('''Math.max(0, total / TOTAL * 100)''','''Math.max(0, total / z.total * 100)''')
rep('''if (z.elapsed >= TOTAL) return finish(true);''','''if (z.elapsed >= z.total) return finish(true);''')

# finish
a=s.index('function finish(timeUp) {'); b=s.index('/* ---------- results ---------- */')
s=s[:a]+r'''function finish(timeUp) {
  const z = state.quiz;
  const rows = z.items.map((q, i) => ({ q, i, pick: z.picks[i], spent: Math.round(z.spent[i]), pts: pointsFor(q, z.picks[i]), kind: z.picks[i] === null ? "blank" : z.picks[i] === q.answer ? "ok" : "no" }));
  const r = {
    name: z.name, mode: z.mode, timeUp, rows, at: Date.now(), seconds: Math.min(z.total, Math.round(z.elapsed)),
    score: rows.reduce((s, x) => s + x.pts, 0), max: maxOf(z.items),
    right: rows.filter(x => x.kind === "ok").length, wrong: rows.filter(x => x.kind === "no").length, blank: rows.filter(x => x.kind === "blank").length
  };
  state.result = r; state.quiz = null;
  const hist = store.get("bccMockHistory", []);
  hist.push({ at: r.at, name: r.name, score: r.score, max: r.max, right: r.right, wrong: r.wrong, blank: r.blank, seconds: r.seconds });
  store.set("bccMockHistory", hist);
  const log = getLog(), seen = new Set(store.get("bccMockSeen", []));
  rows.forEach(x => { const k = keyOf(x.q); (log[k] = log[k] || []).push({ at: r.at, pick: x.pick, ok: x.kind === "ok", spent: x.spent }); seen.add(k); });
  store.set("bccMockLog", log); store.set("bccMockSeen", [...seen]);
  saveResultFile(r);
  state.view = "results"; renderResults(); window.scrollTo(0, 0);
}
/* Saves a small results file to your Downloads folder so Claude can read your answers. */
function saveResultFile(r) {
  try {
    const d = new Date(r.at), two = n => String(n).padStart(2, "0");
    const stamp = `${d.getFullYear()}${two(d.getMonth() + 1)}${two(d.getDate())}-${two(d.getHours())}${two(d.getMinutes())}${two(d.getSeconds())}`;
    const data = {
      app: "beaver-mock-contest", finished: d.toISOString(), contest: r.name, mode: r.mode, timeRanOut: r.timeUp,
      score: r.score, max: r.max, percent: pct(r.score, r.max), right: r.right, wrong: r.wrong, blank: r.blank, secondsUsed: r.seconds,
      questions: r.rows.map(x => ({ number: x.i + 1, year: x.q.y, yearQuestion: x.q.n, part: x.q.part, topic: x.q.topic, title: x.q.title, picked: x.pick === null ? null : LETTERS[x.pick], answer: LETTERS[x.q.answer], result: x.kind === "ok" ? "correct" : x.kind === "no" ? "wrong" : "blank", points: x.pts, seconds: x.spent }))
    };
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([JSON.stringify(data, null, 1)], { type: "application/json" }));
    a.download = `beaver-result-${stamp}.json`;
    document.body.append(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 5000);
  } catch (e) {}
}

'''+s[b:]

rep('''<div class="score"><span class="n">${r.score}</span><span class="of">/ ${MAX_SCORE}</span></div>''','''<div class="score"><span class="n">${pct(r.score, r.max)}%</span><span class="of">${r.score} / ${r.max} points</span></div>
      <div class="row"><span class="small muted">A results file was saved to your Downloads folder so Claude can check your answers.</span><button class="clear" data-savefile="1">Save it again</button></div>''')
rep('''<div class="parts">${["A", "B", "C"].map(part).join("")}</div>''','''<div class="parts">${["A", "B", "C"].filter(p => r.rows.some(x => x.q.part === p)).map(part).join("")}</div>''')
rep('''Topics to practise (questions not answered correctly):</p><div class="tally">${Object.entries(topics).sort((a, b) => b[1] - a[1]).map(([t, n]) => `<span class="pill topic">${TOPICS[t]} · ${n}</span>`).join("")}</div></div>` : `<p>Every answer right. Excellent work.</p>`}''','''Topics to practise (questions not answered correctly):</p><div class="tally">${Object.entries(topics).sort((a, b) => b[1] - a[1]).map(([t, n]) => `<span class="pill topic">${TOPICS[t]} · ${n}</span>`).join("")}</div></div>
        <div><button class="btn" data-pmissed="1">Redo the ones I missed</button></div>` : `<p><b>100%. Every answer right.</b> Excellent work.</p>`}''')
rep('''.parts { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }''','''.parts { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; }''')

# events
rep('''else if (e.target.id === "year") { state.year = +e.target.value; state.mode = "year"; const r = app.querySelector('input[name="mode"][value="year"]'); if (r) r.checked = true; }''','''else if (["year", "topic", "part"].includes(e.target.id)) {
    const id = e.target.id; state[id] = id === "year" ? +e.target.value : e.target.value; state.mode = id;
    const r = app.querySelector(`input[name="mode"][value="${id}"]`); if (r) r.checked = true;
  }''')
rep('''"[data-start],[data-go],[data-pick],[data-nav],[data-jump],[data-submit],[data-quit],[data-clearhist]"''','''"[data-start],[data-go],[data-pick],[data-nav],[data-jump],[data-submit],[data-quit],[data-clearhist],[data-ptopic],[data-ppart],[data-pmissed],[data-savefile]"''')
rep('''  if (d.start) start();
''','''  if (d.start) start();
  else if (d.ptopic) { state.mode = "topic"; state.topic = d.ptopic; start(); }
  else if (d.ppart) { state.mode = "part"; state.part = d.ppart; start(); }
  else if (d.pmissed) { state.mode = "missed"; start(); }
  else if (d.savefile) saveResultFile(state.result);
''')
rep('''if (confirm("Clear your past scores?")) { store.set("bccMockHistory", []); renderHome(); }''','''if (confirm("Clear your past scores and weak-point history?")) { store.set("bccMockHistory", []); store.set("bccMockLog", {}); renderHome(); }''')
assert 'MAX_SCORE' not in s and 'TOTAL' not in s
open(p,'w').write(s)
