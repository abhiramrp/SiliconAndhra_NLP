from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.db import IntegrityError

from .models import *
from .forms import *

def index(request):
  if request.user.is_authenticated:
    return render(request, "app/index.html", {"context": "Logged in"})
  
  return render(request, "app/index.html", {"context": "Home page"})

def register_view(request):
  if request.method == 'POST':
    email = request.POST['email']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    if password != confirm_password:
      messages.error(request, "Passwords must match")
      return redirect('register')
    
    if User.objects.filter(email=email).exists():
      messages.error(request, "Email already exists")
      return render(request, 'app/register.html')

    user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, role="Participant")
    user.save()
    login(request, user)
    return redirect('index')

  return render(request, 'app/register.html')

def login_view(request):
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']
    
    user = authenticate(request, email=email, password=password)
    
    if user is not None:
      login(request, user)
      return redirect('index')
    
    else:
      messages.error(request, "Invalid email or password.")
      
  return render(request, 'app/login.html')

@login_required
def logout_view(request):
  logout(request)
  return redirect('login')



def upload_document(request):
  user = User.objects.get(email=request.user.email)
  if request.method == 'POST':
    form = DocumentForm(request.POST, request.FILES)
    if form.is_valid():
      doc = form.save(commit=False)
      doc.uploader = user
      doc.save()

      return redirect('index')
  else:
    form = DocumentForm()
  
  return render(request, 'app/upload_document.html', {'form': form})

