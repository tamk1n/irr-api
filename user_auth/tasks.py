import os
from celery import shared_task

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

@shared_task
def send_otp_email(full_name, email, otp):
    context = {'full_name': full_name, 'otp': otp}
    
    subject = "Password reset"
    from_email = os.getenv('EMAIL_HOST_USER')
    to_email = email

    text_content = render_to_string('emails/password_reset_otp_email.txt', context)
    html_content = render_to_string('emails/password_reset_otp_email.html', context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)
        