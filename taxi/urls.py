from django.urls import path
from taxi import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('drivers/', views.drivers_list.as_view()),
    path('drivers/new-driver/', views.driver_form.as_view()),
    path('drivers/<str:license_number>/delete/', views.driver_delete.as_view()),
    path('drivers/<str:license_number>/', views.driver_details.as_view()),
    path('orders/', views.orders_list.as_view()),
    path('orders/new-order/', views.order_form.as_view()),
    path('orders/<str:order_id>/delete/', views.order_delete.as_view()),
    path('orders/<str:order_id>/', views.order_details.as_view()),
    path('cars/', views.cars_list.as_view()),
    path('cars/<str:taxi_id>/', views.car_details.as_view()),
    path('error-page/', views.error_page.as_view()),
    path('', views.home.as_view())
    ]

#urlpatterns = format_suffix_patterns(urlpatterns)