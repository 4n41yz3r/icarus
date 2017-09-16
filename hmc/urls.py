from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.CatalogView.as_view(), name='index'),
    url(r'^stream/(.+)', views.StreamView.as_view(), name='stream')
]
