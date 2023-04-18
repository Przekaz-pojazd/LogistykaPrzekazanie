import re
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin,
                                        AbstractUser)
from django.core.exceptions import ValidationError
from django.core.validators import (RegexValidator,
                                    MinValueValidator,
                                    MaxValueValidator)
def email_validator(email_add):
    if re.match(r'([A-Za-z0-9]{25}[.-_]*[A-Za-z0-9]{10}@([A-Za-z]{10})+(\.[A-Za-z]{2,}))', email_add):
        return ValidationError("Email is not propertly")

def zip_code_valid(zip_code):
    if re.match(r'^([0-9]{2})+-([0-9]{3})', zip_code):
        return ValidationError("Zip code isnt properly")

def mobile_address_valid(mobile_phone):
    if not re.match(r'^([1-9]{1})+[0-9]{8}', mobile_phone):
        return ValidationError("Mobile phone is not properly")


class AppUserManager(BaseUserManager):
	def create_user(self, name, surname, city, region, zip_code,
					email_address, mobile_phone, password=None, **extra_fields):
		if not name:
			raise ValueError("Please enter you name")
		if not surname:
			raise ValueError("Please enter you name")
		if not city:
			raise ValueError("Please enter you city")
		if not region:
			raise ValueError("Please enter you name")
		if not zip_code:
			raise ValueError("Please enter zip code:")

		user = self.model(
			name=name,
			surname=surname,
			city=city,
			region=region,
			zip_code=zip_code,
			email_address=self.normalize_email(email_address),
			mobile_phone=mobile_phone,
			**extra_fields
		)
		user.set_password(user.password)
		user.save(using=self._db)
		return user

	def create_superuser(self, name, surname, city, region, zip_code,
						 email_address, mobile_phone, password=None, **extra_fields):
		user = self.create_user(
			name=name,
			surname=surname,
			city=city,
			region=region,
			zip_code=zip_code,
			email_address=email_address,
			mobile_phone=mobile_phone,
			password=password,
			**extra_fields
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class AppUser(AbstractBaseUser, PermissionsMixin):
	name = models.CharField(max_length=40, blank=False)
	surname = models.CharField(max_length=40, blank=False)
	city = models.CharField(max_length=40, blank=False)
	region = models.CharField(max_length=60, blank=False)
	email = models.EmailField(max_length=50, unique=True)
	password = models.CharField(max_length=200, blank=False)
	zip_code = models.CharField(max_length=6,
								validators=[zip_code_valid], blank=False)
	mobile_phone = models.CharField(max_length=9, validators=[mobile_address_valid],
									unique=False, blank=True)
	username = models.CharField(max_length=50, blank=True)

	is_superuser = models.BooleanField(default=False, blank=False)
	is_staff = models.BooleanField(default=False, blank=False)
	is_admin = models.BooleanField(default=False, blank=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['password']
	objects = AppUserManager()

	def __str__(self):
		return self.email


from django.core.validators import (RegexValidator,
                                    MinValueValidator,
                                    MaxValueValidator,
                                    ValidationError)


def registration_num_validator(reg_num):
    if re.match(r'([A-Z]{2,3})([0-9]{4,5})', reg_num):
        return ValidationError("Register num is not proper")


class Truck(models.Model):
    CHOICES = (
        ('Wol', 'Wolny'),
        ('Zaj', 'Zajety'),
        ('Awar', 'Awaria')
    )
    brand = models.CharField(max_length=20, blank=False)
    model = models.CharField(max_length=40, blank=False)
    power = models.IntegerField(blank=False,
                                validators=[MinValueValidator(300), MaxValueValidator(999)])
    registration_number = models.CharField(max_length=8,
                                           blank=False,
                                           validators=[registration_num_validator], unique=True)
    driven_length = models.IntegerField(blank=False)
    production_date = models.DateField(blank=False)
    avaiable = models.CharField(choices=CHOICES, blank=False, max_length=4)

    def __str__(self):
        return self.registration_number

class TruckEquipment(models.Model):
    CHOICES = (
        ('Wol','Wolny'),
        ('Zaj','Zajety'),
        ('Awar','Awaria')
    )
    truck = models.ForeignKey(Truck,
                              on_delete=models.CASCADE,
                              blank=False)
    chest = models.BooleanField(default=True, blank=False)
    chains = models.BooleanField(default=True, blank=False)
    jack_hitch = models.BooleanField(default=True, blank=False)
    planetar_key = models.BooleanField(default=True, blank=False)
    manometer = models.BooleanField(default=True, blank=False)
    avaiable = models.CharField(choices=CHOICES, blank=False,max_length=4)
    tire_pumping_wire = models.BooleanField(default=True, blank=False)
    complete_status = models.BooleanField(default=True)
    def __str__(self):
        return str(self.truck)

    def status_checker(self):
        if all(self.chest, self.chains, self.jack_hitch,
               self.planetar_key, self.manometer, self.tire_pumping_wire):
            self.complete_status = True
        self.complete_status = False


class SemiTrailer(models.Model):
    brand = models.CharField(max_length=20, blank=False)
    model = models.CharField(max_length=40, blank=False)
    production_year = models.DateField()
    registration_number = models.CharField(max_length=8,
                                           blank=False,
                                           validators=[registration_num_validator], unique=True)

    semi_note = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return self.registration_number

class SemiTrailerEquipment(models.Model):
    semi_trailer = models.ForeignKey(SemiTrailer,
                                     on_delete=models.CASCADE,
                                     blank=False)
    belts = models.IntegerField(default=6,
                                validators=[MinValueValidator(6),
                                            MaxValueValidator(12)])
    corners = models.IntegerField(default=8,
                                  validators=[MinValueValidator(8),
                                              MaxValueValidator(16)])
    aluminium_stick = models.IntegerField(default=12,
                                          validators=[MinValueValidator(12),
                                                      MaxValueValidator(20)])
    wide_stick = models.IntegerField(default=2,
                                     validators=[MinValueValidator(2),
                                                 MaxValueValidator(6)])
    ladder = models.BooleanField(default=True, blank=False)
    roof_stick = models.BooleanField(default=True, blank=False)
    dimenstion_board = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return self.semi_trailer.id


class VehicleReceivment(models.Model):
    truck = models.ForeignKey(Truck,
                              on_delete=models.CASCADE,
                              blank=Truck)

    semi_trailer = models.ForeignKey(SemiTrailer,
                                     on_delete=models.CASCADE,
                                     blank=False)
    data_created = models.DateField(auto_created=True)
    data_ended = models.DateField()
    user = models.ForeignKey(AppUser,
                             on_delete=models.CASCADE,
                             blank=False)

    def __str__(self):
        return self.id