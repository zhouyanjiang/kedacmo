from django.conf.urls import patterns, include, url

urlpatterns = patterns('Jenkins.views',
    url(r'^jenkins/choosejob/$', 'chooseipview.ChooseJob', name='choosejoburl'),
)
