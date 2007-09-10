import datetime

from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic import date_based, list_detail

from coltrane.models import Category


def _category_kwarg_helper(category, kwarg_dict):
    if 'extra_context' in kwarg_dict:
        kwarg_dict['extra_context'].update(object=category)
    else:
        kwarg_dict['extra_context'] = { 'object': category }
    for key in ('queryset', 'date_field', 'template_name'):
        if key in kwarg_dict:
            del kwarg_dict[key]
    return kwarg_dict

def category_detail(request, slug, **kwargs):
    """
    Detail view of a ``Category``, listing entries published in it.
    
    This is a short wrapper around the generic
    ``list_detail.object_list`` view, so all context variables
    populated by that view will be available here. One extra variable
    is added::
    
        object
            The ``Category``.

    Additionally, any keyword arguments which are valid for
    ``list_detail.object_list`` will be accepted and passed to it,
    with these exceptions:

    * ``queryset`` will always be the ``QuerySet`` of live entries in
      the ``Category``.
    * ``template_name`` will always be 'coltrane/category_detail.html'.
    
    Template::
        coltrane/category_detail.html
    
    """
    category = get_object_or_404(Category, slug__exact=slug)
    kwarg_dict = _category_kwarg_helper(category, kwargs)
    return list_detail.object_list(request,
                                   queryset=category.live_entry_set,
                                   template_name='coltrane/category_detail.html',
                                   **kwarg_dict)

def category_archive_index(request, slug, **kwargs):
    """
    View of the latest entries published in a ``Category``.
    
    This is a short wrapper around the generic
    ``date_based.archive_index`` view, so all context variables
    populated by that view will be available here. One extra variable
    is added::
    
        object
            The ``Category``.
    
    Additionally, any keyword arguments which are valid for
    ``date_based.archive_year`` will be accepted and passed to it,
    with these exceptions:
    
    * ``queryset`` will always be the ``QuerySet`` of live entries in
      the ``Category``.
    * ``date_field`` will always be 'pub_date'.
    * ``template_name`` will always be 'coltrane/category_archive.html'.
    
    Template::
        coltrane/category_archive.html
    
    """
    category = get_object_or_404(Category, slug__exact=slug)
    kwarg_dict = _category_kwarg_helper(category, kwargs)
    return date_based.archive_index(request,
                                    queryset=category.live_entry_set,
                                    date_field='pub_date',
                                    template_name='coltrane/category_archive.html',
                                    **kwarg_dict)

def category_archive_year(request, slug, year, **kwargs):
    """
    View of entries published in a ``Category`` in a given year.
    
    This is a short wrapper around the generic
    ``date_based.archive_year`` view, so all context variables
    populated by that view will be available here. One extra variable
    is added::
    
        object
            The ``Category``.
    
    Additionally, any keyword arguments which are valid for
    ``date_based.archive_year`` will be accepted and passed to it,
    with these exceptions:
    
    * ``queryset`` will always be the ``QuerySet`` of live entries in
      the ``Category``.
    * ``date_field`` will always be 'pub_date'.
    * ``template_name`` will always be 'coltrane/category_archive_year.html'.
    
    Template::
        coltrane/category_archive_year.html
    
    """
    category = get_object_or_404(Category, slug__exact=slug)
    kwarg_dict = _category_kwarg_helper(category, kwargs)
    return date_based.archive_year(request,
                                   year=year,
                                   queryset=category.live_entry_set,
                                   date_field='pub_date',
                                   template_name='coltrane/category_archive_year.html',
                                   **kwarg_dict)

def category_archive_month(request, slug, year, month, **kwargs):
    """
    View of entries published in a ``Category`` in a given month.
    
    This is a short wrapper around the generic
    ``date_baed.archive_month`` view, so all context variables
    populated by that view will be available here. One extra variable
    is added::
    
        object
            The ``Category``.
    
    Additionally, any keyword arguments which are valid for
    ``date_based.archive_month`` will be accepted and passed to it,
    with these exceptions:
    
    * ``queryset`` will always be the ``QuerySet`` of live entries in
      the ``Category``.
    * ``date_field`` will always be 'pub_date'.
    * ``template_name`` will always be 'coltrane/category_archive_month.html'.
    
    Template::
        coltrane/category_archive_month.html
    
    """
    category = get_object_or_404(Category, slug__exact=slug)
    kwarg_dict = _category_kwarg_helper(category, kwargs)
    return date_based.archive_month(request,
                                    year=year,
                                    month=month,
                                    queryset=category.live_entry_set,
                                    date_field='pub_date',
                                    template_name='coltrane/category_archive_month.html',
                                    **kwarg_dict)

def category_archive_day(request, slug, year, month, day, **kwargs):
    """
    View of entries published in a ``Category`` on a given day.
    
    This is a short wrapper around the generic
    ``date_based.archive_day`` view, so all context variables
    populated by that view will be available here. One extra variable
    is added::
    
        object
            The ``Category``.
    
    Additionally, any keyword arguments which are valid for
    ``date_based.archive_day`` will be accepted and passed to it, with
    these exceptions:
    
    * ``queryset`` will always be the ``QuerySet`` of live entries in
      the ``Category``.
    * ``date_field`` will always be 'pub_date'.
    * ``template_name`` will always be 'coltrane/category_archive_day.html'.
    
    Template::
        coltrane/category_archive_day.html
    
    """
    category = get_object_or_404(Category, slug__exact=slug)
    kwarg_dict = _category_kwarg_helper(category, kwargs)
    return date_based.archive_day(request,
                                 year=year,
                                 month=month,
                                 day=day,
                                 queryset=category.live_entry_set,
                                 date_field='pub_date',
                                 template_name='coltrane/category_archive_day.html',
                                 **kwarg_dict)

def category_archive_today(request, slug, **kwargs):
    """
    View of entries published in a ``Category`` on the current date.
    
    This is a short wrapper around the generic
    ``date_based.archive_day`` view (the generic
    ``date_based.archive_today`` view is also a short wrapper around
    ``date_based.archive_day``), so all context variables populated by
    that view will be available here. One extra variable is added::
    
        object
            The ``Category``.
    
    Additionally, any keyword arguments which are valid for
    ``date_based.archive_day`` will be accepted and passed to it, with
    these exceptions:
    
    * ``queryset`` will always be the ``QuerySet`` of live entries in
      the ``Category``.
    * ``date_field`` will always be 'pub_date'.
    * ``template_name`` will always be 'coltrane/category_archive_day.html'.
    
    Template::
        coltrane/category_archive_day.html
    
    """
    today = datetime.datetime.today()
    return category_archive_day(request,
                                year = str(today.year),
                                month = today.strftime('%b').lower(),
                                day = today.strftime('%d'),
                                **kwargs)
