from django.conf.urls import patterns, include, url
from paloma.views import SignUpMailView,SignUpWebView

urlpatterns = patterns('paloma.views',
    url(r'^enroll/(?P<command>.+)/(?P<secret>.+)', 'enroll',name="paloma_enroll",),
    url(r'^signin', 'signin',name="paloma_signin",),
    url(r'^signup/web/*(?P<command>[^/]*)', SignUpWebView.as_view(),name="paloma_signup_web",),

    url(r'^signup/mail', SignUpMailView.as_view(),name="paloma_signup_mail",),
)
