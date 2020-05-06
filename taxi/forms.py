from django import forms
import datetime

class DriverForm(forms.Form):
	YEARS= [x for x in range(1940,2021)]
	license_number = forms.CharField()
	first_name = forms.CharField()
	last_name = forms.CharField()
	FEMALE = 'F'
	MALE = 'M'
	NON_BINARY = 'N'
	GenderOptions = [
		(FEMALE, 'female'),
		(MALE, 'male'),
		(NON_BINARY, 'non binary'),
    ]
	gender = forms.MultipleChoiceField(choices= GenderOptions)
	birth_date = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))
	mobile_number = forms.CharField()
	city = forms.CharField()
	street = forms.CharField()
	number = forms.CharField()
	postal_code = forms.CharField()
	hire_date = forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget)

class ClientForm(forms.Form):
	mobile_number = forms.CharField()

class OrderForm(forms.Form):
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
	status = forms.MultipleChoiceField(choices= StatusOptions)
	number_people = forms.IntegerField() 
	date_time_start = forms.DateTimeField(help_text = "Input format \'yyyy-mm-dd hh:mm\'")
	date_time_end = forms.DateTimeField(help_text = "Input format \'yyyy-mm-dd hh:mm\'")
	from_city = forms.CharField()
	from_street = forms.CharField()
	from_number = forms.CharField()
	to_city = forms.CharField()
	to_street = forms.CharField()
	to_number = forms.CharField()
	mobile_number = forms.CharField()
	is_paid = forms.BooleanField()
	client_id = 0

#DateField(initial=datetime.date.today)
#forms.BooleanField(required=False)
#DateTimeField]
