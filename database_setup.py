import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Console(Base):
    
    __tablename__='console'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class ConsoleGame(Base):
    
    __tablename__='console_game'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(500))
    price = Column(String(8))
    publisher = Column(String(80))
    console_id = Column(Integer, ForeignKey('console.id'))
    console = relationship(Console)

    @property
    def serialize(self):
        #Returns object data in easily serializable format
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'publisher': self.publisher,
        }

engine = create_engine('sqlite:///consolegames.db')
Base.metadata.create_all(engine)
