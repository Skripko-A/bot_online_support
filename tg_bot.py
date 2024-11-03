from functools import partial
import logging
import traceback

from environs import Env
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import (Updater,
                          CommandHandler,
                          CallbackContext,
                          MessageHandler,
                          Filters)

from set_dialogflow import process_dialogflow_response
from tg_logger import set_telegram_logger


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text='Здравствуйте'
        )


def handle_dialog_flow(update: Update, context: CallbackContext, project_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(
        project_id, update.effective_chat.id
        )
    response = process_dialogflow_response(session_client, session, update.message.text)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response.query_result.fulfillment_text
        )


def main():
    env = Env()
    env.read_env()
    project_id = env.str('DIALOG_FLOW_PROJECT_ID')
    bot_token = env.str('TG_BOT_TOKEN')
    admin_chat_id = env.str('TG_ADMIN_CHAT_ID')

    logger = set_telegram_logger(
        bot_token=bot_token, admin_chat_id=admin_chat_id
        )
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
        )
    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dialog_flow_handler = MessageHandler(
        Filters.text & (~Filters.command),
        partial(handle_dialog_flow, project_id=project_id)
        )

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
