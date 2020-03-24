from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from feed import views

urlpatterns = [
    url('api-auth/', include('rest_framework.urls')),
    url(r'^list/$', views.FeedList.as_view(), name='feed_list'),
    url(r'^insert/$', views.FeedList.as_view(), name='feed_insert'),
    url(r'^detail/(?P<pk>\d+)/$', views.FeedDetail.as_view()),
    url(r'^detail/(?P<pk>\d+)/comment$', views.CommentList.as_view()),
    url(r'^detail/(?P<pk>\d+)/comment/(?P<cpk>\d+)$', views.CommentDetail.as_view()),
    url(r'^detail/(?P<pk>\d+)/like$', views.LikeDetail.as_view()),
]
