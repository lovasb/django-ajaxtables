from django.conf.urls import url, patterns
from . import views
from table.forms import FilterForm
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'list2/$', views.StatesListView.as_view(), name='states-list2'),
    url(r'(form|noform)/$', views.states_list, name='states-list'),
    url(r'^data/$', views.states_list_data, name='states-list-data'),
)