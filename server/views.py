from django.http import JsonResponse, HttpResponseBadRequest
from json import loads
from .consumers import SSH
from os import getenv
from jwt import encode

def login(request):
    if request.method != 'POST':
        return HttpResponseBadRequest(f'Can\'t {request.method} /ws/login')

    try:
        body = loads(request.body)
        username = body.get('username')
        password = body.get('password')
        if not username or not password:
            raise Exception('invalid payload')
        session = SSH(username, password)
        session.close()
        token = encode(body, getenv('JWT_SECRET_KEY'), algorithm='HS256')
        return JsonResponse({'session_token': token})
    except:
        return JsonResponse({'error': 'invalid session credentials'})
