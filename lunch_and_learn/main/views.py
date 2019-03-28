from django.shortcuts import render, redirect
from main.models import User
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
    people = ['Eric', 'Brian', 'Ashkan', 'Osama', 'Anant']
    return render(request=request,
                  template_name="main/create_event.html",
                  context={"data":people})

def edit_profile(request):
    return render(request=request,
                  template_name="main/edit_profile.html")

def choose_skill(request):
    skills = ['Java', 'C++', 'Kubernetes', 'Kotlin', 'Git', 'Bash']
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

def select_time(request):

    data = [
            {
                "startDate": "Sun Dec 09 01:36:45 EST 2012",
                "endDate": "Sun Dec 09 02:36:45 EST 2012",
                "taskName":"Eric",
                "status":"RUNNING"
            },
            {
                "startDate": "Sun Dec 09 04:56:32 EST 2012",
                "endDate":"Sun Dec 09 06:35:47 EST 2012",
                "taskName":"Brian",
                "status":"RUNNING"
            },
            {
                "startDate": "Sun Dec 09 01:56:32 EST 2012",
                "endDate":"Sun Dec 09 03:15:47 EST 2012",
                "taskName":"Brian",
                "status":"RUNNING"
            },
            {
                "startDate": "Sun Dec 09 06:29:53 EST 2012",
                "endDate":"Sun Dec 09 06:34:04 EST 2012",
                "taskName":"Anant",
                "status":"RUNNING"
            },
            {
                "startDate": "Sun Dec 09 05:35:21 EST 2012",
                "endDate":"Sun Dec 09 06:21:22 EST 2012",
                "taskName":"Ashkan",
                "status":"RUNNING"
            },
            {
                "startDate":"Sun Dec 09 05:00:06 EST 2012",
                "endDate":"Sun Dec 09 05:05:07 EST 2012",
                "taskName":"Anant",
                "status":"RUNNING"
            },
            {
                "startDate":"Sun Dec 09 03:46:59 EST 2012",
                "endDate":"Sun Dec 09 04:54:19 EST 2012",
                "taskName":"Ashkan",
                "status":"RUNNING"
            },
            {
                "startDate":"Sun Dec 09 04:02:45 EST 2012",
                "endDate":"Sun Dec 09 04:48:56 EST 2012",
                "taskName":"Anant",
                "status":"RUNNING"
            },
            {
                "startDate":"Sun Dec 09 03:27:35 EST 2012",
                "endDate":"Sun Dec 09 03:58:43 EST 2012",
                "taskName":"Eric",
                "status":"RUNNING"
            }
           ]
    return render(request=request,
                  template_name="main/select_time.html",
                  context={"data":data})