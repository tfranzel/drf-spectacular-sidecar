import django

__version__ = '2023.8.1'

if django.VERSION < (3, 2):
    default_app_config = 'drf_spectacular_sidecar.apps.SpectacularSidecarConfig'
