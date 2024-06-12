import os
from django.utils import timezone
from django.core.mail import send_mail
from rest_framework.exceptions import NotFound

from .models import UserRegisterToken
from user_position.models import UserPosition


class AddEmployee:
    def __init__(self, email=None, position_id=None):
        self.position = UserPosition.objects.get(id=position_id) if position_id else None
        self.email = email

    def check_token(self, token):
        try:
            register_token = UserRegisterToken.objects.get(token=token, is_active=True)
            if register_token.expire_date < timezone.now():
                register_token.is_active = False
                register_token.save()
                raise NotFound('Token not valid!')
            return register_token
        except UserRegisterToken.DoesNotExist:
            raise NotFound('Token not valid!') 


    def generate_token(self):
        if token := UserRegisterToken.objects.filter(email=self.email, is_active=True).first():
            token.is_active = False
            token.save()
        token = UserRegisterToken.objects.create(email=self.email, position=self.position)
        return token.token
    
    def generate_token_url(self):
        token = self.generate_token()
        root_url = ''.join([os.getenv('FRONT_URL'), '/register/'])
        token_url = ''.join([root_url, str(token)])
        self.send_url(token_url)
        return token_url
    
    
    def send_url(self, token_url):
        send_mail(
            "Register in Inspection Report Register",
            f"Please use the link below to register in IRR:{token_url}",
            os.getenv('EMAIL_HOST_USER'),
            (self.email,),
            fail_silently=False
        )


