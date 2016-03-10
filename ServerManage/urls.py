from django.conf.urls import patterns, include, url

urlpatterns = patterns('ServerManage.views',
    url(r'^server/add/$', 'server.AddServer', name='addserverurl'),
    url(r'^server/list/$', 'server.ListServer', name='listserverurl'),
    url(r'^server/edit/(?P<ID>\d+)/$', 'server.EditServer', name='editserverurl'),
    url(r'^server/delete/(?P<ID>\d+)/$', 'server.DeleteServer', name='deleteserverurl'),
    url(r'^server/search/$', 'server.SearchServer', name='searchserverurl'),
)
