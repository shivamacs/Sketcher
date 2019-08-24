from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import RedirectView
from . import views
from .models import Post
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse

app_name = 'sketcher'
urlpatterns = [
    path('', views.RecentsView.as_view(), name='home'),
    path('signup/', views.register, name='signup'),
    path('signin/', LoginView.as_view(template_name='sketcher/registration/signin.html'), name='signin'),
    path('signout/', LogoutView.as_view(next_page="/"), name='signout'),
    path('<username>/newpost/', views.PostView.as_view(), name='newpost'),
    path('<username>/<str:pk>/edit', views.edit_post, name="edit"),
    path('<username>/posts/', views.UserPostView.as_view(), name='posts'),
    path('<username>/<str:pk>/', views.display, name='blog'),
    path('<username>/<str:pk>/delete', views.DeletePostView.as_view(), name="delete"),
    path('<username>/<str:pk>/comments/<int:id>/delete', views.commentDelete, name="remove"),
    path('<username>/', views.UserRedirectView.as_view())
]  

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)