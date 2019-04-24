"""
Django models for the dot-restrict-scopes package.
"""

from django.db import models

from oauth2_provider.models import AbstractApplication
from oauth2_provider.scopes import get_scopes_backend


class RestrictedApplication(AbstractApplication):
    """
    Application model for use with Django OAuth Toolkit that allows the scopes
    available to an application to be restricted on a per-application basis.
    """
    allowed_scope = models.TextField(blank = True)

    @property
    def allowed_scopes(self):
        """
        Returns the set of allowed scope names for this application.
        """
        all_scopes = set(get_scopes_backend().get_all_scopes().keys())
        app_scopes = set(self.allowed_scope.split())
        return app_scopes.intersection(all_scopes)
