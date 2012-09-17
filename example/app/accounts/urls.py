from django.conf.urls import patterns, include, url
from app.accounts.views import SignUpMailView,SignUpWebView

urlpatterns = patterns('app.accounts.views',
    url(r'^enroll/(?P<command>.+)/(?P<secret>.+)', 'enroll',name="accounts_enroll",),
    url(r'^signin', 'signin',name="accounts_signin",),
    url(r'^signup/web/*(?P<command>[^/]*)', SignUpWebView.as_view(),name="accounts_signup_web",),
    url(r'^signup/mail', SignUpMailView.as_view(),name="accounts_signup_mail",),
    url(r'',"default",name="accounts_default"),
)
