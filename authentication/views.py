"""
Views for authentication app.
"""
import oauth2_provider
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.db import DatabaseError
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
)
from .models import UserProfile
from django.conf import settings


class TermsAndConditions(APIView):
    """
    View to render terms & conditions page.

    * Anyone able to access.
    """
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'authentication/terms.html'

    def get(self, request):
        """
        Return terms.html template.
        """
        return Response()


class UserCreateAPIView(generics.CreateAPIView):
    """
    View to register a new user.

    * Anyone able to access.
    """
    permission_classes = [AllowAny]
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer, )
    template_name = 'authentication/signup.html'
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def get(self, request):
        """
        Return signup.html template.
        """
        return Response()

    def post(self, request, *args, **kwargs):
        """
        Create a new user instance.
        """
        data = request.data
        serializer = UserCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=False):
            new_data = serializer.data
            url = settings.SERVICES_DOMAIN + '/webapp/home/'
            serializer.create(serializer.data)
            subject = '[HCMR] Activate User'
            name = new_data['firstname'] + ' ' + new_data['lastname']
            html_content = render_to_string('authentication/activate_user_mail.html', {'url': url, 'name': name, 'country': new_data['country'],
                                                                                       'institution': new_data['institution'], 'email': new_data['email'], 'description': new_data['description']})
            # protect against header injection by forbidding newlines in header values
            try:
                send_mail(subject, name, 'antmoira@gmail.com', [
                        'antmoira@gmail.com'], fail_silently=False, html_message=html_content,)
            except BadHeaderError:
                return Response('Invalid header found.')
            return_data = {
                'success': True,
                'message': "You have successfully registered. An account activation email will be sent to you shortly."
            }
        else:
            return_data = {
                'success': False,
                'message': serializer.errors['non_field_errors'][0]
            }
        return Response(return_data)


class ActivateUser(generics.RetrieveUpdateAPIView):
    """
    View to activate new user.

    * Only admin users are able to access.
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['admin']
    renderer_classes = (JSONRenderer, )

    def get(self, request, *args, **kwargs):
        """
        Return a list of all the inactive users.
        """
        users = User.objects.filter(is_active=False)
        data1 = []
        for user in users:
            profile = UserProfile.objects.get(user=user)
            data1.append({'first_name': user.first_name,
                         'last_name': user.last_name,
                         'country': profile.country,
                         'institution': profile.institution,
                         'email': user.email,
                         'phone': profile.userPhone,
                         'description': profile.description
                         })
        users = User.objects.filter(is_active=True)
        data2 = []
        for user in users:
            profile = UserProfile.objects.get(user=user)
            data2.append({'first_name': user.first_name,
                         'last_name': user.last_name,
                         'country': profile.country,
                         'institution': profile.institution,
                         'email': user.email,
                         'phone': profile.userPhone,
                         'description': profile.description
                         })
        return_data = {
            'inactive': data1,
            'active' : data2
        }
        return Response(return_data)

    def put(self, request, *args, **kwargs):
        """
        Update is_active field of user instance and inform user.
        """
        email = request.data['email']
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        subject = '[HCMR] Account Activation'
        name = user.first_name
        url = settings.SERVICES_DOMAIN + '/webapp/home/'
        html_content = render_to_string(
            'authentication/accept_user_mail.html', {'url': url, 'name': name})
        try:
            send_mail(subject, name, 'antmoira@gmail.com', [
                email], fail_silently=False, html_message=html_content,)
        except BadHeaderError:
            return_data = {'success': False,
                           'message': 'Invalid header found.'
                           }
            return Response(return_data)
        return_data = {
            'success': True,
            'message': 'OK'
        }
        return Response(return_data)


class DeleteUser(generics.DestroyAPIView):
    """
    View to delete a user.

    * Only admin users are able to access.
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['admin']
    renderer_classes = (JSONRenderer, )

    def delete(self, request, *args, **kwargs):
        email = request.data['email']
        reason = request.data['reason']
        user = User.objects.get(email=email)
        user.delete()
        subject = '[HCMR] Your request has been rejected.'
        name = user.first_name
        html_content = render_to_string(
            'authentication/reject_user_mail.html', {'name': name, 'reason': reason})
        try:
            send_mail(subject, name, 'antmoira@gmail.com', [
                email], fail_silently=False, html_message=html_content,)
        except BadHeaderError:
            return_data = {'success': False,
                           'message': 'Invalid header found.'
                           }
            return Response(return_data)
        return_data = {
            'success': True,
            'message': 'OK'
        }
        return Response(return_data)


class UserLoginAPIView(APIView, oauth2_provider.views.mixins.OAuthLibMixin):
    """
    View to login a user.

    * Anyone able to access.
    """
    permission_classes = [AllowAny]
    renderer_classes = (TemplateHTMLRenderer, JSONRenderer, )
    template_name = 'authentication/login.html'
    serializer_class = UserLoginSerializer

    def get(self, request, *args, **kwargs):
        """
        Return signup.html template.
        """
        return Response()

    def post(self, request, *args, **kwargs):
        """
        Authenticate user and set the appropriate scopes for oauth2 access token.
        """
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=False):
            new_data = serializer.data
            user = authenticate(
                request, username=new_data['username'], password=new_data['password'])
            user_profile = UserProfile.objects.get(user=user)
            scopes = 'user'
            if user_profile.permission == 'S':
                scopes = scopes + ' staff'
            if user_profile.permission == 'A' and user.is_superuser:
                scopes = scopes + ' staff admin'
            login(request, user)
            new_data['password'] = ''
            return_data = {
                'success': True,
                'scopes': scopes
            }
        else:
            return_data = {
                'success': False,
                'message': serializer.errors['non_field_errors'][0]
            }
        return Response(return_data)


class ForgotPassword(APIView):
    """
    View to reset user's password.
    """
    permission_classes = [AllowAny]
    renderer_classes = (JSONRenderer, )

    def post(self, request, *args, **kwargs):
        """
        Reset password and send email.
        """
        email = request.POST.get('email', None)
        # try and get the user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # if it fails user doesn't exist
            user = None
        # if user is found
        if user is not None:
            newpassword = User.objects.make_random_password()
            user.set_password(newpassword)
            try:
                user.save()
            except DatabaseError:
                return_data = {
                    'success': False,
                    'message': 'Something went wrong. Please try again later.'
                }
                return Response(return_data)
            subject = '[HCMR] New Password'
            message = newpassword
            url = settings.SERVICES_DOMAIN + '/webapp/home/'
            html_content = render_to_string(
                'authentication/newpassword_mail.html', {'url': url, 'password': message})
            try:
                send_mail(subject, message, 'antmoira@gmail.com', [
                          email], fail_silently=False, html_message=html_content,)
            except BadHeaderError:
                return_data = {
                    'success': False,
                    'message': 'Invalid header found.'
                }
                return Response(return_data)
            return_data = {
                'success': True,
                'message': 'An email has been sent to you with a New Password.'
            }
        else:
            return_data = {
                'success': False,
                'message': 'This email is not valid.'
            }
        return Response(return_data)


class UserDetails(generics.RetrieveUpdateAPIView):
    """
    View to get or update user's profile.
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['user']
    renderer_classes = (JSONRenderer, )

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.get(user=user)
        return_data = {
            'username': user.username,
            # This method returns the “human-readable” value of the field.
            'permission': profile.get_permission_display(),
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bdate': profile.birthDate,
            # This method returns the “human-readable” value of the field.
            'gender': profile.get_gender_display(),
            'country': profile.country,
            'institution': profile.institution,
            'email': user.email,
            'phone': profile.userPhone,
            'description': profile.description
        }
        return Response(return_data)

    def put(self, request, *args, **kwargs):
        data = request.data
        user_profile = UserProfile.objects.get(user__email=data['email'])
        user_django = user_profile.user
        user_django.username = data['username']
        user_django.first_name = data['firstname']
        user_django.last_name = data['lastname']
        try:
            user_django.save()
        except DatabaseError:
            return_data = {
                'success': False,
                'message': 'Something went wrong. Please try again later.'
            }
            return Response(return_data)
        user_profile.userPhone = data['phone']
        user_profile.gender = data['gender']
        if data['bday'] != '' :
            user_profile.birthDate = data['bday']
        user_profile.country = data['country']
        user_profile.institution = data['institution']
        user_profile.description = data['description']
        try:
            user_profile.save()
        except DatabaseError:
            return_data = {
                'success': False,
                'message': 'Something went wrong. Please try again later.'
            }
            return Response(return_data)
        return_data = {
            'success': True,
            'message': 'OK'
        }
        return Response(return_data)


class ChangePassword(generics.UpdateAPIView):
    """
    View to change user's password.
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['user']
    renderer_classes = (JSONRenderer, )

    def put(self, request, *args, **kwargs):
        data = request.data
        email = data['email']
        old_password = data['old_psw']
        new_password = data['new_psw']
        user = User.objects.get(email=email)
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return_data = {
                'success': True,
                "message": "Your password has changed!"
            }
        else:
            return_data = {
                'success': False,
                "message": "Your current password is incorrect."
            }
        return Response(return_data)
