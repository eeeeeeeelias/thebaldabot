# -*- coding: utf-8 -*-
import random
import config
import telebot
import shelve

bot = telebot.TeleBot(config.token)



def get_random_word(message):
	words = [key for key in config.user_vocabs[message.chat.id]]
	print(words)
	config.now_word[message.chat.id] = random.choice(words)
	print(config.now_word)
	return config.now_word[message.chat.id]

def send_random_word(message):
	bot.send_message(message.chat.id, get_random_word(message) + " " + str(message.chat.id))
	config.waiting_for_answer = True

@bot.message_handler(func=lambda call: config.debugging)	
def debug(message):
    bot.send_message(message.chat.id, "Идёт отладка.")	
	
@bot.message_handler(regexp="/start")	
def new_user(message):
	config.user_ids[str(message.chat.id)] = "0"
	d = shelve.open(str(message.chat.id))
	config.user_vocabs[message.chat.id] = d
	config.user_vocabs[message.chat.id]['close-up'] = 'крупный план'
	config.user_vocabs[message.chat.id]['carrot'] = 'морковь'
	config.user_vocabs[message.chat.id]['indigenous'] = 'туземный'
	config.user_vocabs[message.chat.id]['dormitory'] = 'общежитие'
	config.user_vocabs[message.chat.id]['phone'] = 'телефон'
	config.user_vocabs[message.chat.id]['glacier'] = 'ледник'

@bot.message_handler(regexp="/add*")
def add_word(message):
	pair = message.text[5:].split(", ")
	config.user_vocabs[message.chat.id][pair[0]] = pair[1]
	print(config.user_vocabs[message.chat.id])
	bot.send_message(message.chat.id, "Слово успешно добавлено.")
	
	
@bot.message_handler(regexp="/newgame")
def	new_game(message):
	send_random_word(message)
	config.game_is_now = True

@bot.message_handler(regexp="/endgame")
def stop_game(message):
	config.waiting_for_answer = False
	config.game_is_now = False
	config.now_word[message.chat.id] = ""

@bot.message_handler(func=lambda call: config.waiting_for_answer)
def check_answer(message):
	if message.text == "/pass":
		bot.send_message(message.chat.id, "Потом вспомнишь.")
	elif config.user_vocabs[message.chat.id][config.now_word[message.chat.id]] == message.text:
		bot.send_message(message.chat.id, "Молодец!")
	else:
		bot.send_message(message.chat.id, "Ну так себе.")
	config.waiting_for_answer = False
	send_random_word(message)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, "Что-то пошло не так!")

if __name__ == '__main__':
     bot.polling(none_stop=True)
	 
config.user_ids.close()