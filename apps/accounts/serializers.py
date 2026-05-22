import logging
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from .models import User

logger = logging.getLogger(__name__)


class UserCreateSerializer(BaseUserCreateSerializer):
    """Override to send welcome email and return flat errors."""

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "first_name", "last_name", "password")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_email(self, value):
        value = value.lower().strip()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )
        return value

    def create(self, validated_data):
        user = super().create(validated_data)
        try:
            from apps.accounts.tasks import send_welcome_email
            send_welcome_email.delay(str(user.id))
        except Exception as e:
            logger.warning(f"Could not queue welcome email for {user.email}: {e}")
        return user


class UserSerializer(serializers.ModelSerializer):
    full_name    = serializers.ReadOnlyField()
    date_joined  = serializers.ReadOnlyField()

    class Meta:
        model  = User
        fields = (
            "id", "email", "first_name", "last_name", "full_name",
            "avatar", "phone", "date_joined",
        )
        read_only_fields = ("id", "email", "date_joined")


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ("first_name", "last_name", "phone", "avatar")