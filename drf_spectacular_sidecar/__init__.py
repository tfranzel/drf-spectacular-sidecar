import django

__version__ = '2021.09.25'

if django.VERSION < (3, 2):
    default_app_config = 'drf_spectacular.apps.SpectacularSidecarConfig'
