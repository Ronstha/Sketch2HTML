from .DSLrules import graph
import random
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
            return  "\n".join(txts)
       
        if (self.key in ['text','button']) and (self.parent.key[:4]!="flex" and self.parent.key!='logodiv'):
            r=random.random()
            if self.key=='text' and self.parent=='footer':
                if r<0.7:
                    self.key+='-c'
                elif r>0.9:
                    self.key+='-r'
                    
                    
            elif r<0.3:
                self.key+='-c'
            elif r>0.85:
                self.key+'-r'
        elif self.key=='flex':
            r=random.random()
            if r<0.3:
                self.key+='-sb'
            elif r<0.65:
                self.key+='-c'
            elif r>0.85:
                self.key+='-r'
                
        if len(self.childrens)==0:
            if graph.get(self.key)!=None: return ""
            dsl=level*'\t'+self.key
        else:
            dsl=level*'\t'+self.key+"{\n"
            
            for child in self.childrens:
                dsl+=child.get_DSL(level+1)+'\n'
                
            dsl+=level*'\t'+'}'
        return dsl
 