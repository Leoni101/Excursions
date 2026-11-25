from django.urls import path
from . import views

app_name = "excursions"

urlpatterns = [
    path("", views.excursion_list, name="excursion_list"),
    path("<int:excursion_id>/", views.excursion_detail, name="excursion_detail"),
    path("available/", views.available_excursions, name="available"),
]