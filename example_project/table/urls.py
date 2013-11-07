from django.conf.urls import url, patterns
from . import views

urlpatterns = patterns('',
    url(r'^(form|noform)/$', views.states_list),
    url(r'^data/$', views.states_list_data, name='states-list-data')
)