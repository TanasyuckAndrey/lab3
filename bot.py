import telebot
import config
import psycopg2

conn = psycopg2.connect(host="localhost", port = 5432, database="test", user="postgres", password="05021976")
cur = conn.cursor()
print("Database opened successfully")

class BD1:

    def ss():
        cur.execute("""SELECT * from t_order o, t_executor e
where o.id_order = e.id_order and e.id_person = 1 and
to_timestamp('2021.02.21 12:30:00','YYYY.MM.DD HH24:MI:SS') between date_begin and coalesce(date_end,clock_timestamp())""")
        query_results = cur.fetchall()
        text = '\n\n'.join([', '.join(map(str, x)) for x in query_results])
        return (str(text))      
 
from telebot import types
 
bot = telebot.TeleBot(config.TOKEN)
 
@bot.message_handler(commands=['start'])
def welcome(message):

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Создать заявку")
    item2 = types.KeyboardButton("Доступные наряды")
 
    markup.add(item1, item2)
 
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный для тестирования проекта.".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup)
 
@bot.message_handler(content_types=['text'])
def Soobsh(message):
    if message.chat.type == 'private':
        if message.text == 'Создать заявку':
            bot.send_message(message.chat.id, "В разработке")
        elif message.text == 'Доступные наряды':
 
            markup = types.InlineKeyboardMarkup(row_width=4)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
 
            markup.add(item1, item2)
 
            bot.send_message(message.chat.id, BD1.ss(),  reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Неизвестная команда')
 
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает 😢')
 
            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Спасибо за выбор",
                reply_markup=None)
 
            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")
 
    except Exception as e:
        print(repr(e))
 
# RUN
bot.polling(none_stop=True)