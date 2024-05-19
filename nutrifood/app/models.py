from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    
# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)  # Поле для даты рождения
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Поле для роста в сантиметрах
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # Поле для веса в килограммах

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Здесь можно указать другие поля, которые вы хотите запрашивать при создании суперпользователя

    objects = CustomUserManager()


    def __str__(self):
        return self.email

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    

class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, default="avatar.svg")

    def __str__(self):
        return f"Photo for {self.product.name}"
    
    def delete_photo(self):
        self.photo.delete()
        self.delete()

        