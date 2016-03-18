from django.conf.urls import patterns, include, url

from django.conf import settings
from website.views import Home,About

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'website.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$',Home),
    url(r'^about/$',About),

    url(r'^accounts/',include('UserManage.urls' )),
    url(r'^server/',include('ServerManage.urls' )),
    url(r'^dept/',include('DeptManage.urls' )),
    url(r'^logs/',include('Logs.urls' )),
    url(r'^apply/',include('Apply.urls' )),
    url(r'^apply/apply/ajax_dict/','Apply.views.applygit.ajax_dict',name='ajax-dict'),
    #static
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT,}),

)
