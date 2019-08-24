from django.shortcuts import render, redirect, HttpResponseRedirect
from django.conf import settings
from django.views import generic
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Post, Comment
from django.contrib import messages
from .forms import RegistrationForm, BlogPostForm, EditPostForm, CommentsForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

class UserRedirectView(generic.RedirectView):
    url = reverse_lazy('sketcher:home')

class RecentsView(generic.ListView):
    template_name = 'sketcher/home.html'
    context_object_name = 'latest_posts_list'

    def get_queryset(self):
        return Post.objects.filter(status=1).order_by('-created_on')[:5]

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            messages.success(request, f'Account created for {username}!')
            form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('sketcher:home')     
    else:
        form = RegistrationForm()
    return render(request, 'sketcher/registration/signup.html', {'form': form})

class PostView(generic.FormView):
    template_name = 'sketcher/post.html'

    def get(self, request, username):
        blog = BlogPostForm()
        return render(request, self.template_name, {'blog': blog, 'user':request.user })

    def post(self, request, username):
        blog = BlogPostForm(request.POST, request.FILES)
        if request.method == 'POST':
            if blog.is_valid():
                post = blog.save(commit=False)
                post.author = request.user
                post.slug = blog.cleaned_data.get('title').lower().split(" ")
                post.slug = ('-').join(post.slug)
                post.title = blog.cleaned_data.get('title')
                post.content = blog.cleaned_data.get('content')
                if post.status == -1 and request.POST.get('draft') == 'draft':
                    post.status = 0
                if request.POST.get('publish') == 'publish':
                    post.status = 1
                    post.created_on = timezone.now()
                    post.updated_on = post.created_on
                post.save()
                return redirect(f'/{request.user.username}/{post.slug}')
        
        args = {'blog': blog, 'title': post.title, 'content': post.content, 'slug': post.slug, 'user': request.user}
        return render(request, self.template_name, args)

def edit_post(request, username, pk):
    post = get_object_or_404(Post, pk=pk)
    edit = BlogPostForm(request.POST, request.FILES, instance=post)
    if request.method == "POST":
        if edit.is_valid():
            if post.status == 0:
                if request.POST.get('draft') == 'draft':
                    post.status = 0
                else:
                    post.status = 1
                    post.created_on = timezone.now()
            elif post.status == 1 and request.POST.get('update') == 'update':
                post.updated_on = timezone.now()
            edit.save()
            return redirect(f'/{request.user.username}/{post.slug}')
    else:
        edit = BlogPostForm(instance=post)
    return render(request, 'sketcher/post.html', {'blog': edit, 'post': post})

def display(request, username, pk):
    post = get_object_or_404(Post, pk=pk)
    commentData = CommentsForm(request.POST)
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        if commentData.is_valid():
            comment = commentData.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            commentsData = CommentsForm()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if request.user.is_authenticated:
                posts_list = Post.objects.filter(author=request.user).order_by('-created_on')
                return render(request, 'sketcher/display.html', {'post':post, 'posts_list':posts_list, 'global_posts': Post.objects.filter(status=1).order_by('-created_on')[:5], 'commentData':commentData, 'comments':comments})
            else:
                return render(request, 'sketcher/display.html', {'post':post, 'global_posts': Post.objects.filter(status=1).order_by('-created_on')[:5]})
    
    else:
        if request.user.is_authenticated:
                posts_list = Post.objects.filter(author=request.user).order_by('-created_on')
                return render(request, 'sketcher/display.html', {'post':post, 'posts_list':posts_list, 'global_posts': Post.objects.filter(status=1).order_by('-created_on')[:5], 'commentData':commentData, 'comments':comments})
        else:
            commentsData = CommentsForm()
            return render(request, 'sketcher/display.html', {'post':post, 'global_posts': Post.objects.filter(status=1).order_by('-created_on')[:5], 'commentData':commentData, 'comments':comments})

class UserPostView(generic.DetailView):
    model = Post
    template_name = 'sketcher/userposts.html'
    context_object_name = 'posts_list'
   
    def get_object(self):
        return Post.objects.filter(author = self.request.user).order_by('-created_on')

class DeletePostView(generic.DeleteView):
    model = Post
    template_name = 'sketcher/deletepost.html'
    context_object_name = 'post'

    def get_post(self, pk, request):
        return self.model.objects.get(pk=pk)
    
    def get_success_url(self):
        return reverse_lazy('sketcher:posts', kwargs={'username':self.request.user.username})

@csrf_exempt
def commentDelete (request, username, pk, id):
    post = get_object_or_404(Post,pk=pk)
    comment = Comment.objects.get(id=id)
    if request.method == 'DELETE':
        comment.delete()
    return render(request, 'sketcher/deletecomment.html')