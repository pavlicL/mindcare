from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tijekom razvoja može *, u produkciji navedi točno: ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Privremena memorijska baza (dok ne dodamo pravu)
users_db: Dict[str, str] = {}

class User(BaseModel):
    username: str
    password: str

@app.post("/register")
def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Korisnik već postoji.")
    users_db[user.username] = user.password
    return {"message": "Registracija uspješna."}

@app.post("/login")
def login(user: User):
    if users_db.get(user.username) != user.password:
        raise HTTPException(status_code=401, detail="Neispravni podaci.")
    return {"message": "Prijava uspješna."}
