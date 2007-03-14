"""
URLConf for Coltrane.

Recommended usage is to use a call to ``include()`` in your project's
root URLConf to include this URLConf for any URL beginning with
'/weblog/'.

"""

from django.conf.urls.defaults import *
from django.views.generic import date_based
from django.contrib.syndication.views import feed
from tagging.models import Tag
import feeds, views
from models import Category, Entry, Link

# Info for feeds.
feed_dict = {
    'author': feeds.SnippetsByAuthorFeed,
    'language': feeds.SnippetsByLanguageFeed,
    'latest': feeds.LatestSnippetsFeed,
    'tag': feeds.SnippetsByTagFeed,
    }

entry_info_dict = {
    'queryset': Entry.objects.live(),
    'date_field': 'pub_date',
    }

link_info_dict = {
    'queryset': Link.objects.all(),
    'date_field': 'pub_date',
    }

# Generic views.
urlpatterns = patterns('',
                       (r'^$', date_based.archive_index, dict(entry_info_dict, num_latest=10)),
                       (r'^(?P<year>\d{4})/$', date_based.archive_year, entry_info_dict),
                       (r'^(?P<year>\d{4})/(?P<month>\w{3})/$', date_based.archive_month, entry_info_dict),
                       (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', date_based.archive_day, entry_info_dict),
                       (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', date_based.object_detail, dict(entry_info_dict, slug_field='slug')),
                       (r'^categories/$', list_detail.object_list, { 'queryset': Category.objects.all() }),
                       (r'^categories/(?P<slug>[-\w]+)/$', views.category_detail),
                       (r'^links/(?P<year>\d{4})/$', date_based.archive_year, link_info_dict),
                       (r'^links/(?P<year>\d{4})/(?P<month>\w{3})/$', date_based.archive_month, link_info_dict),
                       (r'^links/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', date_based.archive_day, link_info_dict),
                       (r'^links/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', date_based.object_detail, dict(link_info_dict, slug_field='slug')),
                       (r'^tags/$', list_detail.object_list, { 'queryset': Tag.objects.all() }),
                       (r'^tags/(?P<slug>[-\w]+)/$', views.tag_detail),
                       )
