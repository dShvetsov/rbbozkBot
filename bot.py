#!/bin/python3
from random import randint
import telebot
import json
from mytoken import TOKEN, password

BOT_TOKEN = TOKEN()

URL = "https://api.telegram.org/bot%s" % BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)


d = json.load(open('./dict.dmp'))
ret = None

state = 'init'

def getUnread():
    global d
    unread = [ x if d[x]  == 'no' else None for x in d ]
    filter( lambda x : x is not None , unread )
    n = randint(0, len(unread) - 1)
    return unread[ n ]

@bot.message_handler(content_types=["text"])
def handler(message):
   global  state, ret
   if (message.text == 'get') :
        ret = getUnread()
        print (ret)
        state = "expect result"
        bot.send_message(message.chat.id, ret)
   elif state == "expect result" :
        if message.text == 'done' : 
            d[ret] = 'yes'

if __name__ == '__main__':
    bot.polling(none_stop=True)
