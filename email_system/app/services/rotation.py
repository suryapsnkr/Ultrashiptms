# rotation.py
from app.core.config import SMTP_SERVERS, IP_POOL

smtp_index = 0
ip_index = 0

def get_smtp():
    global smtp_index
    smtp = SMTP_SERVERS[smtp_index % len(SMTP_SERVERS)]
    smtp_index += 1
    return smtp

def get_ip():
    global ip_index
    ip = IP_POOL[ip_index % len(IP_POOL)]
    ip_index += 1
    return ip