📧 Email Marketing System (FastAPI + Celery + Redis)

A high-volume, scalable outbound email sending system built with:

⚡ FastAPI (API layer)
🧠 Celery (distributed task queue)
🧵 Redis (message broker)
✉️ SMTP email sender
🎯 CSV-based campaign ingestion
🔁 Domain/IP rotation (extensible)
🚫 Bounce suppression system
🧩 Jinja2 personalization engine

🚀 Features
Upload CSV and send bulk emails
Asynchronous email processing (Celery workers)
Horizontal scalability (multiple workers)
Email personalization using templates
Redis-based queue system
Suppression list for bounced emails
Modular architecture (production-ready structure)

📦 Installation
1. Clone project
git clone <repo-url>
cd email_system

2. Create virtual environment
Windows
python -m venv venv
venv\Scripts\activate

Linux / Mac
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

Linux
sudo apt install redis-server
redis-server

Running the System
Step 1 — Start Celery Worker

celery -A app.celery_app.celery worker --loglevel=info --pool=solo

Step 2 — Start FastAPI server

uvicorn app.main:app --reload

Server runs at:

http://127.0.0.1:8000

API Usage
1. Upload CSV
Endpoint:

POST /upload-csv

Example CSV:

email,name,company
john@example.com,John,Google
alice@example.com,Alice,Amazon

cURL request:

curl -X POST "http://127.0.0.1:8000/upload-csv" \
-F "file=@sample.csv"

Response:

{
  "queued": 2
}

📧 Email Flow
CSV uploaded via API
FastAPI parses rows
Each row sent to Celery queue
Celery worker processes task
Email is personalized using Jinja2
SMTP sends email
Bounce system suppresses invalid emails

🧠 Personalization Example

Template:

Hello {{ name }},

Your company {{ company }} is invited to try our platform.

Thanks,
Team

Output:

Hello John,

Your company Google is invited to try our platform.

🔁 Celery Task

Task name:
app.tasks.email_tasks.send_email_task

⚙️ Configuration

Edit: app/core/config.py
SMTP_SERVERS = [
    {
        "host": "smtp.mail.com",
        "user": "user1",
        "pass": "pass1"
    }
]

REDIS_URL = "redis://localhost:6379/0"

Production scaling upgrades:
Redis Cluster
Kafka (for millions of emails)
AWS SES / SendGrid integration
Load-balanced workers

🧪 Testing

Check API docs: http://127.0.0.1:8000/docs


1. Production Architecture

                 ┌──────────────────────┐
                 │     FastAPI API      │
                 │ (Upload + Campaigns) │
                 └─────────┬────────────┘
                           │
                           v
                 ┌──────────────────────┐
                 │   Celery Broker      │
                 │      Redis           │
                 └─────────┬────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        v                  v                  v
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Celery Worker│  │ Celery Worker│  │ Celery Worker│
│ Email Sender │  │ Email Sender │  │ Email Sender │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       v                 v                 v
   SMTP / SES / SendGrid Providers (rotated domains/IPs)

       │
       v
┌──────────────────────┐
│ Bounce Webhook API   │
└─────────┬────────────┘
          v
┌──────────────────────┐
│ Suppression + Stats  │
│ Redis / DB Layer     │
└──────────────────────┘