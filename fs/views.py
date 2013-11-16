# Create your views here.

from customer.settings import PROJECT_ROOT
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.core.files import File
import os
import shutil
from django.db import models
from django.core import serializers
import shutil
import sys
from django.core.servers.basehttp import FileWrapper

if os.name == 'nt':
    FILES_STORE_PATH = 'C:\\Users\\Saiber\\Desktop\\'
else:
    FILES_STORE_PATH = ''
ROOT_FOLDER = 'store'


#os.path.abspath(os.path.dirname(__file__))

class FileModel(models.Model):
    path = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    is_dir = models.BooleanField()
    size = models.BigIntegerField(default=0)

def create_path(path):
    if os.name == 'nt':
        path=path.replace('/','\\')
    else:
        path=path.replace('\\','/')
    return path

def ls(request):
    returnPath = os.path.realpath(os.curdir)
    if not request.user.is_authenticated():
        return HttpResponse('User is not authenticated')
    if request.method == 'POST':
        path = request.POST['path']
    elif request.method == 'GET':
        path = request.GET['path']
    else:
        os.chdir(returnPath)
        return HttpResponse('Method not supported')
    path=create_path(path)
    print 'path = ' + path

    os.chdir(FILES_STORE_PATH)
    try:
        os.chdir(ROOT_FOLDER)
    except:
        os.mkdir(ROOT_FOLDER)
        os.chdir(ROOT_FOLDER)

    try:
        os.chdir(request.user.username)
    except:
        os.mkdir(request.user.username)
        os.chdir(request.user.username)

    relativePath = os.path.realpath(os.curdir)
    print 'relativePath = ' + relativePath + path

    fullPath = relativePath + path
    print 'fullPath = ' + fullPath
    try:
        os.chdir(fullPath)
    except:
        os.chdir(returnPath)
        return HttpResponse('path not found')

    fileList = []
    dirList = []
    files = os.listdir(os.curdir)
    for file in files:
        f = FileModel(path=os.path.realpath(file).replace(relativePath,'').replace('\\', '/').replace(file,""), name=file, is_dir=os.path.isdir(file))
        if os.path.isfile(file):
            f.size = os.path.getsize(file)
            fileList.append(f)
        else:
            dirList.append(f)

    result = serializers.serialize('json', dirList + fileList)
    os.chdir(returnPath)
    return HttpResponse(result, mimetype='application/json')


def mkdir(request):
    currentPath = os.path.realpath(os.curdir)

    if not request.user.is_authenticated:
        return HttpResponse('User is not authenticated')
    if request.method == 'POST':
        path = request.POST['path']
        name = request.POST['name']
    elif request.method == 'GET':
        path = request.GET['path']
        name = request.GET['name']
    else:
        os.chdir(currentPath)
        return HttpResponse('Method not supported')

    try:
        os.chdir(FILES_STORE_PATH)
        print os.path.realpath(os.curdir)
        os.chdir(ROOT_FOLDER)
        print os.path.realpath(os.curdir)
        os.chdir(request.user.username)
        print os.path.realpath(os.curdir)
    except:
        os.chdir(currentPath)
        return HttpResponse("path not found")

    relativePath = os.path.realpath(os.curdir)
    fullPath = relativePath + path
    print 'full path = ' + fullPath
    try:
        os.chdir(fullPath)
    except:
        os.chdir(currentPath)
        return HttpResponse('path not found')

    try:
        os.mkdir(name)
    except OSError, e:
        print e.strerror
        os.chdir(currentPath)
        return HttpResponse(e.strerror)

    p = os.path.realpath(os.curdir)
    os.chdir(currentPath)
    return HttpResponse(p)


def rmdir(request):
    if request.method == 'GET':
        path = request.GET['path']
    else:
        return HttpResponse('Method not supported')
    fullPath = os.path.realpath(FILES_STORE_PATH) + '/'+ ROOT_FOLDER + '/' + request.user.username + '/'
    fullPath += path
    fullPath = fullPath.replace('//','/')
    print 'delate  = ' + fullPath

    try:
        shutil.rmtree(fullPath);
    except OSError, e:
        str = e.strerror + " : " + e.errno
        return HttpResponse(str)

    return HttpResponse(fullPath)

def load_image(request):
    print 'method [ LoadImage ]'
    if request.method != 'POST':
        return HttpResponse('Only POST method is available')
    elif not request.user.is_authenticated():
        return HttpResponse('User is not authenticated')
    print request.POST
    file = request.FILES['file']
    print request.FILES['file'].name

    path = FILES_STORE_PATH + '/' + ROOT_FOLDER + '/' + request.user.username
    if os.name =='nt':
        path = path.replace("/","\\")
    if not os.path.exists(path):
        try:
            if os.name =='nt':
                path = path.replace("/","\\")
            os.mkdir(path)
            os.mkdir(path + '/MEDIA/')
        except IOError, e:
            return HttpResponse(e.strerror)
    path = path + '/MEDIA/'
    if os.name =='nt':
        path = path.replace("/","\\")

    fullPath = os.path.join(path,request.FILES['file'].name)
    print fullPath
    handle_uploaded_file(path=fullPath, file=file)
    return HttpResponse('success')


def send_file(request):
    if not request.user.is_authenticated:
        return HttpResponse('User is not authentication')

    if 'username' in request.GET:
        username = request.GET['username']
    else:
        username = request.user.username
    print 'User name = ' + username

    path = FILES_STORE_PATH + '/' + ROOT_FOLDER + '/' + username + '/MEDIA/'
    filename = path +  'image.png'
    if os.name == 'nt':
        path = path.replace("/","\\")
    print path

    if not os.path.exists(filename):
        print 'No such file or directory'
        return HttpResponse('No such file or directorty')

    wraper = FileWrapper(file(filename))
    response = HttpResponse(wraper, content_type='*/*')
    response['Content-Length'] = os.path.getsize(filename)
    return response


def handle_uploaded_file(path,file):
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)