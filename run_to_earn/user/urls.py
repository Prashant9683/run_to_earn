from django.contrib import admin
from django.urls import path, include
from user.views import UserViewSet
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('user', UserViewSet)

urlpatterns = [
    path('',include(routers.urls)),
    path('api-auth/', include('rest_framework.urls')),
]