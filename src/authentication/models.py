from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
	MALE = 'MALE'
	FEMALE = 'FEMALE'

	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)

	username = None
	email = models.EmailField(_('Email Address'), unique=True)
	mobile = PhoneNumberField(max_length=12, unique=True)
	gender = models.CharField(max_length=6, choices=GENDER_CHOICES, verbose_name='Gender')
	is_customer = models.BooleanField(default=True)
	is_employee = models.BooleanField(default=False)
	birth_day = models.DateField()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='customer')
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	created_at = models.DateTimeField(default=timezone.now)	

class Employee(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='employee')
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	nif = models.CharField(max_length=10, unique=True)
	niu = models.CharField(max_length=10, unique=True)
	created_at = models.DateTimeField(default=timezone.now)	
	workplace = models.CharField(max_length=100)
	designation = models.CharField(max_length=100)

