from django.shortcuts import render, redirect
from main.models import *
from main.serializer import UserSerializer
from rest_framework import generics
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .forms import NewUserForm
from datetime import datetime
import pytz
from googleapiclient.discovery import build
from google.oauth2 import service_account


with open('main/apikey.txt') as f:
    api_key = f.read().strip()

credentials = service_account.Credentials.from_service_account_file('main/lunchnlearn-b8be1031553e.json')
credentials = credentials.with_scopes(
    ['https://www.googleapis.com/auth/calendar.events']
)
service = build(
    'calendar', 'v3',
    developerKey = api_key,
    # http=http,
    credentials=credentials,
    discoveryServiceUrl = 'https://www.googleapis.com/discovery/v1/apis/{api}/{apiVersion}/rest'
    )

print('successful api build')


def homepage(request):

    user_email = request.COOKIES.get('signed_in')
    
    auth = False
    events = None
    if user_email:
        auth = True
        
        user = User.objects.filter(username=user_email)
        if not user:
            first_name = request.COOKIES.get('first_name')
            last_name = request.COOKIES.get('last_name')
            print(request.COOKIES)
            User(username=user_email, first_name=first_name, last_name=last_name).save()
            print('created new user!')
            response =redirect("main:edit_profile")
            response.delete_cookie('first_name')
            response.delete_cookie('last_name')
            return response
        user = user[0]
        events = [i.event_id for i in user.event_attendees_set.all() if i.event_id.start_date_time > datetime.now(pytz.utc)]
        events = [{
            'Start Date Time':e.start_date_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("America/Toronto")).strftime("%Y-%m-%d %I:%M %p"),
            'End Date Time': e.end_date_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("America/Toronto")).strftime("%Y-%m-%d %I:%M %p"),
            'Skill': e.skill_id,
            'Teacher': f"{e.teacher.first_name} {e.teacher.last_name}",
            'Organizer': f"{e.organizer.first_name} {e.organizer.last_name}",
            } for e in events]
        print(events, user)
    return render(request=request,
                  template_name='main/categories.html',
                  context={"data":events, "user":{"is_authenticated":auth}})


def create_event(request):

    
    people = {user.username : f"{user.first_name} {user.last_name}" for user in User.objects.all()}
    
    return render(request=request,
                  template_name="main/create_event.html",
                  context={"data":people})

def edit_profile(request):
    all_skills = {i.pk for i in Skill.objects.all()}
    user = request.COOKIES.get('signed_in')
    user = User.objects.filter(username=user)[0]
    known_skills = {i.skill_name_id : i.skill_level for i in user.user_skill_set.filter(skill_level__gt=0)}
    wants_skills = {i.skill_name_id : i.skill_level for i in user.user_skill_set.filter(wants=True)}
    
    if request.method == "GET":
        name = user.first_name + " " + user.last_name
        return render(request=request,
                    template_name="main/edit_profile.html",
                    context={"new_skills_want": all_skills - set(wants_skills),
                    "new_skills_know":all_skills-set(known_skills) ,
                    "skills_want": wants_skills,
                    "skills_know": known_skills,
                    "name": name})
    
    if request.method == 'POST':
        items = request.POST
        # print(items)
        new_skills = {}
        for skill in all_skills:
            wants = items.get(skill + "_want"), items.get(skill + "_want_val")
            knows = items.get(skill + "_know"), items.get(skill + "_know_val")
            # print(wants, knows)
            if wants[0] and wants[1]:
                new_skills[skill] = {"wants":True, "skill_level": max(int(wants[1]), int(knows[1]) if knows[0] else 0)}
                continue
            if knows[0] and knows[1] and int(knows[1][0]) > 0:
                new_skills[skill] = {"wants": False, "skill_level": int(knows[1])}
        
        # print(new_skills)
        for new_skill in new_skills:
            if new_skill in known_skills or new_skill in wants_skills:
                skill = user.user_skill_set.filter(skill_name_id =new_skill)[0]
                skill.wants = new_skills[new_skill]["wants"]
                skill.skill_level = new_skills[new_skill]["skill_level"]
                skill.save()
            else:
                
                skill = User_Skill(
                    username=user, 
                    skill_name=Skill.objects.filter(pk=new_skill)[0],
                    wants=new_skills[new_skill]["wants"],
                    skill_level=new_skills[new_skill]["skill_level"])
                skill.save()

        return redirect("main:edit_profile")

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
        else:
            return redirect("main:create_event")

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
 

def choose_time(request):
    attendees = set(
        map(
            lambda s: s.strip(), 
            request.COOKIES.get('attendees').strip('\"[]').replace("'", "").split(',')
                ))
    
    if request.method == 'POST':

        teacher = request.POST.get('teacher')
        response = render(request=request,
            template_name="main/select_time.html",
            context={"emails":attendees, "completeness": True})
        response.set_cookie('teacher',teacher)
        if not teacher:
            response = render(request=request,
                template_name="main/select_time.html",
                context={"emails":attendees, "completeness": False})
        return response



def submit(request):
    if request.method == 'POST':
        items = request.POST
        attendees = set(
            map(
                lambda s: s.strip(), 
                request.COOKIES.get('attendees').strip('\"[]').replace("'", "").split(',')
                    ))
        teacher = User.objects.filter(pk=request.COOKIES.get('teacher'))[0]
        skill = Skill.objects.filter(pk=request.COOKIES.get('skill'))[0]
        organizer = User.objects.filter(pk=request.COOKIES.get('signed_in'))[0]
        
        print(teacher, skill)
        print(items)
        time_offset = ":00-0400"
        start_dt,end_dt = items.get('start_date_time') + time_offset,items.get('end_date_time') + time_offset


        if start_dt > end_dt or not start_dt or not end_dt:
            return redirect("main:choose_time")
        print(start_dt, end_dt)
        e = Event(skill=skill,teacher=teacher,organizer=organizer,
        start_date_time=datetime.strptime(start_dt, "%Y-%m-%dT%H:%M:%S%z"),
        end_date_time=datetime.strptime(end_dt, "%Y-%m-%dT%H:%M:%S%z"))
        e.clean_fields()
        print(e.__dict__)
        e.save()
        for a in attendees:
            attendee = User.objects.filter(username=a)[0]
            Event_Attendees(username=attendee, event_id=e).save()
        
        google_calendar_event = {
            'summary': f'lunch and learn about {skill.skill_name}',
            'start': {"dateTime": start_dt, "timeZone" : "America/Toronto"},
            'end': {"dateTime": end_dt, "timeZone" : "America/Toronto"},
            'description': f'Come out and learn all about {skill.skill_name}!! Lead by {teacher.first_name} {teacher.last_name}',
            'organizer': {
                "email": organizer.username,
                "displayName": f"{organizer.first_name} {organizer.last_name}"
            },
            "attendees": [
                {"email": attendee}
                for attendee in attendees
            ]
        }

        event = service.events().insert(calendarId='primary',sendNotifications=True, body=google_calendar_event).execute()
        print("Event: ", event.get('htmlLink'), 'more:\n', event)


    response = redirect("main:homepage")
    response.delete_cookie('teacher')
    response.delete_cookie('skill')
    response.delete_cookie('attendees')
    return response
