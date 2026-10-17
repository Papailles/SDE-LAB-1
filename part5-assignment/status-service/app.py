"""Esse4 - status-service: "Is Esse4 down?" status page.

Calls GET /health on every service listed in the SERVICES env variable
(format: "name=url,name=url") and shows a green or red light for each one.
Shows the student name found in the STUDENT env variable.
"""
import html
import os

import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Esse4 status-service")

STUDENT = os.getenv("STUDENT", "unknown student")
SERVICES = os.getenv("SERVICES", "")
TIMEOUT = float(os.getenv("CHECK_TIMEOUT", "2"))


def parse_services(raw: str) -> dict:
    services = {}
    for item in raw.split(","):
        item = item.strip()
        if "=" in item:
            name, url = item.split("=", 1)
            services[name.strip()] = url.strip().rstrip("/")
    return services


def check(url: str) -> bool:
    try:
        return requests.get(f"{url}/health", timeout=TIMEOUT).status_code == 200
    except requests.RequestException:
        return False


def check_all() -> dict:
    return {name: check(url) for name, url in parse_services(SERVICES).items()}


@app.get("/api/status")
def api_status():
    return {"student": STUDENT, "services": {n: ("up" if ok else "down") for n, ok in check_all().items()}}


@app.get("/health")
def health():
    return {"status": "ok", "service": "status-service"}


@app.get("/", response_class=HTMLResponse)
def index():
    rows = ""
    for name, ok in check_all().items():
        color = "#2ecc71" if ok else "#e74c3c"
        label = "UP" if ok else "DOWN"
        rows += (
            f'<div class="row"><span class="dot" style="background:{color}"></span>'
            f'<span class="name">{html.escape(name)}</span>'
            f'<span class="label" style="color:{color}">{label}</span></div>'
        )
    if not rows:
        rows = "<p>No service configured (set the SERVICES env variable).</p>"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="3">
  <title>Esse4 status</title>
  <style>
    body {{ font-family: system-ui, sans-serif; background:#f4f6f8; margin:0; padding:40px; }}
    .card {{ max-width:480px; margin:auto; background:#fff; border-radius:12px;
             padding:28px 32px; box-shadow:0 2px 12px rgba(0,0,0,.1); }}
    h1 {{ margin:0 0 4px; }}
    .student {{ color:#666; margin-bottom:24px; }}
    .row {{ display:flex; align-items:center; padding:12px 0; border-top:1px solid #eee; }}
    .dot {{ width:18px; height:18px; border-radius:50%; margin-right:14px; }}
    .name {{ flex:1; font-size:1.1rem; }}
    .label {{ font-weight:700; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>Is Esse4 down?</h1>
    <div class="student">Student: <strong>{html.escape(STUDENT)}</strong></div>
    {rows}
  </div>
</body>
</html>"""
