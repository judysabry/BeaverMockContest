import sys
p=sys.argv[1]; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]); s=s.replace(a,b)
rep('''const TABS = [["plan", "My plan"], ["contest", "By contest"],''','''/* Every question you have ever got wrong or left blank, from both grade levels. */
function mistakeRows() {
  const log = getLog();
  return ALL.map(q => {
    const a = log[keyOf(q)]; if (!a) return null;
    const bad = a.filter(x => !x.ok); if (!bad.length) return null;
    const lastBad = bad[bad.length - 1];
    return { q, times: bad.length, tries: a.length, fixed: a[a.length - 1].ok, pick: lastBad.pick, at: lastBad.at };
  }).filter(Boolean).sort((a, b) => b.at - a.at);
}
function mistakesPanel() {
  const all = mistakeRows(), open = all.filter(r => !r.fixed), f = state.mfilter || "open";
  if (!all.length) return `<div class="panel"><h3>No mistakes saved yet</h3><p class="muted">Every question you get wrong or leave blank is saved here automatically, with your answer, the right answer and the official explanation.</p></div>`;
  const rows = f === "open" ? open : f === "fixed" ? all.filter(r => r.fixed) : all;
  const groups = {};
  rows.forEach(r => (groups[r.q.topic] = groups[r.q.topic] || []).push(r));
  const here = missedList().length;
  return `<div class="panel">
      <div class="row spread"><h3>${open.length} still to fix · ${all.length - open.length} fixed</h3>
        ${here ? `<button class="btn" data-pmissed="1">Redo ${here} as a quiz</button>` : ""}</div>
      <div class="seg" role="radiogroup" aria-label="Which mistakes to show">
        ${[["open", `Still to fix (${open.length})`], ["fixed", `Fixed (${all.length - open.length})`], ["all", `All (${all.length})`]].map(([k, l]) => `<label><input type="radio" name="mfilter" value="${k}" ${f === k ? "checked" : ""}><span>${l}</span></label>`).join("")}
      </div>
      <p class="small muted">Click a question to open it with your answer, the right answer and the explanation. A question moves to "Fixed" once you answer it correctly in a later quiz.</p>
    </div>
    ${rows.length ? Object.entries(groups).sort((a, b) => b[1].length - a[1].length).map(([t, rs]) => `<div class="panel mgroup"><div class="row spread"><h3>${TOPICS[t]}</h3><span class="small muted">${rs.length} question${rs.length === 1 ? "" : "s"}</span></div>
      ${rs.map(r => `<details class="mrow" data-mkey="${keyOf(r.q)}" data-mpick="${r.pick ?? -1}">
        <summary><span class="mtitle">${esc(r.q.title)}</span>
          <span class="small muted">${r.q.y} ${gradeName(lvOf(r.q))} · Part ${r.q.part} · ${r.pick == null ? "left blank" : `you picked (${LETTERS[r.pick]})`} · missed ${r.times} time${r.times === 1 ? "" : "s"} · ${new Date(r.at).toLocaleDateString()}</span>
          <span class="pill ${r.fixed ? "ok" : "no"}">${r.fixed ? "✓ Fixed" : "To fix"}</span></summary>
        <div class="mbody"><p class="muted">Loading…</p></div></details>`).join("")}</div>`).join("") : `<div class="panel"><p class="muted">Nothing in this list.</p></div>`}`;
}
async function openMistake(el) {
  if (!el.open || el.dataset.loaded) return;
  el.dataset.loaded = "1";
  const meta = ALL.find(q => keyOf(q) === el.dataset.mkey), body = el.querySelector(".mbody"), pick = +el.dataset.mpick;
  try {
    const q = await loadQ(meta);
    body.innerHTML = `${questionSheet(q, `${q.y} ${gradeName(lvOf(q))} · Part ${q.part} · ${POINTS[q.part]} points`)}
      <div class="verdict"><span class="${pick < 0 ? "blank" : "no"}">${pick < 0 ? "You left it blank" : `You picked (${LETTERS[pick]})`}</span><span>Answer: <b>(${LETTERS[q.answer]})</b></span></div>
      <div class="paper"><div class="solution missed"><span class="label">Answer</span>${q.answerHtml}${q.explanation ? `<span class="label">Explanation</span>${q.explanation}` : ""}</div>
      ${q.connections ? `<details><summary>Connections to computer science</summary>${q.connections}</details>` : ""}</div>`;
    optionList(body).forEach((li, k) => { if (k === q.answer) li.classList.add("right"); else if (k === pick) li.classList.add("wrong"); });
    typeset(body);
  } catch (e) { body.innerHTML = `<p class="muted">Couldn't load this question. Keep index.html next to the q folder.</p>`; delete el.dataset.loaded; }
}
app.addEventListener("toggle", e => { if (e.target.matches && e.target.matches("details.mrow")) openMistake(e.target); }, true);
const TABS = [["plan", "My plan"], ["mistakes", "My mistakes"], ["contest", "By contest"],''')
rep('''plan: "Seven steps from where you are now''','''mistakes: "Every question you got wrong or left blank, saved automatically from both grade levels.", plan: "Seven steps from where you are now''')
rep('''      ${tab === "plan" ? planPanel() :''','''      ${tab === "plan" ? planPanel() : tab === "mistakes" ? mistakesPanel() :''')
rep('''  else if (e.target.name === "level") {''','''  else if (e.target.name === "mfilter") { state.mfilter = e.target.value; renderHome(); }
  else if (e.target.name === "level") {''')
rep('''/* plan */''','''/* mistakes */
.mgroup { gap: 8px; }
.mrow { border: 1.5px solid var(--line); border-radius: 10px; }
.mrow > summary { list-style: none; display: grid; grid-template-columns: 1fr auto; gap: 2px 12px; align-items: center; padding: 10px 14px; color: var(--ink); font-weight: 400; }
.mrow > summary::-webkit-details-marker { display: none; }
.mrow > summary .mtitle { font-weight: 700; }
.mrow > summary .mtitle::before { content: "▸ "; color: var(--muted); }
.mrow[open] > summary .mtitle::before { content: "▾ "; }
.mrow > summary .pill { grid-column: 2; grid-row: 1 / span 2; }
.mrow[open] { border-color: var(--water); }
.mbody { padding: 0 14px 14px; display: flex; flex-direction: column; gap: 10px; }
.tabs { scrollbar-width: thin; }

/* plan */''')
open(p,'w').write(s)
