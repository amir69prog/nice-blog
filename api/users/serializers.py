from rest_framework import serializers

from blog.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'username',
                  'email', 'first_name', 'last_name')
        read_only_fields = ['id']


class CustomRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ('phone_number', 'username', 'email', 'password', 'password2')

    def validate(self, attrs):
        data = self.get_initial()
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            raise serializers.ValidationError('Passwords must match')
        return attrs

    def save(self, **kwargs):
        data = self.get_initial()
        password = data.get('password')
        user = User.objects.create_user(
            phone_number=data.get('phone_number'),
            username=data.get('username'),
            email=data.get('email'),
            password=password,
            is_verified=False
        )
        return user


class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField()
