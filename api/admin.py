from django.contrib import admin
from .models import CustomUser, Graduate

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Graduate)
