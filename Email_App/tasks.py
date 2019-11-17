from celery import Celery
from datetime import date
from django.core import mail
from django.core.mail import EmailMessage
from django.conf import settings

# settings.configure()
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'Email_App.settings'

app = Celery('tasks', broker="redis://localhost:6379")


@app.task
def get_stats():
    print("Email Stats")

    # Importing Email.models
    import django
    django.setup()

    from Email.models import EmailStats

    query = EmailStats.objects.filter(timestamp__date=date.today())
    print(query.count())
    total_emails = "Total Emails: " + str(query.count())
    body = total_emails
    body += "\n\n"
    body += "Timestamps:\n"
    for q in query:
        print(q.timestamp)
        body += str(q.timestamp)
        body += "\n "

    email_to_admin = [settings.ADMIN_EMAIL]
    print(email_to_admin)
    from_email = settings.EMAIL_HOST_USER
    subject = 'Stats for the day.'

    connection = mail.get_connection()
    connection.open()

    print(subject, body, from_email, email_to_admin)
    email = EmailMessage(subject=subject, body=body, from_email=from_email,
                         to=email_to_admin)
    email.send(fail_silently=False)
    connection.close()


app.conf.beat_schedule = {
    "send_email_every_30_minutes": {
        "task": "tasks.get_stats",
        "schedule": 1800.0
    }
}