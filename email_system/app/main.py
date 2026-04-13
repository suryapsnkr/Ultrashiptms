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


# bounce endpoint (add in main.py)
from app.services.suppression import add_block
from fastapi import Request
from pydantic import BaseModel

class BounceSchema(BaseModel):
    email: str

@app.post("/webhook/bounce")
async def bounce(data: BounceSchema):
    add_block(data.email)
    return {"status": "blocked", "email": data.email}