# Python Imports
import hashlib
import uuid

# Django Imports
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator


from model_utils import Choices

from user_profile.managers import UserManager


def generate_uuid_with_phone(phone):
    hash_id = hashlib.sha256()
    hash_id.update(phone)
    return hash_id.hexdigest()


class TimeStampModel(models.Model):
    """
            Time Stamp Model which will be inherited by all the models.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
             This will tell django and the migration system this isn't a model we can use to store data with. However, we can inherit from it so that each model that we subclass with it has the fields, methods, and properties of the abstract model.
        """
        abstract = True


class UserProfile(AbstractBaseUser, PermissionsMixin, TimeStampModel):

    GENDER = Choices(
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    mobile = models.BigIntegerField(
        validators=[
            MinValueValidator(5000000000),
            MaxValueValidator(9999999999),
        ],
        unique=True,
        db_index=True
    )
    aadhaar_number = models.BigIntegerField(
        validators=[
            MinValueValidator(000000000000),
            MaxValueValidator(999999999999),
        ],
        unique=True,
        null=True
    )
    pan_detail = models.CharField(max_length=10, unique=True, null=True)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    display_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    gender = models.CharField(choices=GENDER, max_length=1, blank=False, default='M')
    address = models.CharField(max_length=1000, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    otp = models.IntegerField(blank=True, null=True)
    account_active = models.BooleanField(default=False)
    account_number = models.BigIntegerField(unique=True, null=True)
    ifsc_code = models.CharField(max_length=11, blank=False, null=False)
    password = models.CharField(max_length=100, blank=False, null=False)

    is_staff = models.BooleanField(
        default=False,
        help_text=(
            'Designates whether the user is a Django User and can log into Django Dashboard'
            ),
    )
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'mobile'

    def __str__(self):
        return str(self.mobile)

    def check_password(self, raw_password):
        if self.password == raw_password:
            return True
        else:
            return False
