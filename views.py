from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import date_based, list_detail
from tagging.models import Tag
from coltrane.models import Category, Entry, Link

paginate_by = (hasattr(settings, 'PAGINATE_BY') and settings.PAGINATE_BY) or 20

def category_detail(request, slug):
    """
    Detail view of a Category, listing Entries posted in it.
    
    This is a short wrapper around the generic
    ``list_detail.object_list`` view, so all context variables
    populated by that view will be available here. One extra variable
    is added::
    
        object
            The Category.
    
    Template::
        coltrane/category_detail.html
    
    """
    category = get_object_or_404(Category, slug__exact=slug)
    return list_detail.object_list(request,
                                   queryset=category.live_entry_set,
                                   extra_context={ 'object': category },
                                   template_name='coltrane/category_detail.html',
                                   paginate_by=paginate_by,
                                   allow_empty=True)

def entry_detail(request, year, month, day, slug):
    """
    Detail view of an Entry.
    
    Context::
    
        object
            The Entry.
            
        next_entry
            The next live Entry by ``pub_date``, if there is one.
    
        previous_entry
            The previous live Entry by ``pub_date``, if there is one.
    
    Template::
        coltrane/entry_detail.html
    
    """
    entry = get_object_or_404(Entry,
                              pub_date__year=year,
                              pub_date__month=month,
                              pub_date__day=day,
                              slug__exact=slug)
    try:
        next_entry = entry.get_next()
    except Entry.DoesNotExist:
        next_entry = None
    try:
        previous_entry = entry.get_previous()
    except:
        previous_entry = None
    return render_to_response('coltrane/entry_detail.html',
                              { 'object': entry,
                                'next_entry': entry.get_next(),
                                'previous_entry': entry.get_previous() },
                              context_instance=RequestContext(request))

