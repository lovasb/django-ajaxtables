from xml.dom.minidom import parseString
from django.template.loader import render_to_string


def render_table_parts(tbody_template=None, tfoot_template="ajaxtables/table_tfoot.html", **kwargs):
    """
    Renders the tbody and tfoot separately.
    """
    retval = {}
    retval['tbody'] = render_to_string(tbody_template, **kwargs)
    retval['tfoot'] = render_to_string(tfoot_template, **kwargs)
    return retval


def render_table(*args, **kwargs):
    html = render_to_string(*args, **kwargs)
    root = parseString(html.encode('utf8'))
    retval = {}
    retval['tbody'] = root.getElementsByTagName("tbody")[0].toxml()
    retval['tbody'] = retval['tbody'].replace('<tbody>', '').replace('</tbody>', '') #TODO: some other solution
    retval['tfoot'] = root.getElementsByTagName("tfoot")[0].toxml()
    retval['tfoot'] = retval['tfoot'].replace('<tfoot>', '').replace('</tfoot>', '') #TODO: some other solution
    return retval