from django.db import models
from django.conf import settings
from django.utils import crypto

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

User = settings.AUTH_USER_MODEL


class Client(models.Model):
	client_id = models.AutoField(primary_key=True)
	mobile_number = models.CharField(unique = True, max_length=15, default = '0682932790', null=False)

class Order(models.Model):
	COMPLETED = 'completed'
	CANCELLED = 'cancelled'
	IN_PROCESS = 'process'
	RESERVED = 'reserved'
	StatusOptions = [
		(COMPLETED, 'completed'),
		(CANCELLED, 'cancelled'),
		(IN_PROCESS, 'process'),
		(RESERVED, 'reserved'),
    ]
	status = models.CharField( max_length=10, choices=StatusOptions, default=IN_PROCESS)
	order_id = models.AutoField(primary_key=True)
	number_people = models.IntegerField(default = 1) 
	order_date_time = models.DateTimeField(auto_now_add=True)
	date_time_start = models.DateTimeField()
	date_time_end = models.DateTimeField()
	from_city = models.CharField(max_length=50, default = 'Groningen')
	from_street = models.CharField(max_length=50, default = 'Albertine')
	from_number = models.CharField(max_length=5, default = '1')
	to_city = models.CharField(max_length=50, default = 'Groningen')
	to_street = models.CharField(max_length=50, default = 'Albertine')
	to_number = models.CharField(max_length=5, default = '1')
	is_paid = models.BooleanField(default=False)
	client_id = models.ForeignKey('Client', to_field='client_id', on_delete=models.CASCADE) 
	taxi_id  = models.ForeignKey('Taxi', to_field='taxi_id', on_delete=models.CASCADE) 

class Model(models.Model):
	model_id = models.AutoField(primary_key=True) 
	model_name = models.ForeignKey('Model_detail', to_field='model_name', on_delete=models.CASCADE)

class Model_detail(models.Model):
	model_name = models.CharField(max_length=50, default = 'The car', primary_key=True)
	max_capacity = models.IntegerField(default = 1) 
 
class Driver(models.Model):
	driver_id = models.AutoField(primary_key=True)
	license_number = models.ForeignKey('Driver_detail', to_field='license_number', on_delete=models.CASCADE)
 
class Driver_detail(models.Model): 
	license_number = models.CharField(max_length=10, default = 'ABC123', primary_key=True)
	first_name = models.CharField(max_length=30, default = 'Mark', null = False, blank = False)
	last_name = models.CharField(max_length=30, default = 'Twen', null = False, blank = False)
	FEMALE = 'F'
	MALE = 'M'
	NON_BINARY = 'N'
	GenderOptions = [
		(FEMALE, 'female'),
		(MALE, 'male'),
		(NON_BINARY, 'non binary'),
    ]
	gender = models.CharField( max_length=1, choices=GenderOptions, default='N')
	birth_date = models.DateField()
	mobile_number = models.CharField(max_length=15, default = '0682932790', null=False)
	city = models.CharField(max_length=50, default = 'Groningen')
	street = models.CharField(max_length=50, default = 'Albertine')
	number = models.CharField(max_length=10, default = '1')
	postal_code = models.CharField(max_length=6, default = '9717EV')
	hire_date = models.DateField()
 
class Driver_adress(models.Model):
	city = models.CharField(max_length=50, default = 'Groningen')
	street = models.CharField(max_length=50, default = 'Albertine')
	number = models.CharField(max_length=10, default = '1')
	postal_code = models.CharField(max_length=6, default = '9717EV')

class Shift(models.Model):
	shift_id = models.AutoField(primary_key=True)
	date_start_time = models.DateTimeField()
	date_end_time = models.DateTimeField()
	taxi_id = models.ForeignKey('Taxi', to_field='taxi_id', on_delete=models.CASCADE)
	driver_id = models.ForeignKey('Driver', to_field='driver_id', on_delete=models.CASCADE)
 
class Salary(models.Model):
	driver_id = models.ForeignKey('Driver', to_field='driver_id', on_delete=models.CASCADE)
	from_date = models.DateField()
	to_date = models.DateField()
	salary = models.IntegerField(default = 0) 
 
class Taxi(models.Model):
	taxi_id = models.AutoField(primary_key=True)
	license_plate = models.ForeignKey('Taxi_detail', to_field='license_plate', on_delete=models.CASCADE)
 
class Taxi_detail(models.Model):
	license_plate = models.CharField(max_length=8, default = 'ABC123', primary_key=True)
	manufacture_year = models.IntegerField(default = 2000) 
	model_id = models.ForeignKey('Model', to_field='model_id', on_delete=models.CASCADE)
 