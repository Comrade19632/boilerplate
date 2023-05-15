from telegram import InlineKeyboardButton, InlineKeyboardMarkup, LoginUrl, Update, WebAppInfo
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, ConversationHandler

from apps.users.services import update_or_create_user

from ....require_channel_membership import require_channel_membership
from .urls import MAIN_SUBMENU_URL, MAIN_URL


MAIN_STAGE = 1


def get_main_reply_markup():
    keyboard = [
        [
            InlineKeyboardButton("Подменю", callback_data=MAIN_SUBMENU_URL),
        ],
        [
            InlineKeyboardButton(
                "Сайт", login_url=LoginUrl(url="https://test.domain/login/")
            ),
            InlineKeyboardButton(
                "Веб приложение в тг",
                web_app=WebAppInfo(url="https://test.domain/login/"),
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


@require_channel_membership
def main(update: Update, _: CallbackContext) -> int:
    """Send message on `/start`."""
    update_or_create_user(update.message.from_user.to_dict())
    update.message.reply_text("Главное меню", reply_markup=get_main_reply_markup())
    return MAIN_STAGE


@require_channel_membership
def return_to_main(update: Update, context: CallbackContext) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    update_or_create_user(query.from_user.to_dict())
    query.edit_message_text(text="Главное меню", reply_markup=get_main_reply_markup())
    return MAIN_STAGE


def get_main_menu_builder(command):
    return ConversationHandler(
        entry_points=[
            CommandHandler(command, main),
            CallbackQueryHandler(callback=return_to_main, pattern=MAIN_URL),
        ],
        states={MAIN_STAGE: []},
        fallbacks=[
            CommandHandler(command, main),
            CallbackQueryHandler(callback=return_to_main, pattern=MAIN_URL),
        ],
    )
