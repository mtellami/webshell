from django.urls import path
from server.views import root

urlpatterns = [
    path('', root, name='root')
]
