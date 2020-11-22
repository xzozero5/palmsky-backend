from .views import *

from django.conf.urls import url
app_name = 'backend'

urlpatterns = [
    url(r'^tag/$',TagListAPIView.as_view(),name='Tag-list'),
    url(r'^book/tag/$',BookTagListAPIView.as_view(),name='Tag-book-list'),
    url(r'^book/$',BookListAPIView.as_view(),name='Book-list'),
    url(r'^book/(?P<pk>\d+)/$',BookRudView.as_view(),name='Book-rud'),
] 
