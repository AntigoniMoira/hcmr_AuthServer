"""
    This is the root url file.
"""

from django.contrib import admin
from django.contrib.auth.views import login
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # add new application only from admin (for Oauth2)
    path('o/applications/',
         TemplateView.as_view(template_name="authentication/error_page.html"), name='error'),
    # OAuth2 urls
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # include all urls from the app "authentication"
    path('auth/', include('authentication.urls')),
    path('accounts/login/', login,
         {'template_name': 'authentication/login.html'}),
]
