from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "excursion", "user", "date", "participants", "is_cancelled")
    list_filter = ("is_cancelled", "date")
    search_fields = ("user__full_name", "user__email", "excursion__title")
