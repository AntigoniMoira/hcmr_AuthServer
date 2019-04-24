"""
Django OAuth Toolkit scopes backend for the dot-restrict-scopes package.
"""

from django.conf import settings
from django.utils import module_loading

from oauth2_provider.scopes import BaseScopes


class RestrictApplicationScopes(BaseScopes):
    """
    Scopes backend that wraps another backend and restricts the scopes available
    to an application based on the application's ``allowed_scopes``.
    """
    def __init__(self):
        # Initialise the wrapped backend from settings
        self._wrapped = module_loading.import_string(
            getattr(settings, 'DOT_RESTRICT_SCOPES', {}).get(
                'WRAPPED_SCOPES_BACKEND_CLASS',
                'oauth2_provider.scopes.SettingsScopes'
            )
        )()

    def get_all_scopes(self):
        # Just return all the available scopes from the wrapped backend
        return self._wrapped.get_all_scopes()

    def get_available_scopes(self, application = None, request = None, *args, **kwargs):
        # Get the available scopes from the wrapped backend, then filter them
        # based on the allowed_scopes of the application
        scopes = self._wrapped.get_available_scopes(application, request, *args, **kwargs)
        if application:
            scopes = [s for s in scopes if s in application.allowed_scopes]
        return scopes

    def get_default_scopes(self, application = None, request = None, *args, **kwargs):
        # Get the default scopes from the wrapped backend, then filter them
        # based on the allowed_scopes of the application
        scopes = self._wrapped.get_default_scopes(application, request, *args, **kwargs)
        if application:
            scopes = [s for s in scopes if s in application.allowed_scopes]
        return scopes
