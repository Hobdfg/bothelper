from config import TOKEN
from sdamgia import SdamGIA
import telebot
from telebot import types

sdamgia = SdamGIA()
subject = 'math'
problems = {1: 1, 2: 2, 3: 4}
test_code = sdamgia.generate_test(subject, problems)
test_file_content = sdamgia.generate_pdf(subject, test_code)

bot = telebot.TeleBot(TOKEN)

with open('test.pdf', 'wb') as f:
    f.write(test_file_content)


@bot.message_handler(commands=['debug'])
def send_logs(message):
    with open("log_file.txt", "rb") as f:
        bot.send_document(message.chat.id, f)


@bot.message_handler(commands=['start'])
def send_test(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Математика')
    itembtn2 = types.KeyboardButton('Физика')
    markup.add(itembtn1, itembtn2)
    msg = bot.send_message(chat_id, "Выберите предмет теста:", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_subject(message):
    chat_id = message.chat.id
    subject = ''
    if message.text == 'Математика':
        subject = 'math'
    elif message.text == 'Физика':
        subject = 'physics'
    problems = {1: 1, 2: 2, 3: 4}
    test_code = sdamgia.generate_test(subject, problems)
    test_file_content = sdamgia.generate_pdf(subject, test_code)

    with open('test.pdf', 'wb') as f:
        f.write(test_file_content)

    with open('test.pdf', 'rb') as test_file:
        bot.send_document(chat_id, data=test_file)


bot.polling(non_stop=True)