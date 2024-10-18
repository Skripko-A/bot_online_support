import json

from environs import Env
from google.api_core.exceptions import BadRequest
from google.cloud import dialogflow
import logging


logger = logging.getLogger('bot_logger')

def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    logging.info(message_texts)
    text = dialogflow.Intent.Message.Text(text=[message_texts])
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    logging.info("Intent created: {}".format(response))


def load_typical_phrases(filename):
    with open(filename, 'r') as file:
        questions_json = file.read()
    return json.loads(questions_json)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
    env = Env()
    env.read_env()
    project_id = env.str('PROJECT_ID')
    typical_phrases = load_typical_phrases('questions.json')
    for key in typical_phrases.keys():
        display_name = key
        try:
            create_intent(
                project_id=project_id,
                display_name=display_name,
                training_phrases_parts=typical_phrases[display_name]['questions'],
                message_texts=typical_phrases[display_name]['answer'])
        except BadRequest as bad_request_error:
            logging.error(bad_request_error)