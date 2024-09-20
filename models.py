# models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Vowel(Base):
    __tablename__ = 'vowels'

    id = Column(Integer, primary_key=True, index=True)
    vowel_char = Column(String, nullable=False)
    audio_file = Column(String, nullable=False)  # Path to vowel audio file

class TextRequest(Base):
    __tablename__ = 'text_requests'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    generated_audio_path = Column(String, nullable=True)
