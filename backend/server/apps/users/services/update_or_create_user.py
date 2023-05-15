from funcy import first

from apps.users.models import User


def get_defaults(data):
    defaults = {}
    if username := data.get("username"):
        defaults["username"] = username
    if first_name := data.get("first_name"):
        defaults["first_name"] = first_name
    if photo_url := data.get("photo_url"):
        defaults["photo_url"] = photo_url
    return defaults


def update_or_create_user(data):
    return first(
        User.objects.update_or_create(
            telegram_id=data["id"], defaults=get_defaults(data)
        )
    )
