from django.conf.urls import include, url

urlpatterns = [
    url(r'^text-analysis/v1/', include('main.urls')),
    url(r'^v1/', include('main.urls')),
]
