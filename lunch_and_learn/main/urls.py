from django.urls import path
from . import views
urlpatterns = [
    path('api/user/', views.UserList.as_view())
]