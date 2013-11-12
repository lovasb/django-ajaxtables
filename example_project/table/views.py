import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from table.models import State
from django.core.paginator import Paginator, EmptyPage
from table.forms import FilterForm
from ajaxtables.utils import render_table_parts, render_table
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from ajaxtables.views import AjaxListView


class StatesListView(AjaxListView):
    model = State
    template_names = ['table/state_list.html', 'table/state_list_data.html']
    filter_form_class = FilterForm

def states_list(request, with_form, template_name='table/state_list.html'):
    form = None
    if with_form == 'form':
        form = FilterForm()
    return render_to_response(template_name,
                                {'form': form},
                                context_instance=RequestContext(request))


def states_list_data(request):
    response_data = {}
    page_size = int(request.GET.get('pageSize', 5))
    act_page = int(request.GET.get('toPage', 1))
    states = State.objects.all()
    form = FilterForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        states = State.objects.filter(name__istartswith=data['name'].lower())
    paginator = Paginator(states, page_size)
    try:
        states = paginator.page(act_page)
    except:
        states = paginator.page(1)
    response_data = render_table('table/state_list_data.html',
                                    {'object_list': states},
                                    context_instance=RequestContext(request))
    return HttpResponse(json.dumps(response_data), content_type="application/json")


"""
response_data['tbody'] = render_to_string('table/states_list_tbody.html',
                                              {'states': states},
                                              context_instance=RequestContext(request))
response_data['tfoot'] = render_to_string('table/states_list_tfoot.html',
                                          {'states': states},
                                          context_instance=RequestContext(request))
return HttpResponse(json.dumps(response_data), content_type="application/json")

##########################################################
response_data = render_table_parts(tbody_template='table/states_list_tbody.html',
                                       tfoot_template='table/states_list_tfoot.html',
                                       dictionary={'states': states},
                                       context_instance=RequestContext(request))
##########################################################
response_data = render_table_parts(tbody_template='table/states_list_tbody.html',
                                       dictionary={'objects': states},
                                       context_instance=RequestContext(request))
##########################################################
response_data = render_table_parts(tbody_template='table/states_list_tbody.html',
                                       dictionary={'objects': states},
                                       context_instance=RequestContext(request))
"""