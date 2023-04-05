from django.core.mail import send_mail
from rest_framework import serializers
from apps.user.serializers import UserSerializer
from apps.user.models import User


class RegisterSerializer(UserSerializer):
    password = serializers.CharField(max_length=128,
                                     min_length=8, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email',
                  'username', 'first_name', 'last_name',
                  'password']

    def create(self, validated_data):
        send_mail(
            subject="That's your subject",
            message="That's your message body",
            from_email="tailhostserve@gmail.com",
            recipient_list=["keks.com.lyl@gmail.com"],
            fail_silently=False,
        )
        return User.objects.create_user(**validated_data)
