from django.conf.urls import patterns, include, url

urlpatterns = patterns('DeptManage.views',
    url(r'^dept/add/$', 'dept.AddDept', name='adddepturl'),
    url(r'^dept/list/$', 'dept.ListDept', name='listdepturl'),
    url(r'^dept/edit/(?P<ID>\d+)/$', 'dept.EditDept', name='editdepturl'),
    url(r'^dept/delete/(?P<ID>\d+)/$', 'dept.DeleteDept', name='deletedepturl'),
    url(r'^dept/search/$', 'dept.SearchDept', name='searchdepturl'),
)
