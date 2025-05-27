import os
from telebot import TeleBot, types

bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_app_button = types.KeyboardButton(
        text="Open Car Tinder",
        web_app=types.WebAppInfo(url="https://up-kiwi-informally.ngrok-free.app/?_ngrok_skip_browser_warning=true")
    )
    markup.add(web_app_button)
    bot.send_message(message.chat.id, f"Launch the Mini App id:", reply_markup=markup)
    
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message: types.Message):
    app_data: types.WebAppData = message.web_app_data
    id = message.sender_chat.id
    # prepared_message = bot.save_prepared_inline_message(
    #     user_id=id,
    #     result=types.InlineQueryResultBase(
    #         id=app_data.data,  # Use the data from the Mini App as the ID
    #         type='article',  # Specify the type of inline query result
    #         title='Received Data',
    #         input_message_content=types.InputTextMessageContent(
    #             message_text=f"Data received: {app_data.data}"
    #         )
    #     )
    # )
    data = app_data.data  # The string sent from the Mini App
    print(f"Received data from Mini App: {id}")
    bot.send_message(id, f"Received data from Mini App: {data}")
    
bot.polling(none_stop=True)