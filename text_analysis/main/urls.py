from django.conf.urls import url

from main import views

urlpatterns = [
    url(r'^parse$', views.parse, name='parse'),
    url(r'^reading$', views.reading, name='reading'),
]
