from django.contrib.auth import get_user_model

import pytz
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "telegram_id",
            "username",
            "first_name",
            "photo_url",
        )
