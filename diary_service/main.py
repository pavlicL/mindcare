from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import aiohttp
import os

# Baza
DATABASE_URL = "sqlite:////data/diary.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

# FastAPI app
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model baze
class DiaryEntryModel(Base):
    __tablename__ = "entries"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    emotion = Column(String)
    note = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Pydantic modeli
class DiaryEntry(BaseModel):
    username: str
    note: str

class BulkEntries(BaseModel):
    entries: list[DiaryEntry]

# Baza dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Analiza emocije
async def analyze_emotion(note: str) -> str:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post("http://analysis_service:8002/analyze-text", json={"note": note}) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("emotion", "neutralno")
        except Exception as e:
            print("❌ Greška kod analize emocije:", e)
    return "neutralno"

# Dohvati savjet
async def fetch_advice(emotion: str) -> str:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"http://advice_service:8003/advice/{emotion}") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("advice", "")
        except Exception as e:
            print("❌ Greška kod dohvaćanja savjeta:", e)
    return "Savjet nije dostupan."

# Dodaj jedan unos
@app.post("/entry")
async def add_entry(entry: DiaryEntry, db: Session = Depends(get_db)):
    emotion = await analyze_emotion(entry.note)
    advice = await fetch_advice(emotion)

    new_entry = DiaryEntryModel(
        username=entry.username,
        note=entry.note,
        emotion=emotion
    )
    db.add(new_entry)
    db.commit()

    return {
        "message": "Unos spremljen",
        "emotion": emotion,
        "advice": advice
    }

# Dodaj više unosa
@app.post("/bulk-entry")
async def bulk_entry(data: BulkEntries, db: Session = Depends(get_db)):
    results = []
    for entry in data.entries:
        emotion = await analyze_emotion(entry.note)
        new_entry = DiaryEntryModel(
            username=entry.username,
            note=entry.note,
            emotion=emotion
        )
        db.add(new_entry)
        results.append({
            "note": entry.note,
            "emotion": emotion
        })
    db.commit()
    return {"status": "OK", "results": results}

# Dohvati unose po korisniku
@app.get("/entries/{username}")
def get_entries(username: str, db: Session = Depends(get_db)):
    return db.query(DiaryEntryModel)\
        .filter(DiaryEntryModel.username == username)\
        .order_by(DiaryEntryModel.timestamp).all()

# Info pri pokretanju
@app.on_event("startup")
def on_startup():
    print("📁 Working dir:", os.getcwd())
    print("📂 /data postoji:", os.path.exists("/data"))
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tablice OK")
    except Exception as e:
        print("❌ Greška:", e)
