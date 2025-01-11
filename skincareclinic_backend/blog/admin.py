from django.contrib import admin
from .models import BlogPost, BlogCategory

# Register your models here.
admin.site.register(BlogCategory)
admin.site.register(BlogPost)
