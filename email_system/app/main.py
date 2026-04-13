# main.py
from fastapi import FastAPI, UploadFile, File
import csv, io, json
from app.tasks.email_tasks import send_email_task

app = FastAPI()

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    content = await file.read()
    stream = io.StringIO(content.decode())

    reader = csv.DictReader(stream)

    count = 0
    for row in reader:
        send_email_task.delay(json.dumps(row))
        count += 1

    return {"queued": count}

from pydantic import BaseModel
from typing import Optional, Dict, Any

class EmailEvent(BaseModel):
    event: Optional[str] = None
    email: Optional[str] = None
    recipient: Optional[str] = None
    notificationType: Optional[str] = None
    mail: Optional[Dict[str, Any]] = None

from fastapi import Body
from app.services.suppression import add_block, add_temp_block

@app.post("/webhook/email-events")
async def email_events(data: EmailEvent = Body(...)):
    
    # normalize event
    event_type = (data.event or data.notificationType or "").lower()

    # extract email
    email = (
        (data.email.strip() if data.email else None)
        or (data.recipient.strip() if data.recipient else None)
        or (
            data.mail.get("destination")[0].strip()
            if data.mail and data.mail.get("destination")
            else None
        )
    )

    if email:
        email = email.lower()

    if not email:
        return {"error": "Email not found"}

    # same logic
    if event_type in ["bounce", "hard_bounce"]:
        add_block(email)
        status = "permanent_block"

    elif event_type in ["complaint", "spam"]:
        add_block(email)
        status = "complaint_block"

    elif event_type in ["soft_bounce"]:
        add_temp_block(email)
        status = "temporary_block"

    else:
        status = "ignored"

    return {
        "status": status,
        "email": email,
        "event": event_type
    }

from app.services.analytics import get_stats

@app.get("/stats")
def stats():
    return get_stats()

from app.core.redis_client import redis_client

@app.post("/reset-stats")
def reset_stats():
    redis_client.delete("stats:sent", "stats:failed", "stats:bounced")
    return {"status": "reset"}