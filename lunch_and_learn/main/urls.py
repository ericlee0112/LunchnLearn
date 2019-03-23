from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('api/user/', views.UserList.as_view()),
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name="register"),
    path("logout", views.logout_request, name="logout"),
    path("login", views.login_request, name="login"),
    path("create_event", views.create_event, name="create_event"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("choose_skill", views.choose_skill, name="choose_skill"),
    path("choose_lead", views.choose_lead, name="choose_lead"),
    path("choose_food", views.choose_food, name="choose_food")
]