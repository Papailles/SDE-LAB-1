"""Esse4 - grades-service: returns the published grades."""
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Esse4 grades-service")

GRADES = [
    {"id": 1, "student": "Tiziano Ferro", "course": "Service Design and Engineering", "grade": 30},
    {"id": 2, "student": "Laura Pausini", "course": "Distributed Systems", "grade": 28},
    {"id": 3, "student": "Eros Ramazzotti", "course": "Databases", "grade": 26},
    {"id": 4, "student": "Elisa Toffoli", "course": "Software Architectures", "grade": 29},
]


@app.get("/grades")
def list_grades():
    return GRADES


@app.get("/grades/{grade_id}")
def get_grade(grade_id: int):
    for grade in GRADES:
        if grade["id"] == grade_id:
            return grade
    raise HTTPException(status_code=404, detail=f"grade {grade_id} does not exist")


@app.get("/health")
def health():
    return {"status": "ok", "service": "grades-service"}
