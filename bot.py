from io import BytesIO
from pprint import pprint

import requests
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters

import bot_config
from exif_reader import get_exif_data, get_location


def hello_world(bot, update):
    user_first_name = update.message.from_user.first_name

    update.message.reply_text(f"Hello, {user_first_name}")
    pprint(update.message.from_user.__dict__)


def reply_to_photo(bot, update):
    document = update.message['document']
    file_id = document['file_id']
    mime_type = document['mime_type']

    if not mime_type.startswith('image'):
        update.reply_text('Я понимаю только файлы с картинками')

    file_info_link = f'https://api.telegram.org/bot{bot_config.TOKEN}/getFile?file_id={file_id}'
    file_path = requests.get(file_info_link, proxies={'http': bot_config.HTTP_PROXY}).json()['result']['file_path']
    file_link = f'https://api.telegram.org/file/bot{bot_config.TOKEN}/{file_path}'
    file = requests.get(file_link,  proxies={'http': bot_config.HTTP_PROXY}).content
    file_data = BytesIO(file)
    exif_data = get_exif_data(file_data)
    lat, lon = get_location(exif_data)

    update.message.reply_text(f"Location info: {lat}, {lon}")


def main():
    my_bot = Updater(bot_config.TOKEN, request_kwargs={
        'proxy_url': bot_config.SOCKS_PROXY
    })

    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler('start', hello_world))
    dp.add_handler(MessageHandler(Filters.document, reply_to_photo))

    my_bot.start_polling()
    my_bot.idle()


if __name__ == '__main__':
    main()
