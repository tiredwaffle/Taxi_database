from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import CharField, Value
from django.shortcuts import redirect
from taxi.models import Client, Order, Model, Model_detail, Driver, Driver_detail, Shift, Salary, Taxi, Taxi_detail

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser,FileUploadParser 
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework import generics
from rest_framework_csv.renderers import CSVRenderer

import csv
import json
import statistics
import random
import datetime

from django.views.generic import View
from django.http import HttpResponse

from .forms import DriverForm, ClientForm, OrderForm
import datetime


class home(APIView):
    def get(self, request, format = None):
        return render(request, "base_pages/home.html")

class error_page(APIView):
    def get(self, request, format = None):
        return render(request, "error_page.html")

class driver_form(APIView):
	def get(self, request, format = None):
		template_name = 'driver_new.html'
		form = DriverForm(request.POST or None)
		data = Driver_detail.objects.order_by('last_name').values('license_number','first_name','last_name', 'gender', 'birth_date', 'hire_date', 'mobile_number', 'city', 'street', 'number', 'postal_code')
		context = {'object_list': data,  'title': "Add new driver", 'form': form}
		return render(request,template_name, context)
	def post(self, request, format = None):
		form = DriverForm(data=request.data)
		if form.is_valid():
			obj = Driver_detail.objects.create(**form.cleaned_data)
			temp = Driver_detail.objects.get(license_number = form.cleaned_data.get('license_number'))
			obj2 = Driver.objects.create(license_number = temp)
		else:
			redirect("error-page/")
		return redirect("/drivers/")

class driver_delete(APIView):
	def get(self, request, license_number, format = None):
		Driver_detail.objects.filter(license_number=license_number).delete()
		return redirect("/drivers/")

class drivers_list(APIView):
	renderer_classes = [JSONRenderer, CSVRenderer, TemplateHTMLRenderer]
	template_name = 'drivers_list.html'
	def get(self, request, format = None):
		template_name = 'drivers_list.html'
		data = Driver_detail.objects.order_by('last_name').values('license_number','first_name','last_name', 'gender', 'birth_date', 'hire_date', 'mobile_number', 'city', 'street', 'number', 'postal_code')
		title = "List of drivers"
		context = {'object_list': data,  'title': title}
		return render(request,template_name, context)

class driver_details(APIView):
	renderer_classes = [JSONRenderer, CSVRenderer, TemplateHTMLRenderer]
	def get(self, request, license_number, format = None):
		template_name = 'driver_details.html'
		data_det = Driver_detail.objects.filter(license_number = license_number) 
		data_obj = Driver.objects.filter(license_number = data_det[0])   
		l_n = data_det[0].license_number
		data = Driver_detail.objects.filter(license_number = license_number)
		title = "Driver #"+ str(data_obj[0].driver_id)
		data_s = Salary.objects.filter(driver_id =  data_obj[0])
		context = {'l_n': l_n, 'object_list': data,  'title': title, 'sal':data_s}
		return render(request,template_name, context)

class order_form(APIView):
	def get(self, request, format = None):
		template_name = 'driver_new.html'
		form = OrderForm(request.POST or None)
		context = {'title': "Make your order!", 'form': form}
		return render(request,template_name, context)
	def post(self, request, format = None):
		form = OrderForm(data=request.data)
		if form.is_valid():
			temp = form.cleaned_data.get('mobile_number')
			obj1, create = Client.objects.get_or_create(mobile_number = temp)
			obj2 = Order()
			obj2.status = form.cleaned_data.get('status')
			obj2.number_people = form.cleaned_data.get('number_people')
			obj2.date_time_start = form.cleaned_data.get('date_time_start')
			obj2.date_time_end = form.cleaned_data.get('date_time_end')
			obj2.from_city = form.cleaned_data.get('from_city')
			obj2.from_street = form.cleaned_data.get('from_street')
			obj2.from_number = form.cleaned_data.get('from_number')
			obj2.to_city = form.cleaned_data.get('to_city')
			obj2.to_street = form.cleaned_data.get('to_street')
			obj2.to_number = form.cleaned_data.get('to_number')
			obj2.is_paid = form.cleaned_data.get('is_paid')
			obj2.client_id = Client.objects.get(mobile_number = form.cleaned_data.get('mobile_number'))
			size = len(Taxi.objects.all())
			avail = Shift.objects.filter(date_start_time__lt = obj2.date_time_start, date_end_time__gt = obj2.date_time_end)
			for obj in avail:
				if obj.taxi_id.license_plate.model_id.model_name.max_capacity > obj2.number_people:
					obj2.taxi_id = obj.taxi_id 
					obj2.save()
					return redirect('/orders/')
			return HttpResponse("Oops! It seems we don't have buses for your time and amount of people :(")
		else:
			return HttpResponse("Something went wrong! Check your connection with server!", status = status.HTTP_403_FORBIDDEN)

class order_delete(APIView):
	def get(self, request, order_id, format = None):
		Order.objects.filter(order_id=order_id).delete()
		return redirect("/orders/")

class orders_list(APIView):
	renderer_classes = [JSONRenderer, CSVRenderer, TemplateHTMLRenderer]
	def get(self, request, format = None):
		template_name = 'orders_list.html'
		data = Order.objects.order_by('order_id').all()
		title = "List of orders"
		context = {'object_list': data,  'title': title}
		return render(request,template_name, context)

class order_details(APIView):
	renderer_classes = [JSONRenderer, CSVRenderer, TemplateHTMLRenderer]
	def get(self, request, order_id, format = None):
		template_name = 'order_details.html'
		data = Order.objects.filter(order_id = order_id)
		title = "Order #"+ str(data[0].order_id)
		context = {'object_list': data,  'title': title}
		return render(request,template_name, context)

class car_delete(APIView):
	def get(self, request, taxi_id, format = None):
		Taxi.objects.filter(taxi_id=taxi_id).delete()
		return redirect("/orders/")

class cars_list(APIView):
	renderer_classes = [JSONRenderer, CSVRenderer, TemplateHTMLRenderer]
	def get(self, request, format = None):
		template_name = 'cars_list.html'
		data = Taxi.objects.order_by('taxi_id').all()
		title = "List of cars"
		context = {'object_list': data,  'title': title}
		return render(request,template_name, context)

class car_details(APIView):
	renderer_classes = [JSONRenderer, CSVRenderer, TemplateHTMLRenderer]
	def get(self, request, taxi_id, format = None):
		template_name = 'car_details.html'
		data = Taxi.objects.filter(taxi_id = taxi_id)
		title = "Car #"+ str(data[0].taxi_id)
		context = {'object_list': data,  'title': title}
		return render(request,template_name, context)
