from django.conf.urls import patterns, include, url

urlpatterns = patterns('paloma.views',
    url(r'^enroll/(?P<command>.+)/(?P<secret>.+)', 'enroll',name="paloma_enroll",),
    url(r'^signin', 'signin',name="paloma_signin",),
    url(r'^signup', 'signup',name="paloma_signup",),
)
