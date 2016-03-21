from django.conf.urls import patterns, include, url

urlpatterns = patterns('Apply.views',
    url(r'^apply/git/$', 'applygit.ApplyGit', name='applygiturl'),
    url(r'^apply/list/$','applygit.ListMyApply', name='listmyapplyurl'),
    url(r'^apply/todo/$','applygit.ListToDo', name='listtodourl'),
)
