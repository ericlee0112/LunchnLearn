from django.shortcuts import render, redirect
from main.models import *
from main.serializer import UserSerializer
from rest_framework import generics
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm



def homepage(request):
    #TODO: get dashboard (upcoming events)
    return render(request=request,
                  template_name='main/categories.html')

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

    
    people = {user.username : f"{user.first_name} {user.last_name}" for user in User.objects.all()}
    
    return render(request=request,
                  template_name="main/create_event.html",
                  context={"data":people})

def edit_profile(request):
    return render(request=request,
                  template_name="main/edit_profile.html")

def choose_skill(request):
    
    if request.method == 'POST':
        
        attendees = request.POST.getlist('names') if 'names' in request.POST else None
        
        all_skills = {}
        if attendees:
            all_skills = User_Skill.objects.filter(username=attendees[0], wants=True)
            for i in range(1, len(attendees)):
                all_skills = all_skills.union(User_Skill.objects.filter(username=attendees[i],wants = True))
                
            
            print('all skills: ', all_skills.values_list())
            new_skills=[]
            for skill in all_skills:
                teachers = skill.skill_name.user_skill_set.filter(skill_level__gt=0)
                print("potential: ",teachers)
                if ([t for t in teachers if t.username_id in attendees]):
                    new_skills.append(skill)

            print('teachable skills: ', [i.skill_name_id for i in new_skills])
        skills = {user_skill.skill_name_id: user_skill.skill_name.user_skill_set.count() for user_skill in new_skills}
        
        
        response = render(request=request,
                    template_name="main/choose_skill.html",
                    context={"data":skills})
        response.set_cookie('attendees', attendees)
        return response

def enter_date(request):
    return render(request=request,
                    template_name="main/enter_date.html")

def choose_lead(request):

    if request.method == 'POST':
        attendees = set(
            map(
                lambda s: s.strip(), 
                request.COOKIES.get('attendees').strip('\"[]').replace("'", "").split(',')
                    ))
        
        skill = request.POST.get('skill')
        print(attendees)
        teachers = User_Skill.objects.filter(skill_name_id=skill,skill_level__gt=0)
        print([(teacher.username_id, teacher.username_id in attendees) for teacher in teachers])
        teachers = {
            teacher.username_id :[
                f"{teacher.username.first_name} {teacher.username.last_name}", 
                teacher.skill_level]
                for teacher in teachers 
                if teacher.username_id in attendees}
        
        print(teachers)
        response = render(request=request,
                    template_name="main/choose_lead.html",
                    context={"data":teachers})
        response.set_cookie('skill', skill)
        return response


def choose_food(request):
    #TODO
    food = ['sandwiches', 'pasta', 'soup']
    return render(request=request,
                  template_name="main/choose_food.html",
                  context={"data":food}) 

def choose_time(request):

    data = {
        "email":{
            "busy": [
                {"start": "2019-03-25T12:00:00Z", "end": "2019-03-25T13:00:00Z"},
                {"start": "2019-03-26T21:00:00Z", "end": "2019-03-26T22:00:00Z"}
            ]
        }
    }

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
                "startDate":"Sun Dec 09 2012 03:00:00 GMT-0500 (Eastern Standard Time)",
                "endDate":"Sun Dec 09 2012 03:40:00 GMT-0500 (Eastern Standard Time)",
                "taskName":"Eric",
                "status":"RUNNING"
            },
            {
                "startDate":"2012-12-09T03:00:00Z",
                "endDate":"2012-12-09T03:40:00Z",
                "taskName":"Eric",
                "status":"RUNNING"
            }
           ]
    return render(request=request,
                  template_name="main/select_time.html",
                  context={"data":data})


def confirm(request):
    #TODO
    """Confirm all details including date, time, teacher, skill, attendees and food options
    """
    #response.delete_cookie(key)
    pass

def submit(request):
    #TODO
    if request.method == 'POST':
        items = request.POST
        skill,teacher,organizer,start_dt,end_dt = items.get('skill'),items.get('teacher'),items.get('organizer'),items.get('start_date_time'),items.get('end_date_time')
        
        Event(skill=skill,teacher=teacher,organizer=organizer,start_dt=start_dt,end_dt=end_dt).save()

    """Submit all information to database and redirect to home page
    """
    return redirect("main:homepage")
