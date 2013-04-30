# -*- coding: utf-8 -*-
from django.conf.urls.defaults import url, patterns

from .models import SimpleModel


urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^$',
        'object_list',
        {'queryset': SimpleModel.objects.all()},
        name="simplemodel_list"
    ),
    url(r'^(?P<slug>[\w-]+)/',
        'object_detail',
        {'queryset': SimpleModel.objects.all()},
        name='simplemode_detail',
    ),
)
