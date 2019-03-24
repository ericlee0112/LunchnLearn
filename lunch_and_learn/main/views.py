from django.shortcuts import render, redirect
from main.models import *
from main.serializer import UserSerializer
from rest_framework import generics
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm

# Create your views here.

'''
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
'''

class UserList(generics.ListAPIView):
    serializer_class = UserSerializer

def homepage(request):
    return render(request=request,
                  template_name='main/categories.html',
                  context={"categories": User.objects.all})

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("main:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")

def create_event(request):
    #get some data
    
    people = [f"{user.first_name} {user.last_name}" for user in User.objects.all()]
    return render(request=request,
                  template_name="main/create_event.html",
                  context={"data":people})

def edit_profile(request):
    return render(request=request,
                  template_name="main/edit_profile.html")

def choose_skill(request):
    
    if request.method == 'POST':
        print(request.POST)
        skills = [skill.skill_name for skill in Skill.objects.all()]
        return render(request=request,
                    template_name="main/choose_skill.html",
                    context={"data":skills})

def choose_lead(request):
    available_people = ['Anant', 'Brian', 'Osama']
    return render(request=request,
                  template_name="main/choose_lead.html",
                  context={"data":available_people})

def choose_food(request):
    food = ['sandwiches', 'pasta', 'soup']
    return render(request=request,
                  template_name="main/choose_food.html",
                  context={"data":food}) 