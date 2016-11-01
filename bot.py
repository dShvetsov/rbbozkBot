#!/bin/python3
from random import randint
import telebot
import json
from mytoken import TOKEN, password

BOT_TOKEN = TOKEN()

URL = "https://api.telegram.org/bot%s" % BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

def check(pswd) :
    return pswd == password() # TODO hash password

d = json.load(open('./dict.dmp'))
ret = None

state = 'init'

users = {}
count = 0

def getUnread():
    global d
    unread = [ x if d[x]  == 'no' else None for x in d ]
    unread = list( filter( lambda x : x is not None , unread ))
    n = randint(0, len(unread) - 1)
    return unread[ n ]

@bot.message_handler(content_types=["text"])
def handler(message):
    user_id = message.chat.id
    global  state, ret, users, d, count
    if not user_id in users.keys():
        users[user_id] = "untrusted"
        bot.send_message(user_id, "Hello,  please input password")
        print ("new users detected, waiting password")
        return
    elif users[user_id] == 'untrusted' :
        if check(message.text) :
            users[user_id] = 'trusted'
            bot.send_message(user_id, "Welcome")
            print ("user accepted")
            return
        else :
            bot.send_message(user_id, "Wrong password, try again")
            print ("wrong password")
            return
    elif users[user_id] != 'trusted' :
        print ("error")
        return

    if (message.text.lower() == 'get') :
        ret = getUnread()
        print (ret)
        state = "expect result"
        bot.send_message(user_id, ret)
    elif state == "expect result" :
        if message.text.lower() == 'done' :
            d[ret] = 'yes'
            print (ret + " done")
            bot.send_message(user_id, "ok, you read this message")
            count += 1
            if count > 10 :
                json.dump(d, open('./dict.dmp','w'))
                count = 0
        elif message.text.lower() == 'repeat' :
            bot.send_message(user_id, ret)

    if message.text.lower() == 'dump' :
        json.dump(d, open('./dict.dmp', 'w'))
        print ("dumped")
        bot.send_message(user_id, "file dumped")

    if message.text.lower() == 'ping' :
        bot.send_message(user_id, 'pong')

    if message.text.lower() == 'count' :
        unread = [ x if d[x]  == 'no' else None for x in d ]
        unread = list( filter( lambda x : x is not None , unread ) )
        bot.send_message(user_id, "count is : " + str(len(unread)))

if __name__ == '__main__':
     bot.polling(none_stop=True)
