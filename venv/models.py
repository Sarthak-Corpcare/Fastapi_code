from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)

'''
class Document:
    def __int__(self,doc_id:str,title:str, content:str):
        self.id=doc_id
        self.title=title
        self.content=content
'''