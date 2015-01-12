from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^text-analysis/v1/', include('main.urls')),
)
