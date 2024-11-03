import logging

from google.cloud import dialogflow


def process_dialogflow_response(session_client, session, user_message_text):
    logging.info(f"Session path: {session}")
    text_input = dialogflow.TextInput(
        text=user_message_text, language_code='Ru'
        )
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response
