from django.conf.urls import patterns, include, url

urlpatterns = patterns('paloma.views',
    url(r'^enroll/(?P<command>.+)/(?P<secret>.+)', 'enroll',name="paloma_enroll",),
)
