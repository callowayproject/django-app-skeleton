from django.conf.urls.defaults import *

from .models import SimpleModel

urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^$', 'object_list', {
        'queryset': SimpleModel.objects.all(),
    }, name="simplemodel_list"),
    (r'^(?P<slug>[\w-]+)/', 'object_detail', {
        'queryset': SimpleModel.objects.all(),
    }, name="simplemodel_detail")
)
