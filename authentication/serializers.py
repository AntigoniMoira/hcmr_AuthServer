from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile


class UserCreateSerializer(serializers.ModelSerializer):
    """
        Serializer for register user data.
    """
    firstname = serializers.CharField(allow_blank=False)
    lastname = serializers.CharField(allow_blank=False)
    country = serializers.CharField(allow_blank=True)
    institution = serializers.CharField(allow_blank=True)
    phone = serializers.CharField(allow_blank=True)
    email = serializers.EmailField(label='Email Address')
    password2 = serializers.CharField(allow_blank=False)
    description = serializers.CharField(allow_blank=False)

    class Meta:
        model = User
        fields = [
            'firstname',
            'lastname',
            'country',
            'institution',
            'phone',
            'email',
            'password',
            'password2',
            'description',
        ]
        extra_kwargs = {"password":
                            {
                                "write_only": True
                            },
                        "password2":
                            {
                                "write_only": True
                            }
                        }

    def validate(self, data):
        """
        Check that user gave valid data.
        """
        email = data.get('email', None)
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise serializers.ValidationError("This email is already used.")
        password1 = data.get("password")
        password2 = data.get("password2")
        if password1 != password2:
            raise serializers.ValidationError("Passwords must match!")
        return data

    def create(self, validated_data):
        username = validated_data['email']
        email = validated_data['email']
        password = validated_data['password2']
        user_obj = User(
            username=username,
            email=email,
            is_active=False,
        )
        user_obj.set_password(password)
        user_obj.first_name = validated_data['firstname']
        user_obj.last_name = validated_data['lastname']
        user_obj.save()
        institution = validated_data['institution']
        description = validated_data['description']
        phone = validated_data['phone']
        country = validated_data['country']
        UserProfile.objects.create(user=user_obj, userPhone=phone,
                                   country=country, institution=institution, description=description)
        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Check that user gave valid credentials.
    """
    username = serializers.CharField(allow_blank=True, read_only=True)
    email = serializers.EmailField(
        label='Email Address', required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]

    def validate(self, data):
        user_obj = None
        email = data.get("email", None)
        password = data["password"]

        user = User.objects.filter(email=email).distinct()
        user = user.exclude(email__isnull=True).exclude(email='')
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError("This email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError(
                    "Incorect password please try again.")
            if user_obj.is_active == False:
                raise serializers.ValidationError(
                    "Your account has not yet been activated.")

        data['username'] = user_obj.username
        return data
