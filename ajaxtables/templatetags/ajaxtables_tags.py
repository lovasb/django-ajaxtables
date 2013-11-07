from django import template
from django.conf import settings
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag(takes_context=False)
def ajaxtables_imports(import_cookies_js=True, import_autoload=True, template_name='ajaxtables/imports.html'):
    """ 
    Renders the imports file.
    """
    return render_to_string(template_name, {'import_cookies_js': import_cookies_js, 
                                            'import_autoload': import_autoload})