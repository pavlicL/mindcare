from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from random import choice

app = FastAPI()

# ✅ Dodano za omogućavanje zahtjeva s frontenda
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tijekom razvoja može *, u produkciji navedi točno: ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Baza savjeta prema emocijama
ADVICE_MAP = {
    "sreća": [
        "Nastavi s aktivnostima koje te vesele!",
        "Zabilježi ovaj trenutak zahvalnosti.",
        "Podijeli svoju sreću s nekim."
    ],
    "tuga": [
        "Pokušaj razgovarati s nekim kome vjeruješ.",
        "Daj si vremena da obradiš emocije.",
        "Radi nešto što te inače smiruje – šetnja, glazba ili crtanje."
    ],
    "ljutnja": [
        "Udahni duboko i pokušaj preusmjeriti pažnju.",
        "Vježbanje može pomoći da izbaciš napetost.",
        "Izrazi ljutnju na zdrav način – napiši dnevnik."
    ],
    "strah": [
        "Zapiši čega se bojiš – to može pomoći da racionaliziraš osjećaje.",
        "Pokušaj tehniku uzemljenja – npr. 5 stvari koje vidiš.",
        "Prisjeti se trenutaka kada si savladala strah."
    ],
    "neutralno": [
        "Zabilježi male stvari koje ti podižu raspoloženje.",
        "Iskoristi dan za planiranje ili opuštanje.",
        "Neutralni dani su prilika za balans – nastavi s brigom o sebi."
    ]
}

@app.get("/advice/{emotion}")
def get_advice(emotion: str):
    advice_list = ADVICE_MAP.get(emotion.lower(), ["Trenutno nemamo savjet za ovu emociju."])
    return {"advice": choice(advice_list)}
