from django.conf.urls import patterns, url, include
from django.contrib import admin

import views

urlpatterns = patterns('',
                       url(r'^dashboard/$', views.DashboardView.as_view()),
                       url(r'^run_test/(?P<id>\d+)$', views.run_test),
                       url(r'^email/(?P<id>\d+)$', views.send_email),
                       url(r'^report/$', views.test_report),
                       url(r'^about/$', views.about),
                       url(r'^detail/(?P<id>\d+)$', views.site_detail),
                       url(r'^edit_user/$', views.edit_user),
                       url(r'^create_edit_site/$', views.CreateEditSiteView.as_view()),
                       url(r'^$', views.LoginRegisterUserView.as_view()),
                       url(r'^password-change/$',
                           'django.contrib.auth.views.password_change',
                           name='password_change'),
                       url(r'^password-change/done/$',
                           'django.contrib.auth.views.password_change_done',
                           name='password_change_done'),
                       url(r'^admin/', include(admin.site.urls)),

                       )
