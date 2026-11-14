import json,re,sys
qs=json.load(open('g910/all.json'))
RULES=[('code',r'binary|encod|cipher|crypt|compress|bit\b|bits\b|decod|hash|checksum|parity|pixel|secret message|code\b'),
('graph',r'graph|shortest path|network|vert(ex|ices)|edges|tree\b|spanning|route|map\b|flow'),
('ds',r'stack|queue|data structure|sort|linked list|array|database|priority|LIFO|FIFO|data\b'),
('opt',r'optimi|greedy|game theory|winning strategy|dynamic programming|schedul|maximum|minimum|best possible|knapsack'),
('logic',r'logic|boolean|constraint|deduc|true or false|condition|gate|AND\b|truth'),
('pat',r'pattern|sequence|recurs|fractal|repeat|symmetr|regular expression'),
('algo',r'algorithm|program|instruction|simulat|state|automat|loop|robot|step')]
OV=json.load(open('g910/topic_override.json')) if len(sys.argv)>1 else {}
from collections import Counter
for q in qs:
    k='%d-%d'%(q['y'],q['n'])
    if q.get('topic') and not q.get('_guess'): continue
    conn=q['_t'].split(' || ')[2]; body=q['_t']
    t=next((t for t,r in RULES if re.search(r,conn,re.I)),None) or next((t for t,r in RULES if re.search(r,body,re.I)),'algo')
    q['topic']=OV.get(k,t); q['_guess']=1
    if len(sys.argv)<2: print('%s|%s|%s|%s|%s'%(k,q['title'][:24],t,q['_t'].split(' || ')[1][:50],conn[:75]))
print(Counter(q['topic'] for q in qs))
json.dump(qs,open('g910/all.json','w'))
