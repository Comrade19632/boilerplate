"""
Telegram login authentication functionality.
"""
import hashlib
import hmac
import time
from operator import itemgetter
from urllib.parse import parse_qsl

from django.conf import settings


class NotTelegramDataError(Exception):
    """
    The verification algorithm did not authorize Telegram data.
    """

    pass


class TelegramDataIsOutdatedError(Exception):
    """
    The Telegram data is outdated.
    """

    pass


ONE_DAY_IN_SECONDS = 86400


def verify_telegram_authentication(request_data):
    """
    Check if received data from Telegram is real.
    Based on SHA and HMAC algothims.
    Instructions - https://core.telegram.org/widgets/login#checking-authorization
    """

    request_data = request_data.copy()
    request_data = {k: v for k, v in request_data.items() if v is not None}

    bot_token = settings.TELEGRAM_BOT_TOKEN

    received_hash = request_data["hash"]
    auth_date = request_data["auth_date"]

    if request_data.get("init_data"):
        parsed_data = dict(parse_qsl(request_data.get("init_data")))

        parsed_data.pop("hash", None)

        data_check_string = "\n".join(
            f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
        )
        secret_key = hmac.new(
            key=b"WebAppData", msg=bot_token.encode(), digestmod=hashlib.sha256
        )
        _hash = hmac.new(
            key=secret_key.digest(),
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256,
        ).hexdigest()

    else:
        request_data.pop("hash", None)

        request_data_alphabetical_order = sorted(
            request_data.items(), key=lambda x: x[0]
        )

        data_check_string = []

        for data_pair in request_data_alphabetical_order:
            key, value = data_pair[0], data_pair[1]
            data_check_string.append(str(key) + "=" + str(value))

        data_check_string = "\n".join(data_check_string)

        secret_key = hashlib.sha256(bot_token.encode()).digest()
        _hash = hmac.new(
            secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256
        ).hexdigest()

    unix_time_now = int(time.time())
    unix_time_auth_date = int(auth_date)

    if unix_time_now - unix_time_auth_date > ONE_DAY_IN_SECONDS:
        raise TelegramDataIsOutdatedError(
            "Authentication data is outdated. Authentication was received more than day ago."
        )

    if _hash != received_hash:
        raise NotTelegramDataError(
            "This is not a Telegram data. Hash from recieved authentication data does not match"
            "with calculated hash based on bot token."
        )

    return request_data
