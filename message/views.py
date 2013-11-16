__author__ = 'kbushko'
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from message.models import Message


def send_message(request):
    if not request.user.is_authenticated():
        return HttpResponse('User is not authenticated');
    if request.method == 'POST':
        recipient = request.POST['recipient']
        message = request.POST['message']
    elif request.method == 'GET':
        recipient = request.GET['r']
        message = request.GET['m']
    else:
        return HttpResponse('Method not supported')

    print(recipient)
    print(message)


    try:
        User.objects.get(username__iexact=recipient)
        sender_username = request.user.username
        m = Message(sender=sender_username, username=recipient, message=message)
        m.save()
        return HttpResponse(sender_username)
    except:
        return HttpResponse('Recipient not found')


