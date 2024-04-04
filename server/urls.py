from django.urls import path
from server.views import login

urlpatterns = [
    path('ws/login/', login, name='login')
]
