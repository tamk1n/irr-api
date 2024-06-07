import uuid
from datetime import timedelta
from datetime import datetime

from django.db import models
from users.models import *



class UserRegisterToken(BaseModel):
    email = models.EmailField()
    position = models.ForeignKey('user_position.UserPosition', on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    expire_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.expire_date = datetime.now() + timedelta(days=7)
        return super().save()

    def __str__(self) -> str:
        return f'{self.email} {self.token}'
