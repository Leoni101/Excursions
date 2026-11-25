from django.contrib import admin
from .models import Category, Excursion


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Excursion)
class ExcursionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "price", "duration", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("title", "description")
