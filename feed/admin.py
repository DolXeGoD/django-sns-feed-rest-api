from django.contrib import admin
from .models import Feed, Comment, Like

# Register your models here.
admin.site.register(Feed)
admin.site.register(Comment)
admin.site.register(Like)
