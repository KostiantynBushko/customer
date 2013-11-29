# Create your views here.

import json
from django.core.serializers.json import DjangoJSONEncoder
import simplejson as json
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def login_services(request):
    print('Login servise runing')
    if request.method != 'POST':
        return HttpResponse('Only POST method is allowed!')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username,password=password)
    if user is not None:
        if user.is_active:
            login(request,user)
            return HttpResponse('User login success')
        else:
            return HttpResponse('Dissable account')
    else:
        return HttpResponse('Invalid login or password')

def logout_services(request):
    logout(request)
    return HttpResponse("Logout")


def check_user_services(request):
    print('Check User authentication')
    if not request.user.is_authenticated():
        print("User is not authenticated")
        return HttpResponse("Error")
    else:
        return HttpResponse('Success')


def create_user_services(request):
    if request.method != 'POST':
        return HttpResponse('Only POST method is allowed!')
    print request.POST

    user_name = request.POST['user_name']
    name = request.POST['name']
    second_name = request.POST['second_name']
    email = request.POST['email']
    password = request.POST['password']

    try:
        User.objects.get(email__iexact=email)
        return HttpResponse("Error registration")
    except:
        try:
            user = User.objects.create_user(user_name, email,password)
            user.is_active = True
            user.first_name = name
            user.last_name = second_name
            user.save()
            print('User succes created')
            return HttpResponse("User success created")
        except:
            return HttpResponse("Error registration, check username.")


def user_page(request):
    print request.COOKIES
    if not request.user.is_authenticated():
        return HttpResponse('User is not authenticated')
    else:
        data = serializers.serialize('json',[request.user], fields=('username', 'first_name','last_name','email'))
        print data
        return HttpResponse(data,mimetype='application/json')


def home(request):
    print('Home page')
    if not request.user.is_authenticated():
        return HttpResponse('User is not authenticated')
    else:
        if 'is_visited' in request.session:
            print request.session['is_visited']
        else:
            request.session['is_visited'] = 'You are visited'
        return HttpResponse('Home page hi Adam')


def user_list(request):
    offset = int(request.GET['offset'])
    count = int(request.GET['limit'])
    print offset
    print count
    ser = serializers.serialize('json',User.objects.all().order_by('username')[offset:offset+count], fields=('username', 'first_name', 'last_name','email'))
    print ser
    return HttpResponse(ser, mimetype='application/data')