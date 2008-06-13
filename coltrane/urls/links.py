"""
URLs for links in a weblog.

"""

from django.conf.urls.defaults import *
from django.views.generic import date_based
from django.views.generic import list_detail

from tagging.models import Tag

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
                       url(r'^links/tags/$',
                           list_detail.object_list,
                           { 'queryset': Tag.objects.all(),
                             'template_name': 'coltrane/link_tag_archive.html',
                             'paginate_by': 40 },
                           name='coltrane_link_tag_archive'),
                       url(r'^links/tags/(?P<tag>[-\w]+)/$',
                           tagged_object_list,
                           { 'queryset_or_model': Link.objects.all(),
                             'template_name': 'coltrane/link_tag_detail.html' },
                           name='coltrane_link_tag_detail'),
                       url(r'^(?P<year>\d{4})/$',
                           date_based.archive_year,
                           dict(link_info_dict, make_object_list=True),
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
