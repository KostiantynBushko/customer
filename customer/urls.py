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
    url(r'^set_gcm_id/$','services.views.set_gcm_reg_id'),


    #message
    url(r'^send_message/$','message.views.send_message'),
    url(r'^msg_list/$','message.views.message_list'),

    #fs
    url(r'^ls/$','fs.views.ls'),
    url(r'^mkdir/$','fs.views.mkdir'),
    url(r'^rmdir/$','fs.views.rmdir'),
    url(r'^upload/$','fs.views.load_image'),
    url(r'^load/$','fs.views.send_file'),
    url(r'^get_file/$','fs.views.get_file'),

    #App Store
    url(r'^add_app/$','appstore.views.new_app'),
    url(r'^app_list/$','appstore.views.app_list'),
    url(r'^app_image/$','appstore.views.app_image'),
    url(r'^get_app/$','appstore.views.get_app'),
    url(r'^upload_data/$','appstore.views.upload_data'),
    url(r'^user_app_list$','appstore.views.app_list_by_user'),
    url(r'^res_files$','appstore.views.get_res_files_list'),
    #rating
    url(r'^get_app_rating/$','appstore.views.get_app_rating'),
    url(r'^rate_app$','appstore.views.set_app_rating'),

)
