from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'customer.views.home', name='home'),
    # url(r'^customer/', include('customer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),

    #Services
    url(r'^login/$','services.views.login_services'),
    url(r'^logout/$','services.views.logout_services'),
    url(r'^user/$','services.views.user_page'),
    url(r'^check/$','services.views.check_user_services'),
    url(r'^new_user/$','services.views.create_user_services'),
    url(r'^$','services.views.home'),
    url(r'^user_list/$','services.views.user_list'),

    #message
    url(r'^send_message/$','message.views.send_message'),

    #fs
    url(r'^ls/$','fs.views.ls'),
    url(r'^mkdir/$','fs.views.mkdir'),
    url(r'^rmdir/$','fs.views.rmdir'),
    url(r'^upload/$','fs.views.load_image'),
    url(r'^load/$','fs.views.send_file')
)
