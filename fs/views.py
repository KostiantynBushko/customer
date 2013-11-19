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
    FILES_STORE_PATH = '/Users/kbushko/Desktop/'
ROOT_FOLDER = 'store'


#os.path.abspath(os.path.dirname(__file__))

class FileModel(models.Model):
    path = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    is_dir = models.BooleanField()
    size = models.BigIntegerField(default=0)

def make_path(path):
    if os.name == 'nt':
        path=path.replace('/','\\').replace('\\\\','\\')
    else:
        path=path.replace('\\','/').replace('//','/')
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
    path=make_path(path)
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
        m_path=os.path.realpath(file).replace(relativePath,'').replace('\\', '/').replace(file,"",1)
        m_path=m_path+'/'
        m_path.replace('//','/')
        print 'm_path = ' + m_path
        f = FileModel(path=m_path, name=file, is_dir=os.path.isdir(file))
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

    path=make_path(path)
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
    fullPath=make_path(fullPath)
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

    path = FILES_STORE_PATH + '/' + ROOT_FOLDER + '/' + username + '/MEDIA/'
    path=make_path(path)
    filename = path +  'image.png'
    print filename
    if not os.path.exists(filename):
        print 'No such file or directory'
        return HttpResponse('No such file or directorty')

    wraper = FileWrapper(file(filename))
    response = HttpResponse(wraper, content_type='*/*')
    response['Content-Length'] = os.path.getsize(filename)
    return response


def get_file(request):
    if not request.user.is_authenticated:
        return HttpResponse('User is not authentication')
    if 'file' in request.GET:
        file_path = request.GET['file']
    else:
        return HttpResponse('No such file or directory')

    path = FILES_STORE_PATH + '/' + ROOT_FOLDER + '/' + request.user.username + '/' + file_path
    path=make_path(path)
    print 'file path = ' + path
    if not os.path.exists(path):
        print 'No such file or directory'
        return HttpResponse('No such file or directory')

    print os.path.getsize(path)
    wraper = FileWrapper(file(path))
    responce=HttpResponse(wraper,content_type='application/octet-stream ')
    responce['Content-Length']=os.path.getsize(path)
    return responce


def handle_uploaded_file(path,file):
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
