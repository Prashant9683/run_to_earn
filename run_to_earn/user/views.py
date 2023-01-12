from django.shortcuts import render
from rest_framework import viewsets
from user.models import User, Goal
from user.serializers import UserSerializer, GoalSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer