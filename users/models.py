from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password, username):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username must be entered")
        if not password:
            raise ValueError("Password is required")  
        user = self.model (email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username):
        user = self.create_user(email, password,  username)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
        
class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=200)
    username = models.CharField(unique=True, max_length=100)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.email

class Profile(models.Model):
    pic = models.URLField()
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    def __str__(self):
        return f"Profile of {self.user.email}"