"""
Urls for authentication app.
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^termsandconditions/', views.TermsAndConditions.as_view(), name='termsandconditions'),
    url(r'^register/', views.UserCreateAPIView.as_view(), name='register'),
    url(r'^login/', views.UserLoginAPIView.as_view(), name='login'),
    url(r'^activate/', views.ActivateUser.as_view(), name='activate_user'),
    url(r'^delete_user/', views.DeleteUser.as_view(), name='delete_user'),
    url(r'^user_details/', views.UserDetails.as_view(), name='user_details'),
    url(r'^new_password/', views.ChangePassword.as_view(), name='change_password'),
    url(r'^reset_password/', views.ForgotPassword.as_view(), name='forgot_password'),
]
