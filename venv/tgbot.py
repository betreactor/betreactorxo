from functions import *
import telebot
import config
token = tgtoken


bot = telebot.TeleBot(token)

# @bot.message_handler(content_types=["text"])
# def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
#     bot.send_message(message.chat.id, message.text)

course = usd_rates()

print(course[0])

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'btc':
        bot.send_message(message.chat.id, btc_usd())
        bot.send_message(message.chat.id, usd_rates())
        bot.send_message(message.chat.id, 'hjhj')


if __name__ == '__main__':
     bot.polling(none_stop=True)