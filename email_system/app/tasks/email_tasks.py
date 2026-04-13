from app.celery_app import celery
from app.services.email_sender import send_email
from app.services.personalization import render
from app.services.suppression import is_blocked
import json

@celery.task(
    bind=True,
    name="app.tasks.email_tasks.send_email_task",
    autoretry_for=(Exception,),
    retry_backoff=True,       # exponential backoff
    retry_kwargs={"max_retries": 5}
)
def send_email_task(self, job_json):
    data = json.loads(job_json)

    email = data["email"]

    if is_blocked(email):
        return "skipped (blocked)"

    content = render(data)

    send_email(
        to_email=email,
        subject="Welcome!",
        content=content
    )

    return "sent"


from app.services.analytics import track_event

# inside task
track_event("sent")