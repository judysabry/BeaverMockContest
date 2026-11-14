import re,json,glob,sys,os,base64,subprocess,tempfile,html,unicodedata
from html.parser import HTMLParser
VOID={'img','br','hr','input','meta','link','col','wbr','source','area','base','embed','param','track'}
class Bal(HTMLParser):
    def __init__(s): super().__init__(convert_charrefs=False); s.stack=[]; s.extra=0
    def handle_starttag(s,t,a):
        if t not in VOID: s.stack.append(t)
    def handle_endtag(s,t):
        if t in VOID: return
        if t in s.stack:
            while s.stack and s.stack.pop()!=t: pass
        else: s.extra+=1
def fix(h):
    h=h.strip()
    for _ in range(6):
        b=Bal(); b.feed(re.sub(r'="data:[^"]*"','=""',h)); b.close()
        if b.extra==0 and not b.stack: return h
        if b.extra:
            # drop last stray closing tag
            m=list(re.finditer(r'</(div|p|li|ul|ol|td|tr|table|center|span)>\s*$',h))
            if m: h=h[:m[-1].start()].rstrip(); continue
        if b.stack:
            m=re.search(r'<(div|p)[^>]*>\s*$',h)
            if m: h=h[:m.start()].rstrip(); continue
            h+=''.join('</%s>'%t for t in reversed(b.stack)); continue
        break
    b=Bal(); b.feed(re.sub(r'="data:[^"]*"','=""',h)); b.close()
    if b.extra or b.stack: print('  UNBALANCED',b.extra,b.stack,h[-80:].replace('\n',' '))
    return h
def shrink(h):
    def r(m):
        d=m.group(1)
        if len(d)<700000: return m.group(0)
        with tempfile.TemporaryDirectory() as td:
            p=td+'/a.png'; open(p,'wb').write(base64.b64decode(d))
            subprocess.run(['sips','-Z','1500',p,'--out',td+'/b.png'],capture_output=True)
            if os.path.exists(td+'/b.png'):
                nd=base64.b64encode(open(td+'/b.png','rb').read()).decode()
                if len(nd)<len(d): return 'src="data:image/png;base64,%s"'%nd
        return m.group(0)
    return re.sub(r'src="data:image/png;base64,([^"]+)"',r,h)
txt=lambda h: html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',re.sub(r'="data:[^"]*"','',h)))).strip()
allq=[]
for f in sorted(glob.glob('g910/*-s.html')):
    y=int(os.path.basename(f)[:4])
    s=open(f,encoding='utf-8',errors='replace').read()
    s=re.sub(r'<style.*?</style>','',s,flags=re.S); s=re.sub(r'<script.*?</script>','',s,flags=re.S)
    s=s[s.index('<h2'):]; s=re.sub(r'</body>.*','',s,flags=re.S)
    parts=re.split(r'<h2[^>]*>\s*Part\s+([ABC])\s*</h2>',s)
    n=0
    for i in range(1,len(parts),2):
        part=parts[i]; qs=re.split(r'<h3[^>]*>(.*?)</h3>',parts[i+1],flags=re.S)
        for j in range(1,len(qs),2):
            n+=1; title=txt(qs[j]); secs=re.split(r'<h4[^>]*>(.*?)</h4>',qs[j+1],flags=re.S)
            d={}
            for k in range(1,len(secs),2):
                name=txt(secs[k]).lower(); key='story' if name.startswith('story') else 'question' if name.startswith('question') else 'answerHtml' if name=='answer' else 'explanation' if name.startswith('explanation') else 'connections' if name.startswith('connection') else 'country' if name.startswith('country') else name
                d[key]=secs[k+1]
            q={'lv':'910','y':y,'n':n,'part':part,'title':title}
            for key in ('story','question','answerHtml','explanation','connections'):
                q[key]=shrink(fix(d.get(key,''))) if d.get(key) else ''
            m=re.search(r'\(?([A-D])\)',txt(q['answerHtml'])[:40])
            q['answer']='ABCD'.index(m.group(1)) if m else None
            if q['answer'] is None: print('  NO ANSWER',y,n,title,txt(q['answerHtml'])[:80])
            extra=set(d)-{'story','question','answerHtml','explanation','connections','country'}
            if extra or not q['question'] or not q['story']: print('  CHECK',y,n,title,'extra',extra,'story',bool(q['story']),'q',bool(q['question']))
            q['_t']=txt(q['story'])[:160]+' || '+txt(q['question'])[:120]+' || '+txt(q['connections'])[:160]
            allq.append(q)
    print(y,'questions',n,'parts',[sum(1 for q in allq if q['y']==y and q['part']==p) for p in 'ABC'],'size KB',sum(len(json.dumps(q)) for q in allq if q['y']==y)//1000)
json.dump(allq,open('g910/all.json','w'))
