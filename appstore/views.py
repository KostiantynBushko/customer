__author__ = 'kbushko'

import json
from django.core.serializers.json import DjangoJSONEncoder
import simplejson as json
from django.core import serializers
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from appstore.models import AppStore
import os
from fs.views import FileModel
from django.core.servers.basehttp import FileWrapper
from customer.settings import FILES_STORE_PATH

APP_FOLDER = 'store/appstore'

def make_path(path):
    if os.name == 'nt':
        path=path.replace('/','\\').replace('\\\\','\\')
    else:
        path=path.replace('\\','/').replace('//','/')
    return path


def new_app(request):
    if request.method == 'POST':
        name=request.POST['appName']
        description=request.POST['description']
        url=request.POST['url']
        packageName=request.POST['packageName']
        versionName=request.POST['versionName']
        versionCode=request.POST['versionCode']
    elif request.method == 'GET':
        name=request.GET['appName']
        description=request.GET['description']
        url=request.GET['url']
        packageName=request.GET['packageName']
        versionName=request.GET['versionName']
        versionCode=request.GET['versionCode']
    else:
        return HttpResponse('Method not supported')

    app=AppStore(name=name,description=description,path=path(name),user=request.user.username)
    app.versionCode=versionCode
    app.versionName=versionName
    app.packageName=packageName
    app.url=url
    app.save()

    ob=[]
    ob.append(app)
    ser=serializers.serialize('json',ob)
    print ser
    return HttpResponse(ser, mimetype='application/data')

########################################################################################################################
def app_list(request):
    offset = int(request.GET['offset'])
    count = int(request.GET['limit'])
    print offset
    print count
    ser = serializers.serialize('json',AppStore.objects.all()[offset:offset+count], fields=('name', 'path', 'description'))
    print ser
    return HttpResponse(ser, mimetype='application/data')

########################################################################################################################
def app_image(request):
    if not request.user.is_authenticated:
        return HttpResponse('User is not authentication')

    if 'path' in request.GET:
        path = request.GET['path']
    else:
        return HttpResponse('error');

    path=make_path(path)
    filename = path +  '/image.png'
    print filename
    if not os.path.exists(filename):
        print 'No such file or directory'
        return HttpResponse('No such file or directorty')

    wraper = FileWrapper(file(filename))
    response = HttpResponse(wraper, content_type='*/*')
    response['Content-Length'] = os.path.getsize(filename)
    return response

########################################################################################################################
def get_app(request):
    print 'method [ get_file ]'
    if not request.user.is_authenticated:
        return HttpResponse('User is not authentication')
    if 'path' in request.GET:
        file_path = request.GET['path']
    else:
        return HttpResponse('No such file or directory')

    file_path = file_path + '/' + 'app.apk'
    path=make_path(file_path)
    print 'file path = ' + file_path
    if not os.path.exists(file_path):
        print 'No such file or directory'
        return HttpResponse('No such file or directory')

    print os.path.getsize(file_path)
    wraper = FileWrapper(file(file_path))
    responce=HttpResponse(wraper,content_type='application/octet-stream ')
    responce['Content-Length']=os.path.getsize(file_path
    )
    return responce

########################################################################################################################
def handle_uploaded_file(path,file):
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

########################################################################################################################
def path(name):
    returnPath = os.path.realpath(os.curdir)

    os.chdir(FILES_STORE_PATH)
    try:
        os.chdir(APP_FOLDER)
    except:
        os.mkdir(APP_FOLDER)
        os.chdir(APP_FOLDER)

    try:
        os.chdir(name)
    except:
        os.mkdir(name)
        os.chdir(name)

    relativePath = os.path.realpath(os.curdir)
    print 'relativePath = ' + relativePath

    fullPath = relativePath
    print 'fullPath = ' + fullPath
    try:
        os.chdir(fullPath)
    except:
        os.chdir(returnPath)
        return HttpResponse('path not found')
    os.chdir(returnPath)
    return fullPath