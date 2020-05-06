from django.contrib import admin

from .models import Client, Order, Model,Model_detail,Driver,Driver_detail,Taxi,Taxi_detail,Shift, Salary
# Register your models here.
admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Model)
admin.site.register(Model_detail)
admin.site.register(Driver)
admin.site.register(Driver_detail)
admin.site.register(Taxi)
admin.site.register(Taxi_detail)
admin.site.register(Shift)
admin.site.register(Salary)