from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import Post
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required


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

@login_required
def profile(request):
  return render(request, 'blog/profile.html')

