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


class Place(BaseModel):
    """Place"""
    type = models.ForeignKey(PlaceType, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, null=True, blank=True)
    codeSite = models.CharField(max_length=200)
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    latitudeLambert72 = models.DecimalField(
            max_digits=13,
            decimal_places=10,
            null=True,
            blank=True
        )
    longitudeLambert72 = models.DecimalField(
            max_digits=13,
            decimal_places=10,
            null=True,
            blank=True
        )
    latitudeDec = models.DecimalField(max_digits=13, decimal_places=10)
    longitudeDec = models.DecimalField(max_digits=13, decimal_places=10)


class Project(BaseModel):
    """Project"""
    abreviation = models.CharField(max_length=255)
    projectLeader = models.ForeignKey(
                        get_user_model(),
                        on_delete=models.CASCADE,
                        related_name='projectLeader'
                    )
    beginYear = models.IntegerField()
    endYear = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    places = models.ManyToManyField(Place)
    members = models.ManyToManyField(
                    get_user_model(),
                    through='ProjectMembership',
                    related_name='members'
                )


class ProjectMembership(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)


class InsectSuperFamilies(BaseModel):
    """Insect super families"""


class InsectFamilies(BaseModel):
    """Insect families"""
    superFamily = models.ForeignKey(
                            InsectSuperFamilies,
                            on_delete=models.CASCADE
                        )


class InsectSubFamilies(BaseModel):
    """Insect sub families"""
    family = models.ForeignKey(InsectFamilies, on_delete=models.CASCADE)


class InsectTribes(BaseModel):
    """Insect tribes"""
    subFamily = models.ForeignKey(InsectSubFamilies, on_delete=models.CASCADE)


class InsectGenes(BaseModel):
    """Insect genes"""
    tribe = models.ForeignKey(InsectTribes, on_delete=models.CASCADE)


class InsectSpecies(BaseModel):
    """Insect species"""
    gene = models.ForeignKey(InsectGenes, on_delete=models.CASCADE)
