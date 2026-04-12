from app.celery_app import celery

@celery.task(name="app.tasks.email_tasks.send_email_task")
def send_email_task(job_json):
    import json
    from app.services.email_sender import send_email
    from app.services.personalization import render

    data = json.loads(job_json)

    content = render(data)

    send_email(
        to_email=data["email"],
        subject="Welcome!",
        content=content
    )

    return "sent"