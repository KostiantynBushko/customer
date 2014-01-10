__author__ = 'kbushko'
from django.contrib import admin
from appstore.models import AppStore

class AppStoreAdmin(admin.ModelAdmin):
    list_display = ('user','name','packageName')

admin.site.register(AppStore,AppStoreAdmin)