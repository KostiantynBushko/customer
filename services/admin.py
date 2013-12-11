__author__ = 'kbushko'

from django.contrib import admin
from services.models import gcm_user_id

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('username', 'gcm_id')


admin.site.register(gcm_user_id,ServiceAdmin)