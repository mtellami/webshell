from django.urls import path
from server.views import login

urlpatterns = [
    path('login/', login, name='login')
]
