"""Esse4 - booking-service.

Receives a booking request, checks with exams-service (REST call over the
internal network) that the exam exists, then stores the booking in Postgres.
"""
import logging
import os
import time

import psycopg2
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("booking")

EXAMS_URL = os.getenv("EXAMS_URL", "http://localhost:8000")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "esse4")
DB_USER = os.getenv("DB_USER", "esse4")
DB_PASSWORD = os.getenv("DB_PASSWORD", "esse4")

app = FastAPI(title="Esse4 booking-service")


class BookingRequest(BaseModel):
    student: str
    exam_id: int


def get_connection(retries: int = 10, delay: float = 1.0):
    """Connect to Postgres, retrying: 'depends_on' does not wait for db readiness."""
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            return psycopg2.connect(
                host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
                user=DB_USER, password=DB_PASSWORD, connect_timeout=3,
            )
        except psycopg2.OperationalError as exc:
            last_error = exc
            log.warning("db not ready (attempt %d/%d) at %s:%s", attempt, retries, DB_HOST, DB_PORT)
            time.sleep(delay)
    log.error("cannot connect to db at %s:%s: %s", DB_HOST, DB_PORT, last_error)
    raise HTTPException(status_code=503, detail="database unavailable")


@app.post("/bookings")
def create_booking(req: BookingRequest):
    url = f"{EXAMS_URL}/exams/{req.exam_id}"
    log.info("REST call: GET %s", url)
    try:
        resp = requests.get(url, timeout=3)
    except requests.RequestException as exc:
        log.error("cannot reach exams-service at %s: %s", url, exc)
        raise HTTPException(status_code=503, detail="exams-service unavailable")

    log.info("exams-service answered %s", resp.status_code)
    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail=f"exam {req.exam_id} does not exist")
    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail="unexpected answer from exams-service")

    course = resp.json()["course"]

    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO bookings (student, exam_id, course) VALUES (%s, %s, %s) RETURNING id",
                (req.student, req.exam_id, course),
            )
            booking_id = cur.fetchone()[0]
    finally:
        conn.close()

    log.info("booking %s saved for %s (exam %s)", booking_id, req.student, req.exam_id)
    return {"id": booking_id, "student": req.student, "exam_id": req.exam_id, "course": course}


@app.get("/bookings")
def list_bookings():
    conn = get_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.execute("SELECT id, student, exam_id, course FROM bookings ORDER BY id")
            rows = cur.fetchall()
    finally:
        conn.close()
    return [{"id": r[0], "student": r[1], "exam_id": r[2], "course": r[3]} for r in rows]


@app.get("/health")
def health():
    return {"status": "ok", "service": "booking-service"}
