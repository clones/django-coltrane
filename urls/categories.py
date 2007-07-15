"""
URLs for categories in a weblog.

"""

from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list

from coltrane.models import Category
from coltrane.views import category_detail


urlpatterns += patterns('',
                       url(r'^categories/$',
                           object_list,
                           { 'queryset': Category.objects.all() },
                           name='coltrane_category_list'),
                       url(r'^categories/(?P<slug>[-\w]+)/$',
                           category_detail,
                           name='coltrane_category_detail'),
                        )
