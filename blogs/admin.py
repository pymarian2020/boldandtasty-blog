from django.contrib import admin

# Register your models here.
from .models import Blog, Review, Tag

admin.site.register(Blog)
admin.site.register(Review)
admin.site.register(Tag)