from django.conf.urls import include, url

urlpatterns = [
    url(r'^text-analysis/v1/', include('main.urls')),
    url(r'^v1/', include('main.urls')),
]

handler400 = 'main.views.handler400'
handler403 = 'main.views.handler403'
handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'
