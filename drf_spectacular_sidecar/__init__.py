import django

__version__ = '2025.6.14'

if django.VERSION < (3, 2):
    default_app_config = 'drf_spectacular_sidecar.apps.SpectacularSidecarConfig'
