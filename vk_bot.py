import logging
import random
import traceback

from environs import Env
from google.cloud import dialogflow
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from tg_bot import set_telegram_logger


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

env = Env()
env.read_env()

PROJECT_ID = env.str('PROJECT_ID')


def handle_dialog_flow(event, vk_api):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, event.user_id)
    logging.info(f"Session path: {session}")
    text_input = dialogflow.TextInput(text=event.text, language_code='Ru')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})

    if not response.query_result.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response.query_result.fulfillment_text,
            random_id=random.randint(1,1000)
        )


def main():
    logger = set_telegram_logger()
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
                    handle_dialog_flow(event, vk_api)
        except ConnectionError as connection_error:
            logging.error(f'Ошибка сети {connection_error}')
        except TimeoutError as timeout_error:
            logging.error(f'Превышено время ожидания {timeout_error.with_traceback}')
        except Exception:
            logger.error(f'Бот упал с ошибкой: {traceback.format_exc()}')



if __name__ == "__main__":
    main()