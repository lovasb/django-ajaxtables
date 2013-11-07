from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class FilterForm(forms.Form):
    name = forms.CharField(label='State name', required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        super(FilterForm, self).__init__(*args, **kwargs)
        self.helper.form_id = 'searchForm'
        self.helper.add_input(Submit('query', 'Search'))