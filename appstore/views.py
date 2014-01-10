__author__ = 'kbushko'

from django.core import serializers
from django.http import HttpResponse, HttpRequest
from appstore.models import AppStore
import os
from django.db import models
from django.core.servers.basehttp import FileWrapper
from customer.settings import FILES_STORE_PATH

APP_FOLDER = 'store/appstore'

def make_path(path):
    if os.name == 'nt':
        path=path.replace('/','\\').replace('\\\\','\\')
    else:
        path=path.replace('\\','/').replace('//','/')
    return path


class Error(models.Model):
    message=models.CharField(max_length=256)

########################################################################################################################
# create new repository
def new_app(request):
    if request.method == 'POST':
        name=request.POST['appName']
        description=request.POST['description']
        url=request.POST['url']
        packageName=request.POST['packageName']
        versionName=request.POST['versionName']
        versionCode=request.POST['versionCode']
    else:
        return HttpResponse('Method not supported')

    app = AppStore.objects.filter(name=name)
    if app:
        return HttpResponse('Application alredi exist')

    app=AppStore(name=name,description=description,path=path(packageName),user=request.user.username)
    app.versionCode=versionCode
    app.versionName=versionName
    app.packageName=packageName
    app.description=description
    app.url=url
    app.save()

    ob=[]
    ob.append(app)
    ser=serializers.serialize('json',ob)
    print ser
    return HttpResponse(ser, mimetype='application/data')
########################################################################################################################
def upload_data(request):
    print 'method [ Upload data ]'
    if request.method != 'POST':
        return HttpResponse('Only POST method is available')
    elif not request.user.is_authenticated():
        return HttpResponse('User is not authenticated')

    file = request.FILES['file_name']
    path = request.POST['file_path']

    print request.FILES['file_name'].name
    print path

    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except IOError, e:
            return HttpResponse(e.strerror)
    fullPath = os.path.join(path,request.FILES['file_name'].name)
    print fullPath
    handle_uploaded_file(path=fullPath, file=file)
    return HttpResponse('success')

########################################################################################################################
# return application list in the database
def app_list(request):
    offset = int(request.GET['offset'])
    count = int(request.GET['limit'])
    #ser = serializers.serialize('json',AppStore.objects.all()[offset:offset+count], fields=('name', 'path', 'description','packageName'))
    ser = serializers.serialize('json',AppStore.objects.all()[offset:offset+count])
    return HttpResponse(ser, mimetype='application/data')

########################################################################################################################
# return application image from app folder
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
# return apk file
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
    responce['Content-Length']=os.path.getsize(file_path)
    return responce

########################################################################################################################
# Returl list of application by the user
def app_list_by_user(request):
    print 'method [ app_list_by_user ]'
    if not request.user.is_authenticated:
        return HttpResponse('User is not authenticated')
    app=AppStore.objects.filter(user=request.user.username)
    return HttpResponse(serializers.serialize('json',app))

########################################################################################################################
# Return list of files in resutce folder of application
def get_res_files_list(request):
    if request.method == 'POST':
        appName = request.POST['name']
    elif request.method == 'GET':
        appName = request.GET['name']
    else:
        error=Error(message='method not supported')
        return HttpResponse(serializers.serialize('json',error))
    d=[]
    try:
        app=AppStore.objects.get(name=appName)
        d.append(app)
    except AppStore.DoesNotExist:
        error=Error(message='Application does not exist')
        d.append(error)

    print serializers.serialize('json',d)
    return HttpResponse(serializers.serialize('json',d))

########################################################################################################################
#
def handle_uploaded_file(path,file):
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

########################################################################################################################
#
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
########################################################################################################################
#