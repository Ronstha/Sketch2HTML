from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String,ForeignKey,DateTime,UniqueConstraint
from sqlalchemy.sql import func
import datetime
Base = declarative_base()
class UI(Base):
    __tablename__="ui"
    id=Column(Integer(),primary_key=True)
    name=Column(String(),nullable=True)
    root_node= Column(
      Integer, 
      ForeignKey('element.id',ondelete="CASCADE"), 
      nullable=False)
    node=relationship('Element',backref='ui',cascade='all, delete')
class Element(Base):
    __tablename__="element"
    id=Column(Integer(),primary_key=True)
    name=Column(String(),nullable=True)
    element=Column(String(),nullable=False)
    data=Column(String())
    parent_id = Column(Integer, ForeignKey('element.id'),nullable=True)
    parent = relationship("Element", back_populates="childrens", remote_side=[id])
    childrens = relationship("Element", back_populates="parent")

