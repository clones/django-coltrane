from django.db.models import get_model
from django import template
from django.contrib.comments.models import Comment, FreeComment
from coltrane.models import Entry, Link


register = template.Library()


class LatestFeaturedNode(template.Node):
    def __init__(self, varname):
        self.varname = varname
    
    def render(self, context):
        context[self.varname] = Entry.live.latest_featured()
        return ''


def do_latest_featured(parser, token):
    """
    Retrieves the latest featured Entry and stores it in a specified
    context variable.
    
    Syntax::
    
        {% get_latest_featured_entry as [varname] %}
    
    Example::
    
        {% get_latest_featured_entry as latest_featured_entry %}
    
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    if bits[1] != 'as':
        raise template.TemplateSyntaxError("first argument to '%s' tag must be 'as'" % bits[0])
    return LatestFeaturedNode(bits[2])

register.tag('get_latest_featured_entry', do_latest_featured)
