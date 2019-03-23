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
    path("edit_profile", views.edit_profile, name="edit_profile")
]