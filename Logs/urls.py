from django.conf.urls import patterns, include, url

urlpatterns = patterns('Logs.views',
    url(r'^logs/list/$', 'logs.ListServer', name='listlogsurl'),
    url(r'^logs/search/$', 'logs.SearchServer', name='searchlogsurl'),
)
