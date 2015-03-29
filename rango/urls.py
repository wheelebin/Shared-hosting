from django.conf.urls import patterns, include, url
from django.contrib import admin
from rango import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^about/', views.about, name='about'),
    url(r'^$', views.index, name='index'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^add_domain/$', views.add_domain, name='add_domain'),
    url(r'^manage/$', views.manage_domain, name='manage_domain'),
    url(r'^reset_ftp_password/$', views.reset_ftp_password, name='reset_ftp_password'),
    url(r'^category/(?P<category_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^category/(?P<category_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
)
