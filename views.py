"""
Weblog views.

These are just wrappers around generic views which
work out a couple of needed parameters.

"""
from django.shortcuts import get_object_or_404
from django.views.generic import list_detail
from tagging.models import Tag, TaggedItem
from coltrane.models import Category, Entry

def category_detail(request, slug):
    """
    View of all Entries in a particular Category.
    
    Context::
        Same as the generic ``list_detail.object_list``
        view, with one extra variable::
    
            object
                The Category.
    
    Template::
        cab/category_detail.html
    
    """
    category = get_object_or_404(Category, slug__exact=slug)
    return list_detail.object_list(request,
                                   queryset=category.entry_set.live(), # Only get live entries
                                   extra_context={ 'object': category },
                                   template_name='coltrane/category_detail.html',
                                   paginate_by=20)

def tag_detail(request, slug):
    """
    View of all Entries with a particular Tag.
    
    Context::
        Same as the generic ``list_detail.object_list``
        view, with one extra variable::
    
            object
                The Tag.
    
    Template::
        cab/tag_detail.html
    
    """
    tag = get_object_or_404(name__exact=slug)
    return list_detail.object_list(request,
                                   queryset=TaggedItem.get_by_model(Entry, tag).filter(status__exact=1),
                                   extra_context={ 'object': tag },
                                   template_name='coltrane/tag_detail.html',
                                   paginate_by=20)

                                   
