"""
URLs for entries in a weblog.

"""

from django.conf.urls.defaults import *
from django.views.generic import date_based

from coltrane.models import Entry


entry_info_dict = {
    'queryset': Entry.live.all(),
    'date_field': 'pub_date',
    }


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
