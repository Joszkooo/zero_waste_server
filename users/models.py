from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Domyślny model użytkownika dziedziczący po AbstractUser. 
    # Pozwala na łatwe rozszerzenie w przyszłości.
    pass
