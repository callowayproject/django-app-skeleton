#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings


DEFAULT_SETTINGS = {

}

USER_SETTINGS = DEFAULT_SETTINGS.copy()
USER_SETTINGS.update(getattr(settings, '{{app_name}}_SETTINGS'))

globals().update(USER_SETTINGS)
