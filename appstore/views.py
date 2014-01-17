__author__ = 'kbushko'

from django.core import serializers
from django.http import HttpResponse, HttpRequest
from appstore.models import AppStore
import os
from django.db import models
from django.core.servers.basehttp import FileWrapper
from customer.settings import FILES_STORE_PATH
from django.core.exceptions import ObjectDoesNotExist

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
        size=(long)(request.POST['sizeByte'])
    else:
        return HttpResponse('Method not supported')

    app = AppStore.objects.filter(name=name)
    if app:
        return HttpResponse(serializers.serialize('json',[Error(message='Application already exist')]),mimetype='application/json')

    app=AppStore(name=name,description=description,path=path(packageName),user=request.user.username)
    app.versionCode=versionCode
    app.versionName=versionName
    app.packageName=packageName
    app.description=description
    app.url=url
    app.size=size
    app.save()

    ob=[]
    ob.append(app)
    ser=serializers.serialize('json',ob)
    print ser
    return HttpResponse(ser, mimetype='application/json')
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
    ser = serializers.serialize('json',AppStore.objects.all()[offset:offset+count])
    return HttpResponse(ser, mimetype='application/json')

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
    responce=HttpResponse(wraper,content_type='application/octet-stream')
    responce['Content-Length']=os.path.getsize(file_path)
    return responce

########################################################################################################################
# Returl list of application by the user
def app_list_by_user(request):
    print 'method [ app_list_by_user ]'
    if not request.user.is_authenticated:
        return HttpResponse('User is not authenticated')

    offset = int(request.GET['offset'])
    count = int(request.GET['limit'])

    app=AppStore.objects.filter(user=request.user.username)[offset:offset+count]
    print serializers.serialize('json',app)
    return HttpResponse(serializers.serialize('json',app))

########################################################################################################################
# Return list of files in resources folder of application
def get_res_files_list(request):
    if request.method == 'POST':
        appName = request.POST['name']
    elif request.method == 'GET':
        appName = request.GET['name']
    else:
        return HttpResponse(serializers.serialize('json',[Error(message='method not supported')]),mimetype='application/json')
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
# Rate the app
def set_app_rating(request):
    if not request.user.is_authenticated:
        return HttpResponse(serializers.serialize('json',[Error(message="User is not authentication")]),mimetype='application/json')

    if request.method == 'POST':
        name=request.POST['name']
        rating=(int)(request.POST['rating'])
    elif request.method == 'GET':
        name=request.GET['name']
        rating=(int)(request.GET['rating'])
    else:
        return HttpResponse(serializers.serialize('json',[Error(message="Method not supported")]),mimetype='application/json')
    try:
        app=AppStore.objects.get(name=name)
    except ObjectDoesNotExist:
        return

    if rating == 1:
        app.one_stars += 1;
    elif rating == 2:
        app.two_stars += 1;
    elif rating == 3:
        app.three_stars += 1;
    elif rating == 4:
        app.four_stars += 1;
    elif rating == 5:
        app.five_stars += 1;
    total_count = app.five_stars + app.four_stars + app.three_stars + app.two_stars + app.one_stars;
    total_rate = (app.five_stars * 5) + (app.four_stars * 4) + (app.three_stars * 3) + (app.two_stars * 2) + app.one_stars;
    app.total_rating = (int)(total_rate / total_count)
    app.save()
    print [app]
    return HttpResponse(serializers.serialize('json',[app]),mimetype='application/json')
########################################################################################################################
# Get appliaction rating
def get_app_rating(request):
    if not request.user.is_authenticated:
        return HttpResponse(serializers.serialize('json',[Error(message='User is not authenticated')]),mimetype='application/json')
    if request.method == 'POST':
        appId=(int)(request.POST['appId'])
    elif request.method == 'GET':
        appId=(int)(request.GET['appId'])
    else:
        return HttpResponse(serializers.serialize('json',[Error(message='Method not supported')]),mimetype='application/json')
    try:
        app=AppStore.objects.get(pk=appId)
    except ObjectDoesNotExist:
        return HttpResponse(serializers.serialize('json',[Error(message='Object does not exist')]),mimetype='application/json')

    rating = (int)((app.five_stars * 5) + (app.four_stars * 4) + (app.three_stars * 3) + (app.two_stars * 2) + app.one_stars)
    print rating
    class Rating(models.Model):
        rating=models.IntegerField(default=0)

    return HttpResponse(serializers.serialize('json',[Rating(rating=rating)]),mimetype='application/json')

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