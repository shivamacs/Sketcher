from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, 'Draft'), (1, 'Publish'))

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    updated_on = models.DateTimeField(auto_now=False, null=True)
    created_on = models.DateTimeField(auto_now_add=False, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images', blank=True)
    status = models.IntegerField(choices=STATUS, default=-1)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username