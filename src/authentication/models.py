from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
	use_in_migration = True

	def _create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError('Users require an email field')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)	
		return self._create_user(email, password, **extra_fields)	

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)	
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(email, password, **extra_fields)		



class User(AbstractUser):
	
	username = None
	email = models.EmailField(_('Email Address'), unique=True)
		
	objets = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	is_customer = models.BooleanField(default=True)
	is_employee = models.BooleanField(default=False)
	
	

class Customer(models.Model):
	MALE = 'MALE'
	FEMALE = 'FEMALE'

	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)
	
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='customer')
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	mobile = PhoneNumberField(max_length=12, unique=True)
	gender = models.CharField(max_length=6, choices=GENDER_CHOICES, verbose_name='Gender')
	birth_day = models.DateField()
	created_at = models.DateTimeField(default=timezone.now)	

class Employee(models.Model):
	MALE = 'MALE'
	FEMALE = 'FEMALE'

	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)

	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='employee')
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	mobile = PhoneNumberField(max_length=12, unique=True)
	
	nif = models.CharField(max_length=10, unique=True)
	niu = models.CharField(max_length=10, unique=True)
	gender = models.CharField(max_length=6, choices=GENDER_CHOICES, verbose_name='Gender')
	birth_day = models.DateField()
	created_at = models.DateTimeField(default=timezone.now)	
	workplace = models.CharField(max_length=100)
	designation = models.CharField(max_length=100)

