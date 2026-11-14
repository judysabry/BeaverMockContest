import sys
p=sys.argv[1]; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]); s=s.replace(a,b)
a=s.index('    <section class="shelf"><div class="shelfhead"><h2>By contest</h2>'); b=s.index('    <p class="credit">Questions and solutions © Centre', a)
s=s[:a]+r'''    <section class="shelf">
      <div class="tabs" role="tablist">${TABS.map(([k, label]) => `<button role="tab" class="tab" data-tab="${k}" aria-selected="${tab === k}">${label}</button>`).join("")}</div>
      <p class="small muted">${{ contest: "The exact paper from each year.", topic: "Up to 15 questions on one skill. Your weakest topic is marked.", part: "15 questions at one difficulty.", scores: "Every contest you've finished, newest first." }[tab]}</p>
      ${tab === "contest" ? `<div class="gallery years">${years}</div>` : tab === "topic" ? `<div class="gallery topics">${topics}</div>` : tab === "part" ? `<div class="gallery parts3">${parts}</div>` : hist.length ? `<div class="panel">
        <div class="tablewrap"><table class="hist"><tr><th>Date</th><th>Contest</th><th>Score</th><th>Right</th><th>Wrong</th><th>Blank</th><th>Time</th></tr>
        ${hist.slice().reverse().slice(0, 30).map(h => `<tr><td>${new Date(h.at).toLocaleDateString()}</td><td>${esc(h.name)}</td><td><b>${h.score}</b>/${h.max || 90} · ${pct(h.score, h.max || 90)}%</td><td>${h.right}</td><td>${h.wrong}</td><td>${h.blank}</td><td>${mmss(h.seconds)}</td></tr>`).join("")}
        </table></div><div><button class="clear" data-clearhist="1">Clear my scores and history</button></div></div>` : `<div class="panel"><p class="muted">No scores yet. Finish a contest and it will show up here.</p></div>`}
    </section>
'''+s[b:]
rep('''function renderHome() {
''','''const TABS = [["contest", "By contest"], ["topic", "By topic"], ["part", "By part"], ["scores", "My scores"]];
function renderHome() {
  const tab = TABS.some(t => t[0] === state.tab) ? state.tab : "contest";
''')
rep('''state = { view: "home",''','''state = { view: "home", tab: store.get("bccMockTab", "contest"),''')
rep('''[data-pmixed],[data-pyear],[data-savefile]"''','''[data-pmixed],[data-pyear],[data-savefile],[data-tab]"''')
rep('''  if (d.start) start();
''','''  if (d.start) start();
  else if (d.tab) { state.tab = d.tab; store.set("bccMockTab", d.tab); renderHome(); app.querySelector(`[data-tab="${d.tab}"]`)?.focus(); }
''')
rep('''.shelfhead {''','''.tabs { display: flex; gap: 4px; border-bottom: 2px solid var(--line); overflow-x: auto; }
.tab { background: none; border: 0; border-bottom: 3px solid transparent; margin-bottom: -2px; padding: 10px 16px; font-weight: 700; font-size: 16px; color: var(--muted); white-space: nowrap; border-radius: 8px 8px 0 0; }
.tab:hover { color: var(--ink); background: var(--water-soft); }
.tab[aria-selected="true"] { color: var(--water); border-bottom-color: var(--water); }
.shelfhead {''')
open(p,'w').write(s)
