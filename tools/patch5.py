import sys
p=sys.argv[1]; s=open(p).read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:80]); s=s.replace(a,b)

# ---------- levels ----------
rep('''const INDEX = window.BCC_INDEX || [];
const YEARS = [...new Set(INDEX.map(q => q.y))].sort((a, b) => b - a);''','''const ALL = window.BCC_INDEX || [];          // both grade levels
const lvOf = q => q.lv || "78";
let INDEX = [];                               // the questions for the grade level you're practising
const YEARS = [...new Set(ALL.map(q => q.y))].sort((a, b) => b - a);''')
rep('''window.BCC_Q = d => { Q[`${d.y}-${d.n}`] = d; };''','''window.BCC_Q = d => { Q[keyOf(d)] = d; };''')
rep('''function loadQ(y, n) {
  const k = `${y}-${n}`;''','''function loadQ(q) {
  const k = keyOf(q);''')
rep('''picked.map(q => loadQ(q.y, q.n))''','''picked.map(q => loadQ(q))''')
rep('''const state = { view: "home",''','''const state = { level: store.get("bccMockLevel", "78") === "910" ? "910" : "78", check: store.get("bccMockCheck", true), view: "home",''')
rep('''const keyOf = q => `${q.y}-${q.n}`;''','''const keyOf = q => `${q.lv === "910" ? "h" : ""}${q.y}-${q.n}`;
function setLevel(lv) { state.level = lv; store.set("bccMockLevel", lv); INDEX = ALL.filter(q => lvOf(q) === lv); }
const LV = () => state.level === "910" ? " · Grade 9/10" : "";
const gradeName = lv => lv === "910" ? "Grade 9/10" : "Grade 7/8";''')
rep('''const AVG = {}; INDEX.forEach(q => { AVG[keyOf(q)] = q.avg; });
const YEAR_AVG = window.BCC_YEAR_AVG || {};
const avgFor = (items, mode) => mode === "year" && YEAR_AVG[items[0].y] ? YEAR_AVG[items[0].y] :''','''const AVG = {}; ALL.forEach(q => { AVG[keyOf(q)] = q.avg; });
const YEAR_AVG = window.BCC_YEAR_AVG || {};
const YEAR_AVGS = { "78": YEAR_AVG, "910": window.BCC_YEAR_AVG_910 || {} };
const avgFor = (items, mode) => mode === "year" && YEAR_AVGS[lvOf(items[0])][items[0].y] ? YEAR_AVGS[lvOf(items[0])][items[0].y] :''')
rep('''return [pickMixed(), "Mixed mock contest"];''','''return [pickMixed(), "Mixed mock contest" + LV()];''')
rep('''`${state.year} contest`];''','''`${state.year} contest` + LV()];''')
rep('''`Topic: ${TOPICS[state.topic]}`];''','''`Topic: ${TOPICS[state.topic]}` + LV()];''')
rep('''`Part ${state.part} practice`];''','''`Part ${state.part} practice` + LV()];''')
rep('''.sort(byPart), "Missed questions"];''','''.sort(byPart), "Missed questions" + LV()];''')
rep('''function missedList() {
  const log = getLog();
  return INDEX.filter(''','''function missedList(list = INDEX) {
  const log = getLog();
  return list.filter(''')
rep('''function weakPoints() {''','''function weakPoints(list = INDEX) {''')
rep('''  INDEX.forEach(q => {
    const a = log[keyOf(q)]; if (!a || !a.length) return;''','''  list.forEach(q => {
    const a = log[keyOf(q)]; if (!a || !a.length) return;''')
rep('''const mixedBest = bestOf("Mixed mock contest");''','''const mixedBest = bestOf("Mixed mock contest" + LV());''')
rep('''const b = bestOf(`${y} contest`); return''','''const b = bestOf(`${y} contest` + LV()); return''')
rep('''<span class="eyebrow">Beaver Computing Challenge · Grade 7/8</span>
      <h1>Mock Contest</h1>
      <p class="lede">Every real question from 2016 to 2025. Pick a card to start.</p>''','''<span class="eyebrow">Beaver Computing Challenge · ${gradeName(state.level)}</span>
      <h1>Mock Contest</h1>
      <p class="lede">Every real ${gradeName(state.level)} question from 2016 to 2025. Pick a card to start.</p>''')
rep('''    <div class="seg" role="radiogroup" aria-label="Timer">''','''    <div class="seg" role="radiogroup" aria-label="Grade level">
      <span class="seglabel">Level</span>
      <label><input type="radio" name="level" value="78" ${state.level === "78" ? "checked" : ""}><span>Grade 7/8 · your contest</span></label>
      <label><input type="radio" name="level" value="910" ${state.level === "910" ? "checked" : ""}><span>Grade 9/10 · stretch</span></label>
    </div>
    <div class="seg" role="radiogroup" aria-label="When to show answers">
      <span class="seglabel">Show if I'm right</span>
      <label><input type="radio" name="check" value="1" ${state.check ? "checked" : ""}><span>After each question</span></label>
      <label><input type="radio" name="check" value="0" ${state.check ? "" : "checked"}><span>Only at the end (real contest)</span></label>
    </div>
    <div class="seg" role="radiogroup" aria-label="Timer">''')
rep('''.seglabel { font-size: 14px; color: var(--muted); margin-right: 4px; }''','''.seglabel { font-size: 14px; color: var(--muted); margin-right: 4px; min-width: 118px; }''')
rep('''  if (e.target.name === "mode") state.mode = e.target.value;''','''  if (e.target.name === "mode") state.mode = e.target.value;
  else if (e.target.name === "level") { setLevel(e.target.value); renderHome(); }
  else if (e.target.name === "check") { state.check = e.target.value === "1"; store.set("bccMockCheck", state.check); }''')
rep('''    name: z.name, mode: z.mode, timeUp, rows,''','''    name: z.name, mode: z.mode, level: lvOf(z.items[0]), timeUp, rows,''')
rep('''hist.push({ at: r.at, name: r.name, score:''','''hist.push({ at: r.at, name: r.name, level: r.level, score:''')
rep('''contest: r.name, mode: r.mode, timeRanOut''','''contest: r.name, mode: r.mode, gradeLevel: gradeName(r.level), timeRanOut''')
rep('''from the ${x.q.y} contest`)}''','''from the ${x.q.y} ${gradeName(lvOf(x.q))} contest`)}''')
rep('''if (!INDEX.length) app.innerHTML''','''setLevel(state.level);
if (!INDEX.length) app.innerHTML''')
rep('''Averages are the official Grade 7/8 results published by CEMC for each real contest.''','''Averages are the official results published by CEMC for each real contest, for the same grade level you practised.''')
rep('''<span><i class="kavg"></i>Average Grade 7/8 student on the same questions</span>''','''<span><i class="kavg"></i>Average student on the same questions</span>''')
rep('''<span>The average Grade 7/8 student scored''','''<span>The average ${gradeName(r.level)} student scored''')

# ---------- instant check ----------
rep('''    name, mode: state.mode, strict: state.strict, items,''','''    name, mode: state.mode, strict: state.strict, check: state.check, checked: items.map(() => false), items,''')
rep('''    ${locked ? `<div class="lockednote">Time's up for this question. It's locked${z.picks[i] === null ? " as blank (2 points)" : ` with your answer (${LETTERS[z.picks[i]]})`}.</div>` : ""}''','''    ${locked && !z.checked[i] ? `<div class="lockednote">Time's up for this question. It's locked${z.picks[i] === null ? " as blank (2 points)" : ` with your answer (${LETTERS[z.picks[i]]})`}.</div>` : ""}''')
rep('''      <div class="row spread">
        <button class="btn ghost" data-nav="-1" ${i === 0 ? "disabled" : ""}>← Back</button>
        ${i < z.items.length - 1 ? `<button class="btn" data-nav="1">Next →</button>` : `<button class="btn" data-submit="1">Submit contest</button>`}
      </div>
    </div>''','''      ${reveal ? `<div class="feedback ${fk}" role="status">
          <b>${fk === "ok" ? `✓ Correct! +${POINTS[q.part]} points` : fk === "no" ? `✗ Not quite. You picked (${LETTERS[z.picks[i]]}), the answer is (${LETTERS[q.answer]}). 0 points` : `– Left blank. The answer is (${LETTERS[q.answer]}). +${BLANK_POINTS} points`}</b>
          <details ${fk === "ok" ? "" : "open"}><summary>Why (${LETTERS[q.answer]}) is right</summary><div class="paper">${q.answerHtml}${q.explanation || ""}</div></details>
        </div>` : ""}
      <div class="row spread">
        <button class="btn ghost" data-nav="-1" ${i === 0 ? "disabled" : ""}>← Back</button>
        <span class="row">
        ${z.check && !locked ? `<button class="btn" data-check="1" id="checkbtn">Check my answer</button>` : ""}
        ${i < z.items.length - 1 ? `<button class="btn ${z.check && !locked ? "ghost" : ""}" data-nav="1">${z.check && !locked ? "Skip →" : "Next →"}</button>` : `<button class="btn ${z.check && !locked ? "ghost" : ""}" data-submit="1">${z.check ? "Finish and see my score" : "Submit contest"}</button>`}
        </span>
      </div>
    </div>''')
rep('''  const std = z.items.length === 15''','''  const reveal = z.check && locked, fk = z.picks[i] === null ? "blank" : z.picks[i] === q.answer ? "ok" : "no";
  const std = z.items.length === 15''')
rep('''  if (!locked) optionList(app).forEach((li, k) => { li.dataset.pick = k; li.tabIndex = 0; });''','''  if (!locked) optionList(app).forEach((li, k) => { li.dataset.pick = k; li.tabIndex = 0; });
  if (reveal) optionList(app).forEach((li, k) => { if (k === q.answer) li.classList.add("right"); else if (k === z.picks[i]) li.classList.add("wrong"); });''')
rep('''  optionList(app).forEach((li, k) => li.classList.toggle("picked", p === k));''','''  optionList(app).forEach((li, k) => li.classList.toggle("picked", p === k && !(z.check && z.locked[z.idx])));
  const cb = document.getElementById("checkbtn"); if (cb) cb.textContent = p === null ? "Check (leave blank)" : `Check my answer (${LETTERS[p]})`;''')
rep('''    d.classList.toggle("answered", z.picks[k] !== null);''','''    d.classList.toggle("answered", z.picks[k] !== null && !(z.check && z.locked[k]));
    d.classList.toggle("dok", z.check && z.locked[k] && z.picks[k] === z.items[k].answer);
    d.classList.toggle("dno", z.check && z.locked[k] && z.picks[k] !== null && z.picks[k] !== z.items[k].answer);''')
rep('''    z.locked[z.idx] = true;
    const order''','''    z.locked[z.idx] = true;
    if (z.check) { renderQuiz(); return; }   // stay here and show whether you were right
    const order''')
rep('''.dot.current {''','''.dot.dok { background: var(--good-soft); border-color: var(--good); color: var(--good); }
.dot.dno { background: var(--bad-soft); border-color: var(--bad); color: var(--bad); }
.feedback { border-radius: 10px; padding: 12px 14px; display: flex; flex-direction: column; gap: 8px; background: var(--warn-soft); }
.feedback > b { color: var(--warn); font-size: 17px; }
.feedback.ok { background: var(--good-soft); } .feedback.ok > b { color: var(--good); }
.feedback.no { background: var(--bad-soft); } .feedback.no > b { color: var(--bad); }
.feedback summary { color: var(--ink); }
.feedback .paper { margin-top: 8px; }
.dot.current {''')
rep('''[data-pyear],[data-savefile],[data-tab]"''','''[data-pyear],[data-savefile],[data-tab],[data-check],[data-plan]"''')
rep('''  else if (d.nav) { z.idx += +d.nav;''','''  else if (d.check) { z.checked[z.idx] = true; z.locked[z.idx] = true; const top = window.scrollY; renderQuiz(); window.scrollTo(0, top); app.querySelector(".feedback")?.scrollIntoView({ block: "nearest", behavior: "smooth" }); }
  else if (d.nav) { z.idx += +d.nav;''')
rep('''    const blank = z.picks.filter(p => p === null).length;''','''    const blank = z.picks.filter((p, k) => p === null && !(z.check && z.locked[k])).length;''')

# ---------- plan tab ----------
rep('''const TABS = [["contest", "By contest"],''','''function planSteps() {
  const L78 = ALL.filter(q => lvOf(q) === "78"), L910 = ALL.filter(q => lvOf(q) === "910");
  const hist = store.get("bccMockHistory", []), w78 = weakPoints(L78), w910 = weakPoints(L910), missed78 = missedList(L78).length;
  const mixed78 = hist.filter(h => h.name === "Mixed mock contest");
  const ratio = k => { const x = w78.topic[k]; return x ? x.right / x.tried : -1; };
  const topicOK = Object.keys(TOPICS).filter(k => w78.topic[k] && w78.topic[k].tried >= 5 && ratio(k) >= 0.85);
  const tried = Object.keys(TOPICS).filter(k => !topicOK.includes(k) && w78.topic[k]).sort((a, b) => ratio(a) - ratio(b));
  const weakest = tried[0] || Object.keys(TOPICS).find(k => !topicOK.includes(k)) || "algo";
  const yearsDone = YEARS.filter(y => hist.some(h => h.name === `${y} contest` && h.score >= 85));
  const nextYear = [...YEARS].reverse().find(y => !yearsDone.includes(y)) || YEARS[0];
  const pOK = k => { const x = w910.part[k]; return x && x.tried >= 10 && x.right / x.tried >= 0.8; };
  const pTxt = k => { const x = w910.part[k]; return x ? `Part ${k}: ${pct(x.right, x.tried)}% of ${x.tried} tried` : `Part ${k}: not tried`; };
  const full910 = hist.filter(h => /^\\d{4} contest · Grade 9\\/10$/.test(h.name) && h.avg != null && h.score > h.avg);
  const next910 = [...YEARS].reverse().find(y => !hist.some(h => h.name === `${y} contest · Grade 9/10`)) || YEARS[0];
  const last2 = mixed78.slice(-2), rehearsal = last2.length === 2 && last2.every(h => h.score === (h.max || 90) && h.seconds <= 40 * 60);
  return [
    { t: "Take a baseline mock", w: "One Grade 7/8 mixed mock with answers shown only at the end and the timer locked. This shows where you really are, so don't worry about the score.", prog: mixed78.length ? `Done. First score ${pct(mixed78[0].score, mixed78[0].max || 90)}%` : "Not done yet", done: mixed78.length > 0, label: "Start the baseline mock", act: "mixed78" },
    { t: "Bring every topic to 85% or better", w: "Practise one topic at a time with \\"show if I'm right after each question\\" turned on, and read the explanation for every miss. A topic counts once you've tried at least 5 of its questions.", prog: `${topicOK.length} of 7 topics there` + (topicOK.length < 7 ? ` · next: ${TOPICS[weakest]}` : ""), done: topicOK.length === 7, label: `Practise ${TOPICS[weakest]}`, act: "topic78:" + weakest },
    { t: "Empty your missed list", w: "Every question you got wrong or left blank comes back until you get it right. This is the step that turns 80% into 100%.", prog: w78.tried < 30 ? `${missed78} waiting · counts once you've tried 30 questions (${w78.tried} so far)` : `${missed78} waiting`, done: w78.tried >= 30 && missed78 === 0, label: missed78 ? `Redo ${missed78} missed` : "Nothing to redo yet", act: missed78 ? "missed78" : "" },
    { t: "Score 85 or more out of 90 on every real Grade 7/8 paper", w: "Ten real papers, oldest first. Answers only at the end, timer locked, just like contest day.", prog: `${yearsDone.length} of 10 papers at 85+`, done: yearsDone.length === 10, label: `Do the ${nextYear} paper`, act: "year78:" + nextYear },
    { t: "Stretch: Grade 9/10 Parts A and B at 80%", w: "Harder questions make the Grade 7/8 ones feel easy. Start with Part A, then Part B. Counts once you've tried 10 questions in each.", prog: `${pTxt("A")} · ${pTxt("B")}`, done: pOK("A") && pOK("B"), label: `Grade 9/10 Part ${pOK("A") ? "B" : "A"}`, act: "part910:" + (pOK("A") ? "B" : "A") },
    { t: "Stretch: beat the Grade 9/10 average on three full papers", w: "Full Grade 9/10 papers, including Part C. You don't need 100% here. Beating the average of students two grades up is the goal.", prog: `${full910.length} of 3 papers above the Grade 9/10 average`, done: full910.length >= 3, label: `Do the ${next910} Grade 9/10 paper`, act: "year910:" + next910 },
    { t: "Dress rehearsal: two perfect mocks in a row", w: "Two Grade 7/8 mixed mocks back to back at 90 out of 90, each finished in 40 minutes or less so you have 5 minutes to re-check.", prog: mixed78.length < 2 ? "Needs your two most recent mixed mocks" : `Last two: ${last2.map(h => `${h.score}/${h.max || 90} in ${mmss(h.seconds)}`).join(" and ")}`, done: rehearsal, label: "Start a rehearsal mock", act: "mixed78" }
  ];
}
function planPanel() {
  const steps = planSteps(), next = steps.findIndex(x => !x.done), doneN = steps.filter(x => x.done).length;
  return `<div class="panel">
      <div class="row spread"><h3>${next < 0 ? "Plan complete. You're ready." : `Your next step: ${steps[next].t}`}</h3><span class="small muted">${doneN} of ${steps.length} steps done</span></div>
      <div class="meter ok"><i style="width:${pct(doneN, steps.length)}%"></i></div>
      <ol class="plan">${steps.map((x, i) => `<li class="${x.done ? "done" : i === next ? "now" : ""}">
        <span class="num">${x.done ? "✓" : i + 1}</span>
        <div class="pbody"><b>${x.t}</b><span class="small muted">${x.w}</span><span class="small"><b>${x.done ? "Done" : "Progress"}:</b> ${esc(x.prog)}</span>
        ${!x.done && x.act ? `<div><button class="btn ${i === next ? "" : "ghost"}" data-plan="${x.act}">${esc(x.label)}</button></div>` : ""}</div></li>`).join("")}</ol>
    </div>
    <div class="panel"><h3>Every practice day (30 to 40 minutes)</h3>
      <ol class="simple"><li><b>One timed set.</b> Do whatever "your next step" says above.</li><li><b>Fix every miss straight away.</b> Read the official explanation, then explain out loud why the right answer is right and why yours was wrong.</li><li><b>Next day, start with the missed list</b> before anything new.</li><li><b>Tell Claude "check my answers"</b> after a set. Claude reads your results file and explains the ones you still don't get.</li></ol></div>
    <div class="panel"><h3>Contest-day rules</h3>
      <ol class="simple"><li><b>Do Part A first and carefully.</b> Those 5 questions are worth 40 of the 90 points, and most lost points there are reading mistakes.</li><li><b>3 minutes a question.</b> If you're stuck at 3:00, mark it, move on, and come back with the time you saved.</li><li><b>Guess only when it pays.</b> A wrong answer is 0 and a blank is 2. A blind guess between four choices is worth 2 points on average in Part A, 1.5 in Part B and 1 in Part C, so a blind guess never beats a blank. Cross out two choices first and a guess is worth 4, 3 and 2: do it in Parts A and B.</li><li><b>Use the last 5 minutes</b> to re-read each question's last sentence and check you answered what it asked.</li></ol>
      <p class="small muted">No plan can promise 100%, but finishing all seven steps means you've seen and corrected every kind of question the contest has used in ten years.</p></div>`;
}
const TABS = [["plan", "My plan"], ["contest", "By contest"],''')
rep('''contest: "The exact paper from each year.",''','''plan: "Seven steps from where you are now to a perfect paper. Progress fills in by itself as you practise.", contest: "The exact paper from each year.",''')
rep('''      ${tab === "contest" ? `<div class="gallery years">${years}</div>` :''','''      ${tab === "plan" ? planPanel() : tab === "contest" ? `<div class="gallery years">${years}</div>` :''')
rep('''  if (d.start) start();
''','''  if (d.start) start();
  else if (d.plan) {
    const [a, v] = d.plan.split(":"), lv = a.endsWith("910") ? "910" : "78", m = a.replace(/78|910/, "");
    setLevel(lv); state.mode = m; if (m === "topic") state.topic = v; if (m === "part") state.part = v; if (m === "year") state.year = +v;
    start();
  }
''')
rep('''/* start screen */''','''/* plan */
ol.plan { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 4px; }
ol.plan > li { display: flex; gap: 14px; padding: 12px; border-radius: 12px; border: 1.5px solid transparent; }
ol.plan > li.now { border-color: var(--water); background: var(--water-soft); }
ol.plan .num { flex: none; width: 32px; height: 32px; border-radius: 50%; display: grid; place-items: center; font: 700 14px var(--mono); border: 2px solid var(--line); color: var(--muted); background: var(--surface); }
ol.plan li.now .num { border-color: var(--water); color: var(--water); }
ol.plan li.done .num { background: var(--good); border-color: var(--good); color: var(--surface); }
ol.plan li.done .pbody > b { color: var(--muted); }
.pbody { display: flex; flex-direction: column; gap: 4px; min-width: 0; }
ol.simple { margin: 0; padding-left: 22px; display: flex; flex-direction: column; gap: 8px; }

/* start screen */''',1)
rep('''tab: store.get("bccMockTab", "contest"),''','''tab: store.get("bccMockTab", "plan"),''')
rep('''TABS.some(t => t[0] === state.tab) ? state.tab : "contest";''','''TABS.some(t => t[0] === state.tab) ? state.tab : "plan";''')
open(p,'w').write(s)
