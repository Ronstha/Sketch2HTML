from DSLrules import graph
class DSLNode:
    def __init__(self,key,parent):
        self.key=key
        self.parent=parent
        self.childrens=[]
    def add(self,child):
        self.childrens.append(child)
    def get_DSL(self,level=0):
        if self.key=="root":
            txts=[]
            for child in self.childrens:
                txts.append(child.get_DSL(level))
            return  "".join(txts)
    
        
        if len(self.childrens)==0:
            if graph.get(self.key)!=None: return ""
            dsl=level*'\t'+self.key
        else:
            dsl=level*'\t'+self.key+"{\n"
            
            for child in self.childrens:
                dsl+=child.get_DSL(level+1)+'\n'
                
            dsl+=level*'\t'+'}'
        return dsl
