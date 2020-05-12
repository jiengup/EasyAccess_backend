from django.contrib import admin
from .models import Major, Grade, User
# Register your models here.

admin.site.register(Major)
admin.site.register(Grade)
admin.site.register(User)