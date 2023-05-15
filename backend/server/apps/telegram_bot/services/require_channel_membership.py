from django.conf import settings

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.chatmember import ChatMember


def require_channel_membership(func):
    def wrapper(update, context):
        if update.message:
            user_id = update.message.from_user.id
        else:
            query = update.callback_query
            query.answer()
            user_id = query.from_user.id
        member = context.bot.get_chat_member(
            chat_id=settings.TG_NEWS_CHANNEL_ID, user_id=user_id
        )
        if (
            member.status == ChatMember.ADMINISTRATOR
            or member.status == ChatMember.CREATOR
            or member.status == ChatMember.MEMBER
        ):
            return func(update, context)
        else:
            keyboard = [
                [InlineKeyboardButton("Подписаться", url="https://t.me/ваш_канал")],
                [InlineKeyboardButton("Проверить подписку", callback_data="main/_url")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(
                user_id,
                "Для использования бота, пожалуйста, подпишитесь на наш канал.",
                reply_markup=reply_markup,
            )

    return wrapper
