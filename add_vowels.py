# add_vowels.py
from sqlalchemy.orm import Session
from models import Vowel, Base
from database import engine, SessionLocal

Base.metadata.create_all(bind=engine)

def add_vowels():
    db: Session = SessionLocal()

    vowels = [
                             
        Vowel(vowel_char='a', audio_file='audio/a.wav'),
        Vowel(vowel_char='e', audio_file='audio/e.wav'),
        Vowel(vowel_char='ẹ', audio_file='audio/e_.wav'),
        Vowel(vowel_char='i', audio_file='audio/i.wav'),
        Vowel(vowel_char='ị', audio_file='audio/i_.wav'),
        Vowel(vowel_char='o', audio_file='audio/o.wav'),
        Vowel(vowel_char='ọ', audio_file='audio/o_.wav'),
        Vowel(vowel_char='u', audio_file='audio/u.wav'),
        Vowel(vowel_char='ụ', audio_file='audio/u_.wav'),
    ]

    db.add_all(vowels)
    db.commit()
    db.close()

if __name__ == "__main__":
    add_vowels()
