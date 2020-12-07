from .views import *
from django.urls import path
from django.conf.urls import url,include
from rest_framework.routers import DefaultRouter
app_name = 'backend'


###router.register(r'login',MyAuthToken.as_view(),basename='login')
urlpatterns = [
    url(r'^tag/$',TagListAPIView.as_view(),name='Tag-list'),
    url(r'^book/tag/$',BookTagListAPIView.as_view(),name='Tag-book-list'),
    url(r'^book/$',BookListAPIView.as_view(),name='Book-list'),
    url(r'^book/rank/$',BookListRankAPIView.as_view(),name='Book-list-rank'),
    url(r'^book/(?P<pk>\d+)/$',BookRudView.as_view(),name='Book-rud'),
    url(r'^account/(?P<pk>\d+)/$',UserAccountViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update','delete': 'destroy'}),name='account-rud'),
    url(r'^account/$',UserAccountViewSet.as_view({'get': 'list','post': 'create'}),name='account-list'),
    path('login/',UserLoginApiView.as_view()),
] 

