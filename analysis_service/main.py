from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tijekom razvoja može *, u produkciji navedi točno: ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NoteInput(BaseModel):
    note: str
EMOTION_KEYWORDS = {
    "sreća": [
        "dobar", "super", "odličan", "odlično", "sretan", "sretna", "veselje", "smijeh", "zadovoljan", "zadovoljna",
        "vesela", "uzbuđena", "zahvalna", "mirno", "opušteno", "divno", "predivno", "volim", "ispunjena", "sretnica"
    ],
    "tuga": [
        "loš", "tužno", "plačem", "usamljen", "depresivan", "depresivna", "nije dobro", "tužna", "prazna",
        "jadno", "slomljeno", "bezvoljna", "umorna", "odustajem", "težak dan", "sve je teško", "užas",
    ],
    "ljutnja": [
        "bijes", "ljut", "ljuta", "živcira", "mrzim", "nervozan", "nervozna", "frustracija", "bijesna", "nepravda",
        "svađa", "pukla sam", "ljutito", "poludjela", "iritira me"
    ],
    "strah": [
        "strah", "panika", "bojim se", "anksiozno", "napeto", "tjeskoba", "uplašena", "nervoza", "panika me hvata",
        "neizvjesnost", "nesigurna", "ne smijem", "izbjegavam", "panika"
    ],
    "neutralno": []
}


@app.post("/analyze-text")
def analyze_text(data: NoteInput):
    note = data.note.lower()
    for emotion, keywords in EMOTION_KEYWORDS.items():
        if any(keyword in note for keyword in keywords):
            return {"emotion": emotion}
    return {"emotion": "neutralno"}
