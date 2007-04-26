"""
URLConf for Coltrane.

Recommended usage is to use a call to ``include()`` in your project's
root URLConf to include this URLConf for any URL beginning with
'/weblog/'.

"""

from django.conf.urls.defaults import *
from django.views.generic import date_based, list_detail
from django.contrib.syndication.views import feed
from coltrane.models import Category, Entry, Link
from coltrane.views import list_detail as coltrane_list_detail

entry_info_dict = {
    'queryset': Entry.live,
    'date_field': 'pub_date',
    }

link_info_dict = {
    'queryset': Link.objects.all(),
    'date_field': 'pub_date',
    }

# Entries.
urlpatterns = patterns('',
                       url(r'^(?P<year>\d{4})/$',
                           date_based.archive_year,
                           entry_info_dict,
                           name='coltrane_entry_archive_year'),
                       url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
                           date_based.archive_month,
                           entry_info_dict,
                           name='coltrane_entry_archive_month'),
                       url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
                           date_based.archive_day,
                           entry_info_dict,
                           name='coltrane.entry_archive_day'),
                       url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
                           date_based.object_detail,
                           dict(entry_info_dict, slug_field='slug'),
                           name='coltrane_entry_detail'),
                       )

# Links.
urlpatterns += patterns('',
                       url(r'^links/(?P<year>\d{4})/$',
                           date_based.archive_year,
                           link_info_dict,
                           name='coltrane_link_archive_year'),
                       url(r'^links/(?P<year>\d{4})/(?P<month>\w{3})/$',
                           date_based.archive_month,
                           link_info_dict,
                           name='coltrane_link_archive_month'),
                       url(r'^links/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
                           date_based.archive_day,
                           link_info_dict,
                           name='coltrane_link_archive_day'),
                       url(r'^links/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
                           date_based.object_detail,
                           dict(link_info_dict, slug_field='slug'),
                           name='coltrane_link_detail'),
                       )

# Categories.
urlpatterns += patterns('',
                       url(r'^categories/$',
                           list_detail.object_list,
                           { 'queryset': Category.objects.all() },
                           name='coltrane_category_list'),
                       url(r'^categories/(?P<slug>[-\w]+)/$',
                           coltrane_list_detail.category_detail,
                           name='coltrane_category_detail'),
                        )
