from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
import json
class Db:
    def __init__(self):
        self.engine = create_engine('sqlite:///data.db?check_same_thread=False')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind = self.engine)
        self.session = Session()
    def get_ui(self):
        return {"data":[{'name':ui.name,'id':ui.id} for ui in self.session.query(UI).all()]}
    def fill_ui(self,node,parent=None):
        dat=node.copy()
        del dat['name']
        del dat['element']
        del dat['nodes']
        elm=Element(name='',element=node['element'],data=json.dumps(dat),parent_id=parent)
        self.session.add(elm)
        self.session.flush()
        for i in node['nodes']:
            self.fill_ui(i,elm.id)
            
        return elm.id
        
        
    def create_ui(self,data):
        try:
            ui=UI(name='',root_node=self.fill_ui(data))
            self.session.add(ui)
            self.session.commit()
            return {'id':ui.id,'name':ui.name}
        except Exception as e:
            
            self.session.rollback()
            return {'error':'Not Found'}

    def getbyid(self,id):
        def fillnode(node):
            if len(node.childrens)==0:
                childrens=[]
            else:
                childrens=[fillnode(n) for n in node.childrens]
            return {
                'name':node.name,
                'id':node.id,
                'parent':node.parent.id,
                'childrens':childrens,
                'data':json.loads(node.data)
            }
        try:
            ui=self.session.query(UI).filter(UI.id==id).one_or_none()
            if ui==None:
                return {'error':'Not Found'},404
            return {
                'name':ui.name,
                'id':ui.id,
                'node':fillnode(ui.node)
            },200
        except:
            return {'error':'Not Found'},404
    def update_ui_name(self,id,name):
        try:
            ui=self.session.query(UI).filter(UI.id==id).one()
            ui.name=name
            self.session.commit()
            return {'success':True},200
        except:
            self.session.rollback()
            return {'error':'Not Found'},404
    def update_data(self,id,name,data):
        try:
            elm=self.session.query(Element).filter(Element.id==id).one()
            elm.name=name
            elm.data=json.dumps(data)
            self.session.commit()
            return {'success':True},200
        except:
            self.session.rollback()
            return {'error':'Not Found'},404
    def delete_ui(self,id):
        try:    
            self.session.delete(self.session.query(UI).filter(UI.id==id).one())
            self.session.commit()
            return {'success':True},200
        except:
            self.session.rollback()
            return {'error':'Not Found'},404