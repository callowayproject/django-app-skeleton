# -*- coding: utf-8 -*-
from django.conf import settings as site_settings


DEFAULT_SETTINGS = {

}

USER_SETTINGS = DEFAULT_SETTINGS.copy()
USER_SETTINGS.update(getattr(site_settings, '{{app_name}}_SETTINGS', {}))

globals().update(USER_SETTINGS)
