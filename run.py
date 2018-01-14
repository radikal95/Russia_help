import telebot
import config
from db_tool import DbQuery
db_query = DbQuery()

bot = telebot.TeleBot(config.token)

def login_check(message):
    query = """SELECT full_name,auth,id
    	        FROM public."user"
                WHERE id={};"""
    query_result = db_query.execute_query(query.format(message.chat.id))
    return query_result.value[0][1]

@bot.message_handler(commands=['start'])
def insert_into_a_db(message):
    query = """SELECT full_name,auth,id
	        FROM public."user"
            WHERE id={};"""
    query_result=db_query.execute_query(query.format(message.chat.id))
    if len(query_result.value)<1:
        query ="""INSERT INTO public."user"(full_name,
                                        auth,
                                        id)
	                                    VALUES ('{}', False, {});"""
        name = 'Unknown user'
        if message.chat.first_name:
            name = str(message.chat.first_name)
        if message.chat.last_name:
            name = name + ' ' + str(message.chat.first_name)
        query_result=db_query.execute_query(query.format(name,message.chat.id),is_dml=True)
        if (query_result.success):
            bot.send_message(message.chat.id, "So, tell us the key")
    else:
        if not query_result.value[0][1]:
            bot.send_message(message.chat.id, "Tell us the key")
        else:
            bot.send_message(message.chat.id, """/security - security information \n
/information - general information \n
/travel - accommodation, logistics, visas, taxis \n
/entertainment - info on local entertainment""")

@bot.message_handler(regexp=config.secret_key)
def login(message):
    query = """SELECT full_name,auth,id
    	        FROM public."user"
                WHERE id={};"""
    query_result = db_query.execute_query(query.format(message.chat.id))
    if not query_result.value[0][1]:
        query = """UPDATE public."user"
                SET auth = True
                WHERE id={};"""
        query_result=db_query.execute_query(query.format(message.chat.id),is_dml=True)
        if query_result.success:
            bot.send_message(message.chat.id, """You are logged in! \n
/security - security information \n
/information - general information \n
/travel - accommodation, logistics, visas, taxis \n
/entertainment - info on local entertainment""")
    else:
        bot.send_message(message.chat.id, """/security - security information \n
/information - general information \n
/travel - accommodation, logistics, visas, taxis \n
/entertainment - info on local entertainment""")

@bot.message_handler(func=lambda message: login_check(message))
def dialog(message):
    if message.text == '/security':
        bot.send_message(message.chat.id, "security information")
    elif message.text == '/information':
        bot.send_message(message.chat.id, "general information")
    elif message.text == '/travel':
        bot.send_message(message.chat.id, "accommodation, logistics, visas, taxis")
    elif message.text == '/entertainment':
        bot.send_message(message.chat.id, "on local entertainment")
    else:
        bot.send_message(message.chat.id, "Can't find such command")

@bot.message_handler(content_types='text')
def default_answer(message):
    bot.send_message(message.chat.id, "You are not authorized")


while True:
    bot.polling(none_stop=True)
