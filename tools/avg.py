import re,json,sys,unicodedata
t=open('pdfs/all.txt').read()
idx=json.loads(open('docs/q/index.js').read()[len('window.BCC_INDEX='):-1])
norm=lambda x: re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',x).lower())
YEAR={2016:51.12,2017:48.66,2018:54.88,2019:58.36,2020:64.18,2021:57.47,2022:65.51,2023:64.55,2024:56.94,2025:68.93}
out={}
ALIAS={'Propagate':'Propogate','Unlock the Crown':'Chest Puzzle'}
for y in range(2016,2026):
    doc=t[t.index('=== pdfs/%d.pdf page 1'%y):]
    nxt=doc.find('=== pdfs/%d.pdf page 1'%(y+1)); doc=doc[:nxt] if nxt>0 else doc
    if y<2025:
        a=doc.index('Overall Statistics for Grade 7/8'); b=min(x for x in (doc.find('Overall Statistics for Grade 9/10',a),doc.find('Honour Roll',a)) if x>0); doc=doc[a:b]
    else:
        a=doc.index('Number of competitors 16344'); doc=doc[a:doc.index('Summary and Statistics',a)]
    doc=re.sub(r'(\d\.\d\d/[468]) ',r'\1\n',doc)
    pairs=re.findall(r'([A-Z][^:\n/]{1,60}?):?\s+(\d\.\d\d)\s*/\s*([468])\b',doc)
    qs=[q for q in idx if q['y']==y]; pts={'A':8,'B':6,'C':4}
    tot=0;miss=[]
    for q in qs:
        c=[(float(v),int(m)) for (n,v,m) in pairs if (norm(n)==norm(q['title']) or ALIAS.get(q['title'])==n.strip()) and int(m)==pts[q['part']]]
        c=list(dict.fromkeys(c))
        if not c: miss.append(q['title']); continue
        if len(c)>1: print(y,q['title'],'multi',c)
        q['avg']=c[-1 if False else 0][0]; tot+=q['avg']
    if miss: print('   names:',[n for n,v,m in pairs])
    print(y,'matched',len(qs)-len(miss),'sum %.2f'%tot,'official',YEAR[y],'missing',miss)
if '--write' in sys.argv:
    open('docs/q/index.js','w').write('window.BCC_INDEX='+json.dumps(idx)+';window.BCC_YEAR_AVG='+json.dumps(YEAR)+';')
