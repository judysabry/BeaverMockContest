import sys
p=sys.argv[1]; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]); s=s.replace(a,b)

# new home
a=s.index('function weakPanel() {'); b=s.index('/* ---------- contest ---------- */')
s=s[:a]+r'''const TOPIC_HINT = { pat: "Spot the rule and continue it", logic: "Clues, true or false, who did what", algo: "Follow the instructions and trace what happens", ds: "Stacks, queues, sorting and storing", graph: "Routes, maps and connections", code: "Secret codes, binary and encoding", opt: "Best move, fewest steps, winning strategy" };
const PART_HINT = { A: "Warm-up questions", B: "Medium questions", C: "The hardest questions" };
const tone = p => p === 100 ? "ok" : p >= 70 ? "mid" : "low";
function statLine(x) {
  if (!x) return `<span class="cmeta">Not tried yet</span><div class="meter"><i style="width:0"></i></div>`;
  const p = pct(x.right, x.tried);
  return `<span class="cmeta"><b class="${tone(p)}">${p}%</b> · ${x.right}/${x.tried} right · ${mmss(Math.round(x.secs / x.tried))} avg</span><div class="meter ${tone(p)}"><i style="width:${p}%"></i></div>`;
}

/* ---------- home ---------- */
function renderHome() {
  const hist = store.get("bccMockHistory", []), w = weakPoints(), missed = missedList().length;
  const bestOf = name => { const xs = hist.filter(h => h.name === name); return xs.length ? Math.max(...xs.map(h => pct(h.score, h.max || 90))) : null; };
  const weakest = Object.entries(w.topic).filter(([, x]) => x.right < x.tried).sort((a, b) => a[1].right / a[1].tried - b[1].right / b[1].tried)[0];
  const mixedBest = bestOf("Mixed mock contest");
  const years = YEARS.map(y => { const b = bestOf(`${y} contest`); return `<button class="card year" data-pyear="${y}">
      <span class="ctitle">${y}</span>
      <span class="cmeta">${b === null ? "Not tried yet" : `Best <b class="${tone(b)}">${b}%</b>`}</span>
      <div class="meter ${b === null ? "" : tone(b)}"><i style="width:${b || 0}%"></i></div></button>`; }).join("");
  const topics = Object.keys(TOPICS).map(k => `<button class="card" data-ptopic="${k}">
      ${weakest && weakest[0] === k ? `<span class="badge">Weakest</span>` : ""}
      <span class="ctitle sm">${TOPICS[k]}</span>
      <span class="chint">${TOPIC_HINT[k]} · ${INDEX.filter(q => q.topic === k).length} questions</span>
      ${statLine(w.topic[k])}</button>`).join("");
  const parts = ["A", "B", "C"].map(p => `<button class="card" data-ppart="${p}">
      <span class="ctitle">Part ${p}</span>
      <span class="chint">${PART_HINT[p]} · ${POINTS[p]} points each</span>
      ${statLine(w.part[p])}</button>`).join("");
  app.innerHTML = `
    <header class="top">
      <span class="eyebrow">Beaver Computing Challenge · Grade 7/8</span>
      <h1>Mock Contest</h1>
      <p class="lede">Every real question from 2016 to 2025. Pick a card to start.</p>
      <div class="scorebar"><span><b>${POINTS.A}</b> Part A</span><span><b>${POINTS.B}</b> Part B</span><span><b>${POINTS.C}</b> Part C</span><span><b>${BLANK_POINTS}</b> left blank</span><span><b>0</b> wrong</span></div>
    </header>
    <div class="seg" role="radiogroup" aria-label="Timer">
      <span class="seglabel">3-minute timer</span>
      <label><input type="radio" name="strict" value="1" ${state.strict ? "checked" : ""}><span>Locks at 3:00</span></label>
      <label><input type="radio" name="strict" value="0" ${state.strict ? "" : "checked"}><span>Warning only</span></label>
    </div>
    <section class="heroes">
      <button class="card hero" data-pmixed="1">
        <span class="eyebrow">The full experience</span>
        <span class="ctitle">Mixed mock contest</span>
        <span class="chint">15 questions, 5 from each part, drawn from different years. 45 minutes. A new mix every time.</span>
        <span class="row spread"><span class="go">Start →</span><span class="cmeta">${mixedBest === null ? "" : `Best ${mixedBest}%`}</span></span>
      </button>
      <button class="card hero alt" data-pmissed="1" ${missed ? "" : "disabled"}>
        <span class="eyebrow">Road to 100%</span>
        <span class="ctitle">${missed} missed</span>
        <span class="chint">${missed ? "Redo the questions you last got wrong or left blank. Get one right and it comes off the list." : "Questions you get wrong or leave blank will wait here for a second try."}</span>
        <span class="go">${missed ? "Redo them →" : "Nothing to redo"}</span>
      </button>
    </section>
    <section class="shelf"><div class="shelfhead"><h2>By contest</h2><span class="small muted">The exact paper from each year</span></div><div class="gallery years">${years}</div></section>
    <section class="shelf"><div class="shelfhead"><h2>By topic</h2><span class="small muted">Up to 15 questions on one skill</span></div><div class="gallery topics">${topics}</div></section>
    <section class="shelf"><div class="shelfhead"><h2>By part</h2><span class="small muted">15 questions at one difficulty</span></div><div class="gallery parts3">${parts}</div></section>
    ${hist.length ? `<details class="panel"><summary>Your past scores (${hist.length})</summary>
      <div class="tablewrap"><table class="hist"><tr><th>Date</th><th>Contest</th><th>Score</th><th>Right</th><th>Wrong</th><th>Blank</th><th>Time</th></tr>
      ${hist.slice().reverse().slice(0, 15).map(h => `<tr><td>${new Date(h.at).toLocaleDateString()}</td><td>${esc(h.name)}</td><td><b>${h.score}</b>/${h.max || 90} · ${pct(h.score, h.max || 90)}%</td><td>${h.right}</td><td>${h.wrong}</td><td>${h.blank}</td><td>${mmss(h.seconds)}</td></tr>`).join("")}
      </table></div><div><button class="clear" data-clearhist="1">Clear my scores and history</button></div></details>` : ""}
    <p class="credit">Questions and solutions © Centre for Education in Mathematics and Computing, University of Waterloo, copied here for personal practice. Originals at <a href="https://cemc.uwaterloo.ca/resources/past-contests" target="_blank" rel="noopener">cemc.uwaterloo.ca</a>.</p>`;
}

'''+s[b:]

rep('''/* start screen */''','''/* front page gallery */
header.top { display: flex; flex-direction: column; gap: 8px; }
.scorebar { display: flex; flex-wrap: wrap; gap: 6px 8px; margin-top: 4px; }
.scorebar span { background: var(--surface); border: 1.5px solid var(--line); border-radius: 999px; padding: 3px 12px 3px 10px; font-size: 13px; color: var(--muted); }
.scorebar b { font: 700 14px var(--mono); color: var(--ink); margin-right: 4px; }
.seg { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; }
.seglabel { font-size: 14px; color: var(--muted); margin-right: 4px; }
.seg label { cursor: pointer; }
.seg input { position: absolute; opacity: 0; }
.seg label span { display: block; border: 1.5px solid var(--line); border-radius: 999px; padding: 5px 14px; font-size: 14px; background: var(--surface); }
.seg input:checked + span { background: var(--water); border-color: var(--water); color: var(--surface); font-weight: 700; }
.seg input:focus-visible + span { outline: 3px solid var(--water); outline-offset: 2px; }
.heroes { display: grid; grid-template-columns: 3fr 2fr; gap: 12px; }
.shelf { display: flex; flex-direction: column; gap: 10px; }
.shelfhead { display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 12px; }
.gallery { display: grid; gap: 10px; }
.gallery.years { grid-template-columns: repeat(5, 1fr); }
.gallery.topics { grid-template-columns: repeat(4, 1fr); }
.gallery.parts3 { grid-template-columns: repeat(3, 1fr); }
.card { position: relative; text-align: left; background: var(--surface); color: var(--ink); border: 1.5px solid var(--line); border-radius: 14px; padding: 14px; display: flex; flex-direction: column; gap: 6px; min-width: 0; transition: transform .15s, border-color .15s, box-shadow .15s; }
.card:hover:not(:disabled) { border-color: var(--water); transform: translateY(-2px); box-shadow: 0 6px 16px rgb(0 0 0 / .08); }
.card:disabled { opacity: .6; cursor: default; }
.ctitle { font-weight: 800; font-size: 26px; line-height: 1.1; letter-spacing: -0.01em; }
.ctitle.sm { font-size: 16px; line-height: 1.25; }
.chint { font-size: 13px; color: var(--muted); line-height: 1.4; flex: 1; }
.cmeta { font-size: 12px; color: var(--muted); font-variant-numeric: tabular-nums; }
.cmeta b.ok { color: var(--good); } .cmeta b.mid { color: var(--warn); } .cmeta b.low { color: var(--bad); }
.meter { height: 6px; border-radius: 3px; background: var(--water-soft); overflow: hidden; }
.meter i { display: block; height: 100%; background: var(--water); }
.meter.ok i { background: var(--good); } .meter.mid i { background: var(--warn); } .meter.low i { background: var(--bad); }
.badge { position: absolute; top: -9px; right: 10px; background: var(--bad); color: var(--surface); font: 700 11px var(--mono); border-radius: 999px; padding: 2px 8px; }
.card.hero { padding: 20px; gap: 8px; background: var(--water-soft); border-color: var(--water); }
.card.hero .ctitle { font-size: 30px; }
.card.hero .chint { font-size: 14px; color: var(--ink); }
.card.hero.alt { background: var(--surface); border-color: var(--line); }
.card.hero.alt .chint { color: var(--muted); }
.go { align-self: flex-start; background: var(--accent); color: var(--accent-ink); font-weight: 700; border-radius: 10px; padding: 8px 16px; }
.card.hero.alt .go { background: transparent; color: var(--ink); border: 1.5px solid var(--line); }
@media (max-width: 640px) { .heroes { grid-template-columns: 1fr; } .gallery.years { grid-template-columns: repeat(3, 1fr); } .gallery.topics { grid-template-columns: repeat(2, 1fr); } .gallery.parts3 { grid-template-columns: 1fr; } }
@media (prefers-reduced-motion: reduce) { .card { transition: none; } }

/* start screen */''')
rep('''[data-ptopic],[data-ppart],[data-pmissed],[data-savefile]"''','''[data-ptopic],[data-ppart],[data-pmissed],[data-pmixed],[data-pyear],[data-savefile]"''')
rep('''  else if (d.pmissed) {''','''  else if (d.pmixed) { state.mode = "mixed"; start(); }
  else if (d.pyear) { state.mode = "year"; state.year = +d.pyear; start(); }
  else if (d.pmissed) {''')
rep('''<button class="btn ghost" data-go="home">← Home</button><button class="btn" data-start="1">New contest</button>''','''<button class="btn ghost" data-go="home">← Home</button><button class="btn" data-start="1">Another one like this</button>''')
assert s.count('function renderHome()')==1
open(p,'w').write(s)
