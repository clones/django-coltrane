from django.db.models import get_model
from django import template
from django.contrib.comments.models import Comment, FreeComment
from coltrane.models import Entry, Link


register = template.Library()


class LatestContentNode(template.Node):
    def __init__(self, queryset, num, varname):
        self.queryset = queryset
        self.num, self.varname = num, varname
    
    def render(self, context):
        context[self.varname] = self.queryset[:self.num]
        return ''

def do_latest_entries(parser, token):
    """
    Inserts the latest ``num`` published entries (i.e., those with
    "live" status) into ``varname``.
    
    Example::
    
        {% get_latest_entries 5 as latest_entries %}
        
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes exactly three arguments" % bits[0])
    return LatestContentNode(queryset=Entry.objects.live(),
                             num=int(bits[1]),
                             varname=bits[3])

def do_latest_links(parser, token):
    """
    Inserts the latest ``num`` links into ``varname``.
    
    Example::
    
        {% get_latest_links 5 as latest_links %}
    
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes exactly three arguments" % bits[0])
    return LatestContentNode(queryset=Link.objects.all(),
                             num=int(bits[1]),
                             varname=bits[3])

def do_latest_comments(parser, token):
    """
    Inserts the latest ``num`` approved comments (i.e., those with
    ``is_public=True`` into ``varname``.
    
    Pass ``FreeComment`` as the second argument if you're using the
    ``FreeComment`` model, or ``Comment`` if you're using the ``Comment``
    model.
    
    Example::
    
        {% get_latest_comments FreeComment 5 as latest_comments %}
    
    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'%s' tag takes exactly four arguments" % bits[0])
    if bits[1] not in ("Comment", "FreeComment"):
        raise template.TemplateSyntaxerror("First argument to '%s' tag must be the name of the comment model to use" % bits[0])
    comment_model = { 'FreeComment': FreeComment,
                      'Comment': Comment }[bits[1]]
    return LatestContentNode(queryset=comment_model.objects.filter(is_public__exact=True),
                                                                   num=int(bits[2]),
                                                                   varname=bits[3])

register.tag('get_latest_entries', do_latest_entries)
register.tag('get_latest_links', do_latest_links)
register.tag('get_latest_comments', do_latest_comments)
