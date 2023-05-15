from django.conf import settings
from django.core.management.base import BaseCommand

from telegram.ext import Updater

from ...services.handlers.telegram_bot.menus import get_main_menu_builder
from ...services.handlers.telegram_bot.menus.submenu import get_submenu_menu_builder


class Command(BaseCommand):
    help = "Running manual telegram bot"

    def handle(self, *args, **kwargs):
        """инициализация бота"""
        updater = Updater(settings.TELEGRAM_BOT_TOKEN)

        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher

        # Add ConversationHandler to dispatcher that will be used for handling updates
        dispatcher.add_handler(get_main_menu_builder(command="start"))
        dispatcher.add_handler(get_submenu_menu_builder())

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()
