import os

from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from config import settings


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}

GENDER_CHOOSES = [
    ('erkak', 'Erkak'),
    ('ayol', 'Ayol'),
]

STATUS_CHOOSES = [
    ('yangi_k', 'Yangi kitobxon'),
    ('k', 'Kitobxon'),
    ('kuchli_k', 'Kuchli kitobxon'),
]


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOOSES, default='')
    status = models.CharField(max_length=30, choices=STATUS_CHOOSES, default='yangi_k')
    birth_date = models.DateField(null=True, blank=True)
    # image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True,
                              default=os.path.join(settings.MEDIA_ROOT, 'profile_images/user_profil.jpg'))

    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
