import json,re,unicodedata
norm=lambda x: re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',x).lower())
t=open('pdfs/all.txt').read()
qs=json.load(open('g910/all.json'))
YEAR={}
OUT='docs/q'
pts={'A':8,'B':6,'C':4}
for y in range(2016,2026):
    doc=t[t.index('=== pdfs/%d.pdf page 1'%y):]
    nxt=doc.find('=== pdfs/%d.pdf page 1'%(y+1)); doc=doc[:nxt] if nxt>0 else doc
    if y<2025:
        a=doc.index('Overall Statistics for Grade 9/10'); b=doc.find('Honour Roll',a); doc=doc[a:b]
        YEAR[y]=float(re.search(r'Overall average score: ([\d.]+)',doc).group(1))
    else:
        a=doc.index('Number of competitors 7827'); doc=doc[a:doc.index('Summary and Statistics',a)]
        YEAR[y]=float(re.search(r'Overall average score ([\d.]+)',doc).group(1))
    doc=re.sub(r'(\d\.\d\d/[468]) ',r'\1\n',doc)
    pairs=re.findall(r'([A-Z][^:\n/]{1,60}?):?\s+(\d\.\d\d)\s*/\s*([468])\b',doc)
    miss=[];tot=0
    for q in [q for q in qs if q['y']==y]:
        c=[float(v) for n,v,m in pairs if (norm(n)==norm(q['title']) or {'Propagate':'Propogate','Unlock the Crown':'Chest Puzzle'}.get(q['title'])==n.strip()) and int(m)==pts[q['part']]]
        if not c: miss.append(q['title']); continue
        q['avg']=c[0]; tot+=c[0]
    print(y,'sum %.2f'%tot,'official',YEAR[y],'missing',miss, [n for n,v,m in pairs if not any(norm(n)==norm(q['title']) for q in qs if q['y']==y)])
json.dump(qs,open('g910/all.json','w')); json.dump(YEAR,open('g910/year.json','w'))

idxsrc=open(OUT+'/index.js').read()
i78=json.loads(idxsrc.split(';window.BCC_YEAR_AVG')[0][len('window.BCC_INDEX='):])
i78=[q for q in i78 if q.get('lv')!='910']
y78=json.loads(re.search(r'window\.BCC_YEAR_AVG=(\{.*?\});',idxsrc).group(1))
tot=0
for q in qs:
    assert q['answer'] in (0,1,2,3) and 'avg' in q and q['topic'], q['title']
    o={k:q[k] for k in ('lv','y','n','part','topic','title','answer','story','question','answerHtml','explanation','connections')}
    sj='BCC_Q('+json.dumps(o,ensure_ascii=False).replace('</','<\\/')+');'
    open('%s/h%d-%d.js'%(OUT,q['y'],q['n']),'w').write(sj); tot+=len(sj)
    i78.append({k:q[k] for k in ('lv','y','n','part','topic','title','avg')})
open(OUT+'/index.js','w').write('window.BCC_INDEX='+json.dumps(i78)+';window.BCC_YEAR_AVG='+json.dumps(y78)+';window.BCC_YEAR_AVG_910='+json.dumps(YEAR)+';')
print('wrote',len(qs),'files',tot//1000000,'MB; index entries',len(i78))
