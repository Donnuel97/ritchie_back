from django.contrib import admin

# Register your models here.
from .models import CustomUser  # Import your model here

# Create a custom admin class if needed
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')  # Fields to display in the list view
    search_fields = ('username', 'email')  # Fields to search
    list_filter = ('is_active', 'is_staff')  # Filters for the list view

# Register the model with the admin site
admin.site.register(CustomUser, CustomUserAdmin)