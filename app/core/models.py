from django.db import models
from django.contrib.auth import get_user_model
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


class BaseModel(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class PlantFamilies(BaseModel):
    """Plant family"""


class PlantGenes(BaseModel):
    """Plant gene"""
    family = models.ForeignKey(PlantFamilies, on_delete=models.CASCADE)


class PlantSpecies(BaseModel):
    """Plant species"""
    gene = models.ForeignKey(PlantGenes, on_delete=models.CASCADE)


class PlaceType(BaseModel):
    """Place type"""


class Country(BaseModel):
    """Country"""


class Region(BaseModel):
    """Region"""
    country = models.ForeignKey(Country, on_delete=models.CASCADE)


class City(BaseModel):
    """City"""
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


class Town(BaseModel):
    """Town"""
    city = models.ForeignKey(City, on_delete=models.CASCADE)


class Project(BaseModel):
    """Project"""
    abreviation = models.CharField(max_length=255)
    projectLeader = models.ForeignKey(
                        get_user_model(),
                        on_delete=models.CASCADE
                    )
    beginYear = models.IntegerField()
    endYear = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
