from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(UserForm)
admin.site.register(Wallet)
admin.site.register(Transaction)
