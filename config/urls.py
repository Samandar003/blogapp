from django.contrib import admin
from django.urls import path, include
from user.views import profile
from django.conf import settings
from django.conf.urls.static import static
from blog.views import CustomLoginView, register, about, PostListView
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetConfirmView
from blog.views import (
    PostDetailView, 
    PostCreateView, 
    PostUpdateView, 
    PostDelete,
    UserPostListView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PostListView.as_view(), name='home'),
    path('about/', about, name='about'),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', profile, name='profile'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post-delete'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('password-reset/', PasswordResetView.as_view(
        template_name='blog/password_reset.html'),
         name='password_reset'),
    path('password-reset/done', PasswordResetView.as_view(
        template_name='blog/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(
        template_name='blog/password_reset_confirm.html'),
         name='password_reset_confirm'),
    
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


