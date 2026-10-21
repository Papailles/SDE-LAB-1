"""Esse4 - exams-service: returns the exam sessions."""
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Esse4 exams-service")

EXAMS = [
    {"id": 1, "course": "Service Design and Engineering", "date": "2026-01-15", "room": "A101"},
    {"id": 2, "course": "Distributed Systems", "date": "2026-01-22", "room": "B204"},
    {"id": 3, "course": "Databases", "date": "2026-02-02", "room": "C007"},
    {"id": 4, "course": "Software Architectures", "date": "2026-02-10", "room": "A102"},
]


@app.get("/exams")
def list_exams():
    return EXAMS


@app.get("/exams/{exam_id}")
def get_exam(exam_id: int):
    for exam in EXAMS:
        if exam["id"] == exam_id:
            return exam
    raise HTTPException(status_code=404, detail=f"exam {exam_id} does not exist")


@app.get("/health")
def health():
    return {"status": "ok", "service": "exams-service"}
