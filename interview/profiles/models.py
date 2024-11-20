from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import ImageField, EmailField


class UserProfile(AbstractBaseUser):
    avatar = ImageField(upload_to=None, height_field=720, width_field=1280, max_length=100)
    email = EmailField(unique=True)

    USERNAME_FIELD = 'email'
