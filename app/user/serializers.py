"""
Serializers for the user API View.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers

#this is where we import serializer module from rest framowrk
#serializer is a way to convert obj to and from py obj
#it take JSON input from API and validate it then it convert it to py obj or a model
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None) #we put pwd none in case user chose to only update its name
        user = super().update(instance, validated_data)

        if password: #in case user update pwd "pwd=true"
            user.set_password(password)
            user.save()

        return user
    
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}, #we put its type 'password' so the pwd text can be hidden
        trim_whitespace=False,
    )

    def validate(self, attrs): #when the data is posted to the view, it'll pass it to serializer then it call this method to validate the data is correct
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs