import os
from celery import shared_task

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from user_position.models import UserPosition
from report.models import ReportObservation

User = get_user_model()

@shared_task
def send_daily_report():
    employee = UserPosition.objects.get(id=2)
    users = User.objects.filter(is_active=True,position=employee).all()

    for user in users:
        observations = ReportObservation.objects.get_open_obs(user)
        due_obs = observations.filter(deadline=timezone.now().date())
        context = {'observations': observations, 'due_obs': due_obs}
        
        subject = "Sizin gündəlik hesabatınız"
        from_email = os.getenv('EMAIL_HOST_USER')
        to_email = user.email

        text_content = render_to_string('emails/daily_report_email.txt', context)
        html_content = render_to_string('emails/daily_report_email.html', context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        