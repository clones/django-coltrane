"""
URLs for links in a weblog.

"""

from django.conf.urls.defaults import *
from django.views.generic import date_based

from coltrane.models import Link


link_info_dict = {
    'queryset': Link.objects.all(),
    'date_field': 'pub_date',
    }


urlpatterns = patterns('',
                       url(r'^$',
                           date_based.archive_index,
                           link_info_dict,
                           name='coltrane_link_archive_index'),
                       url(r'^(?P<year>\d{4})/$',
                           date_based.archive_year,
                           link_info_dict,
                           name='coltrane_link_archive_year'),
                       url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
                           date_based.archive_month,
                           link_info_dict,
                           name='coltrane_link_archive_month'),
                       url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$',
                           date_based.archive_day,
                           link_info_dict,
                           name='coltrane_link_archive_day'),
                       url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
                           date_based.object_detail,
                           dict(link_info_dict, slug_field='slug'),
                           name='coltrane_link_detail'),
                       )
