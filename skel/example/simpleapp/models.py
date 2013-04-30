# -*- coding: utf-8 -*-
from django.db import models


class SimpleModel(models.Model):
    """
    (SimpleModel description)
    """

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('simplemodel_detail_view_name', [str(self.id)])
