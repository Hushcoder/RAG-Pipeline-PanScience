from sqlalchemy import Column, Integer, String, Text
from backend.db.database import Base 

class Docum(Base):
    __tablename__ = 'Documents'

    doc_id = Column(Integer, primary_key=True, index=True)
    doc_type = Column(String(10), nullable=False)
    filename = Column(String(255), nullable=False)
    document_text = Column(Text, nullable=False)


  
