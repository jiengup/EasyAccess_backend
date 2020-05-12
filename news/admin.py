from django.contrib import admin
from .models import NewCategory, News, Banner, Comment
# Register your models here.
admin.site.register(NewCategory)
admin.site.register(News)
admin.site.register(Banner)
admin.site.register(Comment)