import random

from .DSLrules import graph,rules
from .tree import DSLNode

MAX_LEVELS = 7
MAX_TOKENS = 45
tokensCount = 0

def generate(node,level):
    global MAX_LEVELS,MAX_TOKENS,tokensCount
    if level>MAX_LEVELS or tokensCount>=MAX_TOKENS or (node.key in graph.keys() and level+2>MAX_LEVELS):
        return False
    cur=graph.get(node.key)
    if cur==None:
        return True
    rule=rules.get(node.key)
    if 'inOrder' in rule.keys():
        for elm in cur:
            if elm=='container' or random.randrange(0,3):
                childNode=DSLNode(elm,node)
                res=generate(childNode,level+1)
                if res:
                    node.add(childNode)
                    tokensCount+=1
        return True
    elif 'combinations' in rule.keys():
       divs= random.choice(rule["0" if random.random()<rule['proba'] else "1"])
       for n in divs:
            childNode=DSLNode('div-'+str(n),node)
            res=generate(childNode,level+1)
            if res:
                node.add(childNode)
                tokensCount+=1
       return True
    
    elif node.key=='flex' and node.parent.key=='header':
        nodes=[]
        if random.random()>0.3:
            nodes.append('nav')
            if random.random()>0.8:
                nodes.append('nav')
        if random.random()<0.9 or len(nodes)==0: 
            if random.random()>0.8:
                nodes.append('logodiv')
            else:
                nodes.insert(0,'logodiv')
        for el in nodes:
            childNode=DSLNode(el,node)
            res=generate(childNode,level+1)
            if res:
                node.add(childNode)
                tokensCount+=1
        return True
    
    a = rule.get('min')
    b = rule.get('max')
    
    if b:
        cur=cur.copy()
        if node.key=='card' and node.parent.key=='div-3':
            cur.pop()
        n=random.randrange(a,b+1)
        for _ in range(n):
            elm=random.choice(cur)
            # if elm=='card':
            #     cur.remove('card')
            if elm in ['image','carousel','table','card']:
                for el in cur.copy():
                    if el in ['image','carousel','table','card']:
                        cur.remove(el)
            childNode=DSLNode(elm,node)
            res=generate(childNode,level+1)       
            if res:
                node.add(childNode)
                tokensCount+=1
            elif level+1>MAX_LEVELS or tokensCount>=MAX_TOKENS: break
        return True
    return False

def gen():
    global tokensCount
    tokensCount=0
    root=DSLNode('root',None)
    generate(root,0)
    return root.get_DSL()
    
if __name__=='__main__':
    for i in range(10):
        tokensCount=0
        root=DSLNode('root',None)
        generate(root,0)
        with open(f'DSL/{i}.dsl','w') as f:
            f.write(root.get_DSL())
    