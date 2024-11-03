import logging
import random
import traceback

from environs import Env
from google.cloud import dialogflow
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from set_dialogflow import process_dialogflow_response
from tg_logger import set_telegram_logger


def handle_dialog_flow(event, vk_api, project_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, event.user_id)
    response = process_dialogflow_response(
        session_client, session, event.text
    )

    if not response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


def main():
    env = Env()
    env.read_env()
    project_id = env.str('DIALOG_FLOW_PROJECT_ID')
    tg_bot_token = env.str('TG_BOT_TOKEN')
    admin_chat_id = env.str('TG_ADMIN_CHAT_ID')

    logger = set_telegram_logger(
        bot_token=tg_bot_token, admin_chat_id=admin_chat_id
        )
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
        )
    vk_api_key = env.str('VK_API_KEY')
    vk_bot_start_log_message = 'vk_bot started'
    while True:
        try:
            vk_session = vk.VkApi(token=vk_api_key)
            vk_api = vk_session.get_api()
            longpoll = VkLongPoll(vk_session)
            logging.info(vk_bot_start_log_message)
            logger.info(vk_bot_start_log_message)

            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    handle_dialog_flow(event, vk_api, project_id)

        except ConnectionError as connection_error:
            logging.error(f'Ошибка сети {connection_error}')

        except TimeoutError as timeout_error:
            logging.error(
                f'Превышено время ожидания {timeout_error.with_traceback}'
                )
        except Exception:
            logger.error(f'Бот упал с ошибкой: {traceback.format_exc()}')


if __name__ == "__main__":
    main()
