from functions import *
import telebot
import schedule
import config
token = tgtoken
import sched, time

bot = telebot.TeleBot(token)

# @bot.message_handler(content_types=["text"])
# def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
#     bot.send_message(message.chat.id, message.text)




x = 9500







# @bot.message_handler(content_types=['text'])
# def send_text(message):
#     if message.text.lower() == 'btc':
#         bot.send_message(message.chat.id, btc_usd())


# def msg(message):
# bot.send_message(message.chat.id, 'OVER!')
# print('jjj')

# schedule.every().day.at("00:48").do(msg)
# while True:
#     schedule.run_pending()
#     time.sleep(1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    bot.send_message(message.chat.id, 'кукукуку Катя')
#
#
# s = sched.scheduler(time.time, time.sleep)
# def do_something(sc):
#     @bot.message_handler(content_types=['text'])
#     def send_text(message):
#         if x <= 19000:
#             bot.send_message(message.chat.id, 'OVER 9407!')
#             s.enter(5, 1, do_something, (sc,))
#
# s.enter(5, 1, do_something, (s,))
# s.run()
#
#
if __name__ == '__main__':
     bot.polling(none_stop=True)


