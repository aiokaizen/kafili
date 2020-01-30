from django.conf.urls import url

from orphanage.views import *

app_name = 'orphanage'

urlpatterns = [
    url(r'^login$', connexion, name='login'),
    url(r'^logout$', logout, name='logout'),
    url(r'^profile$', profile, name='profile'),
    url(r'^$', children_list, name='home'),
    url(r'^children_list/$', children_list, name='children_list'),
    url(r'^child_details/(?P<id>[0-9]+)$', child_details, name='child_details'),
    url(r'^child_insert/$', child_insert, name='child_insert'),
    url(r'^child_details/(?P<id>[0-9]+)/update$', child_update, name='child_update'),
]
