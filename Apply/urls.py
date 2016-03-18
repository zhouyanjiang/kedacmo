from django.conf.urls import patterns, include, url

urlpatterns = patterns('Apply.views',
    url(r'^apply/git/$', 'applygit.ApplyGit', name='applygiturl'),
)
