import sys
p=sys.argv[1]; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:70]); s=s.replace(a,b)

rep('''const byPart = (a, b)''','''/* Official Grade 7/8 averages from CEMC's results booklets: per question, and per whole contest. */
const AVG = {}; INDEX.forEach(q => { AVG[keyOf(q)] = q.avg; });
const YEAR_AVG = window.BCC_YEAR_AVG || {};
const avgFor = (items, mode) => mode === "year" && YEAR_AVG[items[0].y] ? YEAR_AVG[items[0].y] : Math.round(items.reduce((t, q) => t + (AVG[keyOf(q)] || 0), 0) * 10) / 10;
const histAvg = h => h.avg ?? (/^(\\d{4}) contest$/.test(h.name) ? YEAR_AVG[h.name.slice(0, 4)] ?? null : null);
function versus(score, avg) {   // text + icon, so it never relies on colour alone
  if (avg == null) return `<span class="muted">–</span>`;
  const d = Math.round((score - avg) * 10) / 10;
  return d > 0 ? `<span class="vs up">▲ Above by ${d}</span>` : d < 0 ? `<span class="vs down">▼ Below by ${-d}</span>` : `<span class="vs">Same as average</span>`;
}
const byPart = (a, b)''')

# finish
rep('''score: rows.reduce((s, x) => s + x.pts, 0), max: maxOf(z.items),''','''score: rows.reduce((s, x) => s + x.pts, 0), max: maxOf(z.items), avg: avgFor(z.items, z.mode),''')
rep('''score: r.score, max: r.max, right: r.right, wrong: r.wrong, blank: r.blank, seconds: r.seconds });''','''score: r.score, max: r.max, avg: r.avg, right: r.right, wrong: r.wrong, blank: r.blank, seconds: r.seconds });''')
rep('''score: r.score, max: r.max, percent: pct(r.score, r.max),''','''score: r.score, max: r.max, percent: pct(r.score, r.max), averageStudentScore: r.avg, beatAverage: r.score > r.avg,''')
rep('''points: x.pts, seconds: x.spent }))''','''points: x.pts, averageStudentPoints: AVG[keyOf(x.q)], seconds: x.spent }))''')

# results verdict
rep('''      <div class="row"><span class="small muted">A results file was saved''','''      <div class="avgline ${r.score > r.avg ? "up" : r.score < r.avg ? "down" : ""}">
        <b>${r.score > r.avg ? "▲ You beat the average" : r.score < r.avg ? "▼ Below the average this time" : "Same as the average"}</b>
        <span>The average Grade 7/8 student scored <b>${r.avg}</b> / ${r.max} (${pct(r.avg, r.max)}%) on these questions in the real contest. You scored ${r.score}, ${r.score >= r.avg ? Math.round((r.score - r.avg) * 10) / 10 + " above" : Math.round((r.avg - r.score) * 10) / 10 + " below"}.</span>
      </div>
      <div class="row"><span class="small muted">A results file was saved''')

# scores tab
a=s.index(''' : hist.length ? `<div class="panel">'''); b=s.index('''`<div class="panel"><p class="muted">No scores yet.''')
s=s[:a]+''' : hist.length ? scoresPanel(hist) : '''+s[b:]

rep('''const TABS = [[''',r'''function scoreChart(list) {
  const W = 720, H = 270, L = 40, R = 96, T = 16, B = 30, n = list.length;
  const x = i => n === 1 ? L + (W - L - R) / 2 : L + i * (W - L - R) / (n - 1);
  const y = p => T + (100 - p) * (H - T - B) / 100;
  const you = list.map(h => pct(h.score, h.max || 90)), avg = list.map(h => histAvg(h) == null ? null : Math.round(histAvg(h) / (h.max || 90) * 100));
  const path = v => v.map((p, i) => p == null ? "" : `${i && v[i - 1] != null ? "L" : "M"}${x(i).toFixed(1)},${y(p).toFixed(1)}`).join("");
  const lastAvg = avg[n - 1];
  let ly = y(you[n - 1]), la = lastAvg == null ? null : y(lastAvg);
  if (la != null && Math.abs(ly - la) < 16) { const mid = (ly + la) / 2, up = ly <= la; ly = mid + (up ? -8 : 8); la = mid + (up ? 8 : -8); }
  const step = Math.max(1, Math.ceil(n / 10));
  return `<svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="Line chart of your score in each contest compared with the average student's score. The same numbers are in the table below.">
    ${[0, 25, 50, 75, 100].map(g => `<line class="grid" x1="${L}" x2="${W - R}" y1="${y(g)}" y2="${y(g)}"/><text class="axis" x="${L - 8}" y="${y(g) + 4}" text-anchor="end">${g}%</text>`).join("")}
    ${list.map((h, i) => i % step === 0 || i === n - 1 ? `<text class="axis" x="${x(i)}" y="${H - 8}" text-anchor="middle">${i + 1}</text>` : "").join("")}
    <path class="lavg" d="${path(avg)}"/><path class="lyou" d="${path(you)}"/>
    ${avg.map((p, i) => p == null ? "" : `<rect class="mavg" x="${x(i) - 4}" y="${y(p) - 4}" width="8" height="8" transform="rotate(45 ${x(i)} ${y(p)})"/>`).join("")}
    ${you.map((p, i) => `<circle class="myou" cx="${x(i)}" cy="${y(p)}" r="5"/>`).join("")}
    <text class="dlabel" x="${x(n - 1) + 12}" y="${ly + 4}">You ${you[n - 1]}%</text>
    ${la == null ? "" : `<text class="dlabel sub" x="${x(n - 1) + 12}" y="${la + 4}">Average ${lastAvg}%</text>`}
    ${list.map((h, i) => { const w = n === 1 ? W - L - R : (W - L - R) / (n - 1); return `<rect class="hit" tabindex="0" data-tip="${esc(`Contest ${i + 1} · ${h.name} · You ${you[i]}%${avg[i] == null ? "" : ` · Average ${avg[i]}% · ${you[i] > avg[i] ? "above average ▲" : you[i] < avg[i] ? "below average ▼" : "same as average"}`}`)}" data-x="${x(i)}" x="${x(i) - w / 2}" y="${T}" width="${w}" height="${H - T - B}"/>`; }).join("")}
    <line class="cross" id="cross" x1="0" x2="0" y1="${T}" y2="${H - B}" visibility="hidden"/>
  </svg>`;
}
function scoresPanel(hist) {
  const list = hist.slice(-20), judged = hist.filter(h => histAvg(h) != null), beat = judged.filter(h => h.score > histAvg(h)).length;
  const last = hist[hist.length - 1];
  return `<div class="panel">
    <div class="row spread"><h3>${judged.length ? `You beat the average in ${beat} of ${judged.length} contest${judged.length === 1 ? "" : "s"}` : "Your scores"}</h3><span>Latest: ${versus(last.score, histAvg(last))}</span></div>
    <div class="legend"><span><i class="kyou"></i>You</span><span><i class="kavg"></i>Average Grade 7/8 student on the same questions</span></div>
    ${scoreChart(list)}
    <p class="small muted" id="tip">Point at or tap the chart to see one contest. Numbers along the bottom are your contests in order${hist.length > 20 ? " (latest 20)" : ""}.</p>
    <div class="tablewrap"><table class="hist"><tr><th>#</th><th>Date</th><th>Contest</th><th>You</th><th>Average</th><th>Did you pass it?</th><th>Right</th><th>Wrong</th><th>Blank</th><th>Time</th></tr>
    ${hist.map((h, i) => [h, i]).reverse().slice(0, 30).map(([h, i]) => `<tr><td>${i + 1}</td><td>${new Date(h.at).toLocaleDateString()}</td><td>${esc(h.name)}</td><td><b>${h.score}</b>/${h.max || 90} · ${pct(h.score, h.max || 90)}%</td><td>${histAvg(h) == null ? "–" : `${histAvg(h)} · ${pct(histAvg(h), h.max || 90)}%`}</td><td>${versus(h.score, histAvg(h))}</td><td>${h.right}</td><td>${h.wrong}</td><td>${h.blank}</td><td>${mmss(h.seconds)}</td></tr>`).join("")}
    </table></div>
    <p class="small muted">Averages are the official Grade 7/8 results published by CEMC for each real contest. For mixed, topic and part practice, the average is added up from the official average of each question you were given.</p>
    <div><button class="clear" data-clearhist="1">Clear my scores and history</button></div></div>`;
}
const TABS = [[''')

rep('''/* start screen */''','''/* score chart */
:root { --s-you: #1d6f86; --s-avg: #8a6d3b; }
@media (prefers-color-scheme: dark) { :root { --s-you: #6cc3d9; --s-avg: #d0a968; } }
.chart { width: 100%; height: auto; display: block; }
.chart .grid { stroke: var(--line); stroke-width: 1; }
.chart .axis { fill: var(--muted); font: 11px var(--mono); }
.chart .lyou { fill: none; stroke: var(--s-you); stroke-width: 2; stroke-linejoin: round; stroke-linecap: round; }
.chart .lavg { fill: none; stroke: var(--s-avg); stroke-width: 2; stroke-dasharray: 6 5; }
.chart .myou { fill: var(--s-you); stroke: var(--surface); stroke-width: 2; }
.chart .mavg { fill: var(--s-avg); stroke: var(--surface); stroke-width: 2; }
.chart .dlabel { fill: var(--ink); font: 700 13px var(--body); }
.chart .dlabel.sub { fill: var(--muted); font-weight: 400; }
.chart .hit { fill: transparent; cursor: crosshair; outline: none; }
.chart .cross { stroke: var(--muted); stroke-width: 1; pointer-events: none; }
.legend { display: flex; flex-wrap: wrap; gap: 6px 18px; font-size: 14px; color: var(--muted); }
.legend span { display: inline-flex; align-items: center; gap: 8px; }
.legend i { display: inline-block; width: 26px; height: 0; border-top: 3px solid var(--s-you); }
.legend i.kavg { border-top: 3px dashed var(--s-avg); }
.vs { font-weight: 700; white-space: nowrap; } .vs.up { color: var(--good); } .vs.down { color: var(--bad); }
.avgline { border-radius: 10px; padding: 12px 14px; display: flex; flex-direction: column; gap: 2px; background: var(--water-soft); }
.avgline.up { background: var(--good-soft); } .avgline.up > b { color: var(--good); }
.avgline.down { background: var(--bad-soft); } .avgline.down > b { color: var(--bad); }
.avgline span { font-size: 14px; }

/* start screen */''')

rep('''app.addEventListener("keydown", e => {''','''function showTip(e) {
  const el = e.target.closest && e.target.closest(".hit"), tip = document.getElementById("tip"), cross = document.getElementById("cross");
  if (!el || !tip) return;
  tip.textContent = el.dataset.tip;
  cross.setAttribute("x1", el.dataset.x); cross.setAttribute("x2", el.dataset.x); cross.setAttribute("visibility", "visible");
}
app.addEventListener("pointerover", showTip); app.addEventListener("focusin", showTip); app.addEventListener("click", showTip);
app.addEventListener("keydown", e => {''')
open(p,'w').write(s)
