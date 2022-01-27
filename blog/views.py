from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.views.generic import (
  ListView, 
  UpdateView, 
  DeleteView, 
  DetailView,
)

def home(request):
  context = {
    'posts':Post.objects.all()
  }
  return render(request, 'blog/home.html', context)

def about(request):
  return render(request, 'blog/about.html', {'title':'About'})

class CustomLoginView(LoginView):
  template_name = 'blog/login.html'
  fields = '__all__'
  redirect_authenticated_user = True
  def get_success_url(self) -> str:
      return reverse_lazy('home')  

def register(request):
  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      messages.success(request, f'Account created for {username}')
      return redirect('home')
  else:
      form = UserRegisterForm()
  return render(request, 'blog/register.html', {'form':form})

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    def get_queryset(self):
      user = get_object_or_404(User, username=self.kwargs.get('username'))
      return Post.objects.filter(author=user).order_by('-date_posted')
      
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html' 
    

class PostCreateView(LoginRequiredMixin, CreateView):
  model = Post
  fields = ['title', 'content']
  template_name = 'blog/post_create.html'  
  def form_valid(self, form):
    form.instance.author = self.request.user
    return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  fields = ['title', 'content', 'date_posted']
  template_name = 'blog/post_update.html'
  def form_valid(self, form):
      form.instance.author = self.request.user
      return super().form_valid(form)
  def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
      
class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  template_name = 'blog/post_delete.html'
  context_object_name = 'post'
  success_url = reverse_lazy('home')
  def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
  
    