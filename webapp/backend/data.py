from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
import os
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
            dat={
                'name':node.name,
                'id':node.id,
                'nodes':childrens,
              
                'element':node.element
            }
            dat.update(json.loads(node.data))
            return dat
        try:
            ui=self.session.query(UI).filter(UI.id==id).one_or_none()
            if ui==None:
                return {'error':'Not Found'},404
            return {
                'name':ui.name,
                'id':ui.id,
                'node':fillnode(ui.node)
            },200
        except Exception as e:
          
            return {'error':'Not Found'},404
    def add_image(self,url):
        try:
            img=Image(url=url)
            self.session.add(img)
            self.session.commit()
            return {'id':img.id,'url':url},200
        except:
            
            self.session.rollback()
            return {"error":"Unexpected Error occured"},400
    def remove_image(self,id):
        try:
            img=self.session.query(Image).filter(Image.id==id).one()
            if(not img.url.startswith('http')):
               try:
                 os.remove("images/"+img.url)
               except:
                   pass
            self.session.delete(img)
            self.session.commit()
            return {"success":True},200
        except:
            return {"error":"Unexpected Error occured"},400
    def get_images(self):
       return [{'id':i.id,'url':i.url} for i in self.session.query(Image).all()],200
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
            elm=self.session.query(UI).filter(UI.id==id).one()
            node=elm.node
            self.session.delete(elm)
            self.session.flush()
            self.session.delete(node)
            self.session.commit()
            return {'success':True},200
        except:
            import traceback
            print(traceback.format_exc())
            self.session.rollback()
            return {'error':'Not Found'},404