import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from table.models import State
from django.core.paginator import Paginator, EmptyPage
from table.forms import FilterForm
from ajaxtables.utils import render_table_parts, render_table

def states_list(request, with_form, template_name='table/states_list.html'):
    form = None
    if with_form == 'form':
        form = FilterForm()
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))


def states_list_data(request):
    response_data = {}
    page_size = int(request.GET.get('pageSize', 5))
    act_page = int(request.GET.get('actPage', 1))
    if request.method == 'POST': ## ...use form
        form = FilterForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            states = State.objects.filter(name__istartswith=data['name'].lower())
        else:
            states = State.objects.all()
    else:
        states = State.objects.all()
    paginator = Paginator(states, page_size)
    try:
        states = paginator.page(act_page)
    except:
        states = paginator.page(1)
    response_data = render_table('table/states_list_data.html',
                                  {'objects': states},
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