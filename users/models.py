from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.password_validation import validate_password
from .managers import IRRUserManager


class BaseModel(models.Model):
    """Abstract Base model, for keeping base fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True,
                              error_messages={
                                  'unique': 'User with that email already exists.'
                              })
    position = models.ForeignKey('user_position.UserPosition', on_delete=models.CASCADE, related_name='users')
    password = models.CharField('password', max_length=128, validators=[validate_password])
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    objects = IRRUserManager()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email



