from django.http import Http404
from django.core.exceptions import ImproperlyConfigured

from vanilla import ListView


class AjaxListView(ListView):
    template_names = ['ajaxtables/object_list.html', 'ajaxtables/object_list_data.html']
    filter_form_class = None
    page_size = 10
    page_kwarg = 'page'

    def get_page_from_request(self):
        page_size = int(self.request.GET.get('pageSize', self.page_size))
        act_page = int(self.request.GET.get('toPage', 1))
        return page_size, act_page

    def get_template_names(self):
        try:
            assert len(self.template_names) == 2
        except AssertionError:
            msg = "'%s' must have two template names. One for view the" \
                  "table, and one for the jax loaded data."
            raise ImproperlyConfigured(msg % self.__class__.__name__)
        if self.request.is_ajax():
            return [self.template_names[1]]
        return [self.template_names[0]]

    def form_to_filters(self, form_data):
        return {}

    def append_display_filters(self, queryset):
        sort_by = self.request.POST.get('sort_by', None)
        if sort_by:
            queryset = queryset.order_by(sort_by)

        hidden_cols = self.request.POST.get('hidden_cols', None)
        if hidden_cols:
            queryset = queryset.defer(hidden_cols)
        return queryset

    def paginate_queryset(self, queryset):
        page_size, act_page = self.get_page_from_request()
        try:
            return super(AjaxListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            paginator = self.get_paginator(queryset, page_size)
            return paginator.page(1)

    def get(self, request, *args, **kwargs):
        if request.is_ajax(): ## no filter form provided, and request for data
            queryset = self.get_queryset()
            page_size, act_page = self.get_page_from_request()
            page = self.paginate_queryset(queryset)
            self.object_list = page.object_list
            context = self.get_context_data(
                page_obj=page,
                is_paginated=page.has_other_pages(),
                paginator=page.paginator,
            )
            return self.render_to_response(context)
        form = self.filter_form_class(request.POST or None) if self.filter_form_class else None
        return self.render_to_response({'form': form, 'page_size': self.page_size})

    def post(self, request, *args, **kwargs):
        form = self.filter_form_class(request.POST or None)
        print request.POST
        if form.is_valid():
            filters = self.form_to_filters(form.cleaned_data)
            queryset = self.append_display_filters(self.get_queryset().filter(**filters))
            page = self.paginate_queryset(queryset)
            self.object_list = page.object_list
            context = self.get_context_data(
                page_obj=page,
                is_paginated=page.has_other_pages(),
                paginator=page.paginator,
            )
            return self.render_to_response(context)