from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using  email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class PlantFamilies(models.Model):
    """Plant family"""
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name


class PlantGenes(models.Model):
    """Plant gene"""
    name = models.CharField(max_length=255, blank=False)
    family = models.ForeignKey(PlantFamilies, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PlantSpecies(models.Model):
    """Plant species"""
    name = models.CharField(max_length=255, blank=False)
    gene = models.ForeignKey(PlantGenes, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PlaceType(models.Model):
    """Place type"""
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=200, blank=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
