__author__ = 'kbushko'
from django.contrib import admin
from message.models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('username','sender','message','date')

admin.site.register(Message,MessageAdmin)