import json,glob,re,sys,os
src,out=sys.argv[1],sys.argv[2]
index=[];missing=0;sizes=[]
for f in sorted(glob.glob(src+'/data/*.json')):
    d=json.load(open(f)); y=d['year']; imgs=d['images']
    def inl(h):
        global missing
        def r(m):
            global missing
            v=imgs.get(m.group(1))
            if not v: missing+=1; return 'src=""'
            return 'src="%s"'%v
        return re.sub(r'src="img:([^"]+)"',r,h or '')
    for q in d['questions']:
        o={'y':y,'n':int(q['n']),'part':q['part'],'topic':q['topic'],'title':q['title'],'answer':q['answer']}
        for k in ('story','question','answerHtml','explanation','connections'): o[k]=inl(q.get(k))
        o['mc']=len(re.findall(r'<ol class="mc"',q.get('question') or ''))+len(re.findall(r'<ol class="mc"',q.get('story') or ''))
        s='BCC_Q('+json.dumps(o,ensure_ascii=False).replace('</','<\\/')+');'
        open('%s/q/%d-%d.js'%(out,y,o['n']),'w').write(s); sizes.append(len(s))
        index.append({k:o[k] for k in ('y','n','part','topic','title')})
        if o['mc']!=1: print('mc count',y,o['n'],o['mc'])
        assert o['answer'] in (0,1,2,3)
open(out+'/q/index.js','w').write('window.BCC_INDEX='+json.dumps(index)+';')
print(len(index),'questions; missing imgs',missing,'; max',max(sizes),'total',sum(sizes))
print(list(json.load(open(src+'/data/2016.json'))['images'].values())[0][:60])
