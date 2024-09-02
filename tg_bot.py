import logging
import traceback

from environs import Env
from google.cloud import dialogflow
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('bot_logger')

env = Env()
env.read_env()

PROJECT_ID = env.str('PROJECT_ID')
BOT_TOKEN = env.str('TOKEN')


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Здравствуйте')


def handle_dialog_flow(update: Update, context: CallbackContext):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, update.effective_chat.id)
    text_input = dialogflow.TextInput(text=update.message.text, language_code='Ru')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    context.bot.send_message(chat_id=update.effective_chat.id, text=response.query_result.fulfillment_text)


class TelegramLogsHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id
    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(text=log_entry, chat_id=self.chat_id)


def set_telegram_logger():
    bot = telegram.Bot(BOT_TOKEN)
    admin_chat_id = env.str('TG_ADMIN_CHAT_ID')
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(bot, admin_chat_id))
    return logger

def main():
    logger = set_telegram_logger()
    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dialog_flow_handler = MessageHandler(Filters.text & (~Filters.command), handle_dialog_flow)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(dialog_flow_handler)

    bot_start_log_message = 'tg_bot started'
    logging.info(bot_start_log_message)
    logger.info(bot_start_log_message)
    while True:
        try:
            updater.start_polling()
        except ConnectionError as connection_error:
            logging.error(f'Ошибка сети {connection_error}')
        except Exception:
            logger.error(f'Бот упал с ошибкой: {traceback.format_exc()}')

if __name__ == '__main__':
    main()