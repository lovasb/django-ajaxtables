try:
    from lxml import etree
except ImportError:
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
    retval = {}
    html = render_to_string(*args, **kwargs)
    try:
        root = etree.HTML(html)
        retval['tbody'] = ''.join([etree.tostring(row) for row in root.xpath('//tbody/tr')])
        retval['tfoot'] = ''.join([etree.tostring(row) for row in root.xpath('//tfoot/tr')])
    except NameError:
        root = parseString(html.encode('utf8'))
        retval['tbody'] = ''.join([row.toxml() for row in root.getElementsByTagName("tbody")[0].childNodes])
        retval['tfoot'] = ''.join([row.toxml() for row in root.getElementsByTagName("tfoot")[0].childNodes])
    return retval