# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'views.index', name='index'),
)
