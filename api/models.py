from typing import Self
from django.db import models
import uuid
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .managers import UserManager
from django.utils.translation import gettext_lazy as _
# Create your models here.

DEGREE_CHOICES = [
    ('BSc', 'BSc'),
    ('OND', 'OND'),
    ('HND', 'HND'),
    ('CERTIFICATE', 'CERTIFICATE'),
    ("SSCE", "SSCE"),
]

PREFERRED_JOB = [
    ('Cosmetics/Skin Care', 'Cosmetics/Skin Care'),
    ('Pharmacy/Consumables/Surgicals', 'Pharmacy/Consumables/Surgicals'),
    ('Electronics/Electricals', 'Electronics/Electricals'),
    ('Clothings/Boutiques', 'Clothings/Boutiques'),
    ("BuildingMaterials", "BuildingMaterials"),
    ("Computers/Phones/Accessories/Software",
     "Computers/Phones/Accessories/Software"),
    ("FoodStores/Drinks/Wines", "FoodStores/Drinks/Wines"),
    ("SpareParts and Automobiles", "SpareParts and Automobiles"),

]


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True,)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.')
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        )
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["full_name"]
    objects = UserManager()

    def profile_type(self, user):
        """
        Given a user instance, returns 'BusinessOwner', 'Graduate',
        or 'None' based on attached profiles.
        """
        # Check for a related BusinessOwner
        if hasattr(user, 'business_owner'):
            return 'BusinessOwner'
        # Check for a related Graduate
        elif hasattr(user, 'graduate'):
            return 'Graduate'
        # Default
        return 'None'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return "email" + self.email


class Graduate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='graduate')

    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    profile_picture = models.ImageField(
        upload_to='profile_pictures', null=True, blank=True)
    address = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    course_studied = models.CharField(max_length=255)
    year_of_graduation = models.DateField()
    degrees_obtained = ArrayField(
        models.CharField(max_length=225, choices=DEGREE_CHOICES),
        default=list,
        blank=True
    )
    skills = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    aspirations = models.CharField(max_length=255)
    preffered_job = ArrayField(models.CharField(
        max_length=225, choices=PREFERRED_JOB), default=list, blank=True)
    relocate = models.CharField(max_length=255)
    cv = models.FileField(upload_to='cv', null=True, blank=True)
    relocation_availability = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    comments = models.TextField()

    reference = models.CharField(max_length=255)
    reference_phone_number = models.CharField(max_length=15)
    reference_relationship = models.CharField(max_length=225)
    reference_1 = models.CharField(max_length=255)
    reference_phone_number_1 = models.CharField(max_length=15)
    reference_relationship_1 = models.CharField(max_length=225)

    def __str__(self):
        return self.user
