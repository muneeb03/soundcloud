from rest_framework import serializers
from apps.account.models import User
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import  PasswordResetTokenGenerator


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2= serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'password2']
        extra_kwargs ={
            'password':{'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password does not match')
        return attrs
    
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    notifications = serializers.ListField(child=serializers.CharField(), read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'notifications']


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 255, style= {'input_type':'password'}, write_only = True)
    password2 = serializers.CharField(max_length = 255, style= {'input_type':'password'}, write_only = True)
    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Password does not match')
        user.set_password(password)
        user.save()
        return attrs


class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID: ', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token: ',token)
            link = 'http://localhost:8000/api/users/reset-password/'+uid+'/'+token
            print('Password Reset Link: ', link)
            #SEND EMAIL
            """body = 'Click on the following link to reset your password ' + link
            data = {
                'subject' : 'PASSWORD RESET LINK',
                'body' : body,
                'to_email' : user.email
            }
            Util.send_email(data)"""
            return attrs

        else:
            raise ValidationError('This email is not registered!')

        
class NewResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 255, style= {'input_type':'password'}, write_only = True)
    password2 = serializers.CharField(max_length = 255, style= {'input_type':'password'}, write_only = True)
    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError('Password does not match')
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError('Token is not valid')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError('Token is not valid')

