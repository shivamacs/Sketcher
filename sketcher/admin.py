from django.contrib import admin
from sketcher.models import Post, Comment
from django.utils import timezone

admin.site.register(Post)
admin.site.register(Comment)