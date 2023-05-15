from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, ConversationHandler

from apps.telegram_bot.services.handlers.telegram_bot.menus.urls import MAIN_SUBMENU_URL, MAIN_URL


MAIN_SUBMENU_STAGE = 1


def submenu(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    keyboard = [
        [
            InlineKeyboardButton("Главное меню", callback_data=MAIN_URL),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text="Подменю",
        reply_markup=reply_markup,
    )
    return MAIN_SUBMENU_STAGE


def get_submenu_menu_builder():
    return ConversationHandler(
        entry_points=[CallbackQueryHandler(callback=submenu, pattern=MAIN_SUBMENU_URL)],
        states={MAIN_SUBMENU_STAGE: []},
        fallbacks=[CallbackQueryHandler(callback=submenu, pattern=MAIN_SUBMENU_URL)],
    )
