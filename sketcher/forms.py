from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import models
from .models import Post, Comment

class RegistrationForm(UserCreationForm):
    email = models.EmailField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

        def save(self, commit=True):
            user = super(RegistrationForm, self).save(commit=False)
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']

            if commit:
                user.save()

            return user

class BlogPostForm(forms.ModelForm):
    title = forms.CharField(max_length=200, required=False)
    content = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 40%;'}), required=False)
    
    class Meta:
        model = Post
        fields = ('title', 'content', 'image')
        
class EditPostForm(UserChangeForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'image')

class CommentsForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body',)  