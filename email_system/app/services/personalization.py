# personalization.py
from jinja2 import Template

EMAIL_TEMPLATE = """
Hello {{ name }},

We noticed your company {{ company }} might benefit from our solution.

Regards,
Growth Team
"""

def render(data):
    return Template(EMAIL_TEMPLATE).render(**data)