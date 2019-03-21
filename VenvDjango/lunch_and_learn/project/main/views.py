from django.shortcuts import render
from main.models import User
from main.serializer import UserSerializer
from rest_framework import generics

# Create your views here.
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer