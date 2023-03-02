import logging
import telebot
import json
from functools import wraps
from libs import is_known_username
import openai

API_TOKEN = os.environ['TELEGRAM_TOKEN']
OPENAI_API = os.environ['OPENAI_API']
OPENAI_ORG = os.environ['OPENAI_ORG']

openai.organization = OPENAI_ORG
openai.api_key = OPENAI_API

def private_access():

    def deco_restrict(f):

        @wraps(f)
        def f_restrict(message, *args, **kwargs):
            username = message.from_user.username

            if is_known_username(username):
                return f(message, *args, **kwargs)
            else:
                pass
        return f_restrict
    return deco_restrict


def process_event(event):

    request_body_dict = json.loads(event['body'])
    update = telebot.types.Update.de_json(request_body_dict)
    bot.process_new_updates([update])


def lambda_handler(event, context):
    process_event(event)
    return {
        'statusCode': 200
    }

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN, threaded=False)

@bot.message_handler(commands=['chat'])
@private_access()
def chat_gpt(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message.text}
        ]
    )

    response = response['choices'][0]['message']['content']
    bot.reply_to(message, parse_mode='markdown', response)