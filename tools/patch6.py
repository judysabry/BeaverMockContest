import sys,json,re
p=sys.argv[1]; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]); s=s.replace(a,b)
# data
ix='docs/q/index.js'; d=open(ix).read()
d=re.sub(r'window\.BCC_TOP=.*?;$','',d)
open(ix,'w').write(d+'window.BCC_TOP='+json.dumps(json.load(open('g910/honour.json')))+';')

rep('''const histAvg = h =>''','''/* Top students: the honour-roll cutoff CEMC published for each real contest (82 to 84 out of 90). */
const TOP = window.BCC_TOP || {};
const TOP_SHARE = 84 / 90, TYPICAL_SD = 17.3;
const topFor = (items, mode) => { const t = (TOP[lvOf(items[0])] || {})[items[0].y]; return mode === "year" && t ? t.cut : Math.round(maxOf(items) * TOP_SHARE); };
const histTop = h => h.top ?? Math.round((h.max || 90) * TOP_SHARE);
function normCdf(z) { const t = 1 / (1 + 0.2316419 * Math.abs(z)), d = 0.3989423 * Math.exp(-z * z / 2), q = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274)))); return z > 0 ? 1 - q : q; }
/* Rough estimate of the share of real contestants you would have beaten (bell-curve estimate from the official mean and spread). */
function standing(score, max, avg, items, mode) {
  if (avg == null) return null;
  const t = (TOP[lvOf(items[0])] || {})[items[0].y], sd = mode === "year" && t ? t.sd : TYPICAL_SD * max / 90;
  return Math.max(1, Math.min(99, Math.round(normCdf((score - avg) / sd) * 100)));
}
function tier(score, max, avg, top) {
  if (score >= max) return ["top", "★ Perfect score"];
  if (score >= top) return ["top", "★ Honour-roll level"];
  if (avg != null && score > avg) return ["up", "▲ Above average"];
  return ["down", "▼ Below average"];
}
const histAvg = h =>''')
rep('''score: rows.reduce((s, x) => s + x.pts, 0), max: maxOf(z.items), avg: avgFor(z.items, z.mode),''','''score: rows.reduce((s, x) => s + x.pts, 0), max: maxOf(z.items), avg: avgFor(z.items, z.mode), top: topFor(z.items, z.mode),''')
rep('''  state.result = r; state.quiz = null;''','''  r.beat = standing(r.score, r.max, r.avg, z.items, z.mode);
  state.result = r; state.quiz = null;''')
rep('''score: r.score, max: r.max, avg: r.avg, right:''','''score: r.score, max: r.max, avg: r.avg, top: r.top, beat: r.beat, right:''')
rep('''averageStudentScore: r.avg, beatAverage: r.score > r.avg,''','''averageStudentScore: r.avg, beatAverage: r.score > r.avg, honourRollLine: r.top, reachedHonourRollLine: r.score >= r.top, estimatedPercentBeaten: r.beat,''')
# results box
rep('''      <div class="row"><span class="small muted">A results file was saved''','''      <div class="avgline ${r.score >= r.top ? "top" : ""}">
        <b>${r.score >= r.max ? "★ Perfect score. That's the very top." : r.score >= r.top ? "★ Honour-roll level" : `Top students: ${r.top - r.score} more point${r.top - r.score === 1 ? "" : "s"} to reach the honour-roll line`}</b>
        <span>Top students usually score <b>${r.top}</b> / ${r.max} or more (${pct(r.top, r.max)}%). That's the honour-roll line${r.mode === "year" ? " for this real contest" : ", scaled from the usual 84 out of 90"}. ${r.score >= r.max ? "In the real contest only about 2 to 5 students in 100 get a perfect score." : `You'd have scored higher than roughly ${r.beat} in 100 students (an estimate).`}</span>
        <div class="ladder" aria-hidden="true"><i class="lavgm" style="left:${pct(r.avg, r.max)}%"></i><i class="ltopm" style="left:${pct(r.top, r.max)}%"></i><i class="lyoum" style="left:${pct(r.score, r.max)}%"></i></div>
        <div class="ladderkey small"><span><i class="lyoum"></i>You ${r.score}</span><span><i class="lavgm"></i>Average ${r.avg}</span><span><i class="ltopm"></i>Top ${r.top}</span></div>
      </div>
      <div class="row"><span class="small muted">A results file was saved''')
# chart
rep('''  const lastAvg = avg[n - 1];
  let ly = y(you[n - 1]), la = lastAvg == null ? null : y(lastAvg);
  if (la != null && Math.abs(ly - la) < 16) { const mid = (ly + la) / 2, up = ly <= la; ly = mid + (up ? -8 : 8); la = mid + (up ? 8 : -8); }
''','''  const top = list.map(h => pct(histTop(h), h.max || 90));
  const labels = [{ v: you[n - 1], text: `You ${you[n - 1]}%`, cls: "" }, { v: top[n - 1], text: `Top ${top[n - 1]}%`, cls: "sub" }];
  if (avg[n - 1] != null) labels.push({ v: avg[n - 1], text: `Average ${avg[n - 1]}%`, cls: "sub" });
  labels.sort((a, b) => b.v - a.v || (a.cls ? 1 : -1)); labels.forEach((l, i) => { l.y = y(l.v); if (i && l.y - labels[i - 1].y < 15) l.y = labels[i - 1].y + 15; });
''')
rep('''    <path class="lavg" d="${path(avg)}"/><path class="lyou" d="${path(you)}"/>''','''    <path class="ltop" d="${path(top)}"/><path class="lavg" d="${path(avg)}"/><path class="lyou" d="${path(you)}"/>
    ${top.map((p, i) => `<path class="mtop" d="M${x(i)},${y(p) - 5}L${x(i) + 5},${y(p) + 4}L${x(i) - 5},${y(p) + 4}Z"/>`).join("")}''')
rep('''    <text class="dlabel" x="${x(n - 1) + 12}" y="${ly + 4}">You ${you[n - 1]}%</text>
    ${la == null ? "" : `<text class="dlabel sub" x="${x(n - 1) + 12}" y="${la + 4}">Average ${lastAvg}%</text>`}''','''    ${labels.map(l => `<text class="dlabel ${l.cls}" x="${x(n - 1) + 12}" y="${l.y + 4}">${l.text}</text>`).join("")}''')
rep('''"below average ▼" : "same as average"}`}`)}"''','''"below average ▼" : "same as average"}`} · Top ${top[i]}%${you[i] >= top[i] ? " · honour-roll level ★" : ""}`)}"''')
rep('''<span><i class="kavg"></i>Average student on the same questions</span></div>''','''<span><i class="kavg"></i>Average student on the same questions</span><span><i class="ktop"></i>Top students (honour-roll line)</span></div>''')
rep('''<span>Latest: ${versus(last.score, histAvg(last))}</span></div>''','''<span>Latest: <span class="vs ${tier(last.score, last.max || 90, histAvg(last), histTop(last))[0]}">${tier(last.score, last.max || 90, histAvg(last), histTop(last))[1]}</span></span></div>
    <p>You reached the honour-roll line in <b>${hist.filter(h => h.score >= histTop(h)).length} of ${hist.length}</b> and scored a perfect paper in <b>${hist.filter(h => h.score >= (h.max || 90)).length}</b>.</p>''')
rep('''<th>Did you pass it?</th>''','''<th>Did you pass it?</th><th>Top line</th><th>Where you are</th>''')
i=s.index('${hist.map((h, i) => [h, i]).reverse().slice(0, 30)'); j=s.index('<td>${h.right}</td>',i)
a='<td>${versus(h.score, histAvg(h))}</td>'
assert s[i:j].count(a)==1
s=s[:i]+s[i:j].replace(a,a+'<td>${histTop(h)}/${h.max || 90}</td><td><span class="vs ${tier(h.score, h.max || 90, histAvg(h), histTop(h))[0]}">${tier(h.score, h.max || 90, histAvg(h), histTop(h))[1]}</span>${h.score < histTop(h) ? `<br><span class="small muted">${histTop(h) - h.score} to the top line</span>` : ""}</td>')+s[j:]
rep('''For mixed, topic and part practice, the average is added up from the official average of each question you were given.</p>''','''For mixed, topic and part practice, the average is added up from the official average of each question you were given. The top line is CEMC's honour-roll cutoff: 82 to 84 out of 90 depending on the year for real papers, and the same share (93%) of the points for other practice sets. In real contests about 5 to 15 students in 100 reach it, and about 2 to 5 in 100 get a perfect 90.</p>''')
rep(''':root { --s-you: #1d6f86; --s-avg: #8a6d3b; }
@media (prefers-color-scheme: dark) { :root { --s-you: #6cc3d9; --s-avg: #d0a968; } }''',''':root { --s-you: #1d6f86; --s-avg: #8a6d3b; --s-top: #7a3fa0; --top-soft: #efe4f7; }
@media (prefers-color-scheme: dark) { :root { --s-you: #6cc3d9; --s-avg: #d0a968; --s-top: #c79be8; --top-soft: #33234a; } }
.chart .ltop { fill: none; stroke: var(--s-top); stroke-width: 2; stroke-dasharray: 2 4; stroke-linecap: round; }
.chart .mtop { fill: var(--s-top); stroke: var(--surface); stroke-width: 2; }
.legend i.ktop { border-top: 3px dotted var(--s-top); }
.vs.top { color: var(--s-top); }
.avgline.top { background: var(--top-soft); } .avgline.top > b { color: var(--s-top); }
.ladder { position: relative; height: 10px; border-radius: 5px; background: var(--surface); margin: 14px 6px 4px; }
.ladder i { position: absolute; top: -4px; width: 4px; height: 18px; margin-left: -2px; border-radius: 2px; }
.ladder i.lyoum { width: 14px; height: 14px; top: -2px; margin-left: -7px; border-radius: 50%; border: 2px solid var(--surface); }
i.lyoum { background: var(--s-you); } i.lavgm { background: var(--s-avg); } i.ltopm { background: var(--s-top); }
.ladderkey { display: flex; flex-wrap: wrap; gap: 4px 16px; color: var(--muted); }
.ladderkey i { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; }''')
open(p,'w').write(s)
