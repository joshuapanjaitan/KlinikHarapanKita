from django.contrib import admin

# Register your models here.
from .models import Antrian
from .models import Current

admin.site.register(Antrian)
admin.site.register(Current)
