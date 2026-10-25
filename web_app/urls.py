from django.urls import path
from . import views

app_name = "web_app" 

urlpatterns = [
    path('', views.index, name='index'),
    path('excursions/', views.excursion_list, name='excursion_list'),
    path('excursions/<int:excursion_id>/', views.excursion_detail, name='excursion_detail'),
    path('bookings/', views.booking_list, name='booking_list'),
]