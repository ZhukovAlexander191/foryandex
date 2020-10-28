import telebot
from telebot import types
import requests
import json
import urllib

url = f"https://api.telegram.org/bot{token}/"
bot = telebot.AsyncTeleBot(token=token, threaded=False, skip_pending=False)
data = {}


def users_in(file_name, users):
    with open(file_name, 'w') as f:
        f.write(json.dumps(users))


def feedback_in(file_name, users):
    with open(file_name, 'w') as f:
        f.write(json.dumps(users, ensure_ascii=False))


def users_out(file_name):
    with open(file_name, 'r') as f:
        users = json.loads(str(f.read()))
        return users


@bot.message_handler(commands=['start'])
def welcome_start(message):
    if not IsBaned(message):
        users = users_out('users.json')
        if message.chat.id not in users[0]:
            bot.send_message(message.chat.id, kick)
            bot.send_message(message.chat.id, vanish)
            users[0].append(message.chat.id)
            user = {}
            user['username'] = message.from_user.username
            users.append(user)
            bot.send_message(sheluha,
                             'Привет, хозяин и два ! ' + str(
                                 message.from_user.first_name) + ' использовал команду /start')
            users_in('users.json', users)
            keyboard = types.InlineKeyboardMarkup()
            key_eng = types.InlineKeyboardButton(text='ENGLISH',
                                                 callback_data='eng')
            keyboard.add(key_eng)
            key_rus = types.InlineKeyboardButton(text='РУССКИЙ',
                                                 callback_data='rus')
            keyboard.add(key_rus)
            bot.send_message(message.from_user.id,
                             text=" Привет/Hi\n Выберите язык бота/Choose the language of the bot:",
                             reply_markup=keyboard)
            users_in('users.json', users)
        else:  # надо сделать хуйню с привязкой юзера к языку, а здесь дать возможность поменять, чтобы постоянно не дрочило его этой хуйней2
            if 'rus' in users[users[0].index(message.chat.id) + 2].values():
                keyboard = types.InlineKeyboardMarkup()
                key_eng = types.InlineKeyboardButton(text='YES',
                                                     callback_data='eng')
                keyboard.add(key_eng)
                key_rus = types.InlineKeyboardButton(text='NO', callback_data='rus')
                keyboard.add(key_rus)
                bot.send_message(message.from_user.id,
                                 text="Вы хотите поменять язык бота на английский?",
                                 reply_markup=keyboard)
            else:  # я ебучий гений)
                keyboard = types.InlineKeyboardMarkup()
                key_eng = types.InlineKeyboardButton(text='YES',
                                                     callback_data='rus')
                keyboard.add(key_eng)
                key_rus = types.InlineKeyboardButton(text='NO', callback_data='eng')
                keyboard.add(key_rus)
                bot.send_message(message.from_user.id,
                                 text="Do you want to switch the language of the bot to Russian?",
                                 reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    users = users_out('users.json')
    if call.data == "eng":
        users[users[0].index(call.message.chat.id) + 2]['lng'] = 'eng'
        bot.send_message(call.message.chat.id, "You've chosen the English language")
    elif call.data == "rus":
        users[users[0].index(call.message.chat.id) + 2]['lng'] = 'rus'
        bot.send_message(call.message.chat.id, 'Вы выбрали русский язык')
    users_in('users.json', users)
    if call.data == "yes":
        if 'срочно' in data[str(call.message.chat.id)][3].lower() \
                or "immediately" in data[str(call.message.chat.id)][3].lower():
            bot.forward_message(sro4no, call.message.chat.id,
                                data[str(call.message.chat.id)][4])
            bot.send_message(sro4no,
                             f'  ID: {data[str(call.message.chat.id)][0]}\n ВУЗ: {data[str(call.message.chat.id)][1]}\n'
                             f' Предмет: {data[str(call.message.chat.id)][2]}\n'
                             f' Срок:{data[str(call.message.chat.id)][3]}\n ')
        else:
            bot.forward_message(pinaem, call.message.chat.id,
                                data[str(call.message.chat.id)][4])
            bot.send_message(pinaem,
                             f'  ID: {data[str(call.message.chat.id)][0]}\n ВУЗ: {data[str(call.message.chat.id)][1]}\n'
                             f' Предмет: {data[str(call.message.chat.id)][2]}\n'
                             f' Срок:{data[str(call.message.chat.id)][3]}\n ')
        bot.send_message(call.message.chat.id,
                         "Ваш запрос был успешно отправлен. В ближайшее время вы получите информацию по цене и сроку выполнения задания")
    elif call.data == "no":
        if users[users[0].index(call.message.chat.id) + 2]['lng'] == 'rus':
            bot.send_message(call.message.chat.id,
                             ' Какой пункт заявки необходимо исправить?\n 1 - ВУЗ\n 2 - Предмет\n 3 - Срок\n 4 - Задание')
        else:
            bot.send_message(call.message.chat.id,
                             " Which section of the request is have to be changed?\n 1 - University name\n 2 - Subject\n 3 - Deadline\n 4 - Task")
        bot.register_next_step_handler(call.message, correct)


@bot.message_handler(commands=['help'])
def welcome_help(message):
    if not IsBaned(message):
        users = users_out('users.json')
        if users[users[0].index(message.chat.id) + 2]['lng'] == 'rus':
            bot.send_message(message.chat.id, instruction)
        else:
            bot.send_message(message.chat.id, engstruction)
        bot.send_message(sheluha,
                         'Привет, хозяин и два ! ' + str(
                             message.from_user.first_name) + ' использовал команду /help')


@bot.message_handler(commands=['pay'])
def pay(message):
    if not IsBaned(message):
        users = users_out('users.json')
        if users[users[0].index(message.chat.id) + 2]['lng'] == 'rus':
            bot.send_message(message.chat.id, "")
        else:
            bot.send_message(message.chat.id,
                             "")
        bot.send_message(sheluha,
                         'Привет, хозяин и два ! ' + str(
                             message.from_user.first_name) + ' использовал команду /pay')


@bot.message_handler(commands=['feedback'])
def feedback(message):
    if not IsBaned(message):
        users = users_out('users.json')
        if users[users[0].index(message.chat.id) + 2]['lng'] == 'rus':
            bot.send_message(message.chat.id,
                             'Здесь Вы можете оставить свои отзывы и предложения по поводу работы сервиса.\n   Пожалуйста, пишите всё одним сообщением!\n'
                             f'{ext}')
        else:
            bot.send_message(message.chat.id,
                             "Here you can leave your feedback and suggestions about working of the service\n"
                             "Please write all in one message!\n"
                             f"{ext}")
        bot.register_next_step_handler(message, feed)


@bot.message_handler(commands=["price"])
def price(message):
    if not IsBaned(message):
        users = users_out('users.json')
        if users[users[0].index(message.chat.id) + 2]['lng'] == 'rus':
            bot.send_message(message.chat.id,
                             "Ваш запрос был успешно получен. В ближайшее время мы Вам ответим")
        else:
            bot.send_message(message.chat.id,
                             "Your request has been successfully received. We will answer you in a short time")
        bot.forward_message(tuporezi, message.chat.id, message.message_id)
        bot.send_message(tuporezi, message.chat.id)


@bot.message_handler(commands=['client'])
def client(message):
    if message.from_user.username in usernames:
        bot.register_next_step_handler(message, client_add)


@bot.message_handler(commands=['task'])
def exercise(message):
    if not IsBaned(message):
        users = users_out('users.json')
        bot.send_message(sheluha,
                         'Привет, хозяин и двf ' + str(
                             message.from_user.first_name) + ' использовал команду /task')
        if users[users[0].index(message.chat.id) + 2]['lng'] == 'rus':
            bot.send_message(message.chat.id,
                             'Для того, чтобы оставить заявку на выполнение задания, необходимо сначала заполнить несколько полей\n'
                             'Введите название вашего университета (необязательно, можно поставить прочерк)\n'
                             f'{ext}')
        else:
            bot.send_message(message.chat.id,
                             'To send a reguest for completion of the task, you have to fill in a few fields at first\n'
                             'Enter the name of your university (not obligatory, you may leave a dash)\n'
                             f'{engext}')
        data[str(message.chat.id)] = []
        data[str(message.chat.id)].append(message.chat.id)
        bot.register_next_step_handler(message, university)


@bot.message_handler(commands=['send'])
def working(message):
    if message.from_user.username in usernames:
        try:
            bot.register_next_step_handler(message, process_mind)
        except:
            bot.send_message(message.chat.id,
                             "Что-то пошло не так!", parse_mode='HTML')
    else:
        bot.send_message(message.chat.id,
                         'Вы не являетесь администратором для выполнения этой команды!')


@bot.message_handler(commands=['photo'])
def working(message):
    if message.from_user.username in usernames:
        try:
            bot.register_next_step_handler(message, sender)
        except:
            bot.send_message(message.chat.id,
                             "Что-то пошло не так!", parse_mode='HTML')
    else:
        bot.send_message(message.chat.id,
                         'Вы не являетесь администратором для выполнения этой команды!')


@bot.message_handler(content_types=["sticker", "document", "audio", "photo", "voice", "video"])
def messages(message):
    if not IsBaned(message):
        try:
            bot.forward_message(tuporezi, message.chat.id, message.message_id)
        except:
            bot.send_message(tuporezi,
                             'Что-то пошло не так! Бот продолжил свою работу.')


@bot.message_handler(commands=['ban'])
def ban(message):
    if message.from_user.username in usernames:
        bot.register_next_step_handler(message, banforgay)


@bot.message_handler(content_types=["text"])
def messages(message):
    if not IsBaned(message):
        print(f"{message.from_user.username} : ", message.text)
        try:
            bot.forward_message(tuporezi, message.chat.id, message.message_id)
        except:
            bot.send_message(tuporezi,
                             'Что-то пошло не так! Бот продолжил свою работу.')


def process_mind(message):
    if message.from_user.username in usernames:
        try:
            text = 'Сообщение было отправлено пользователю ' + str(
                message.reply_to_message.forward_from.first_name)
            bot.send_message(message.reply_to_message.forward_from.id,
                             f"GOD: {message.text}")
            bot.send_message(tuporezi, text)
        except:
            bot.send_message(message.chat.id,
                             'Что-то пошло не так! Бот продолжил свою работу.',
                             parse_mode='HTML')
    else:
        bot.send_message(message.chat.id,
                         'Вы не являетесь администратором для выполнения этой команды!')


def client_add(message):
    clients = users_out('client.json')
    try:
        idus = str(message.reply_to_message.forward_from.id)
        money = message.text
        if idus not in clients[message.from_user.username].keys():
            clients[message.from_user.username][idus] = []
            clients[message.from_user.username][idus].append(money)
        else:
            clients[message.from_user.username][idus].append(money)
        bot.send_message(sheluha, f'Обманули {message.reply_to_message.forward_from.username} на 4 кулака')
    except:
        bot.send_message(message.chat.id,
                         'Что-то пошло не так! Бот продолжил свою работу.',
                         parse_mode='HTML')
    users_in('client.json', clients)


def banforgay(message):
    users = users_out('users.json')
    try:
        users[1].append(str(message.reply_to_message.forward_from.id))
        bot.send_message(message.reply_to_message.forward_from.id, 'Вы были заблокированы!')
        bot.send_message(sheluha, f'{message.reply_to_message.forward_from.id} был добавлен в список пидорасов')
    except:
        bot.send_message(message.chat.id,
                         'Что-то пошло не так! Бот продолжил свою работу.',
                         parse_mode='HTML')
    users_in('users.json', users)


def IsBaned(message):
    users = users_out('users.json')
    return str(message.chat.id) in users[1]


def sender(message):
    if message.from_user.username in usernames:
        try:
            text = 'Сообщение было отправлено пользователю ' + str(
                message.reply_to_message.forward_from.first_name)
            bot.send_photo(message.reply_to_message.forward_from.id,
                           open(f'{message.text}', "rb"))
            bot.send_message(tuporezi, text)
        except:
            bot.send_message(message.chat.id,
                             'Что-то пошло не так! Бот продолжил свою работу.',
                             parse_mode='HTML')
    else:
        bot.send_message(message.chat.id,
                         'Вы не являетесь администратором для выполнения этой команды!')


def university(message):
    users = users_out('users.json')
    if message.text != "/exit":
        data[str(message.chat.id)].append(message.text)
        if users[users[0].index(message.chat.id) + 2]['lng'] == 'rus':
            bot.send_message(message.chat.id, 'Введите предмет\n'
                                              f'{ext}')
        else:
            bot.send_message(message.chat.id, "Enter the subject\n"
                                              f"{engext}")
        bot.register_next_step_handler(message, expiration_date)
    else:
        exit(message)


def expiration_date(message):
    users = users_out('users.json')
    if message.text != "/exit":
        data[str(message.chat.id)].append(message.text)
        if users[users[0].index(message.chat.id) + 2]['lng'] == 'rus':
            bot.send_message(message.chat.id,
                             'Введите срок выполнения задания\n'
                             'Если ответ необходим в ближайшее время, напишите дату и слово СРОЧНО\n'
                             'Например, *05/10 СРОЧНО*'
                             f'{ext}')
        else:
            bot.send_message(message.chat.id, 'Enter the deadline for the task\n'
                                              'If you need the answer in a short time, write date and the word IMMEDIATELY\n'
                                              'For example, *05/10 IMMEDIATELY*'
                                              f'{engext}')
        bot.register_next_step_handler(message, task)
    else:
        exit(message)


def task(message):
    users = users_out('users.json')
    if message.text != "/exit":
        data[str(message.chat.id)].append(message.text)
        if users[users[0].index(message.chat.id) + 2]['lng'] == 'rus':
            bot.send_message(message.chat.id,
                             "Прикрепите условие задания\n"
                             f"{ext}")
        else:
            bot.send_message(message.chat.id,
                             "Send the task itself\n"
                             f"{engext}")
        bot.register_next_step_handler(message, ok)
    else:
        exit(message)


def ok(message):
    users = users_out('users.json')
    if message.text != '/exit':
        if len(data[str(message.chat.id)]) == 4:
            data[str(message.chat.id)].append(message.message_id)
        if users[users[0].index(message.chat.id) + 2]['lng'] == 'rus':
            bot.send_message(message.chat.id,
                             f' ВУЗ: {data[str(message.chat.id)][1]}\n Предмет: {data[str(message.chat.id)][2]}\n'
                             f' Срок:{data[str(message.chat.id)][3]}\n Задание :')
        else:
            bot.send_message(message.chat.id,
                             f' University: {data[str(message.chat.id)][1]}\n Subject: {data[str(message.chat.id)][2]}\n'
                             f' Deadline: {data[str(message.chat.id)][3]}\n Task :')
        bot.forward_message(message.chat.id, message.chat.id,
                            data[str(message.chat.id)][4])
        bot.send_message(message.chat.id, '')
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='ДА/YES', callback_data='yes')
        keyboard.add(key_yes)
        key_no = types.InlineKeyboardButton(text='НЕТ/NO', callback_data='no')
        keyboard.add(key_no)
        if users[users[0].index(message.chat.id) + 2]['lng'] == 'rus':
            bot.send_message(message.from_user.id,
                             text="Заявка заполнена корректно?",
                             reply_markup=keyboard)
        else:
            bot.send_message(message.from_user.id,
                             text="Is the request filled correctly?",
                             reply_markup=keyboard)
    else:
        exit(message)


def correct(message):
    users = users_out('users.json')
    if message.text not in ['1', '2', '3', '4']:
        if users[users[0].index(message.chat.id) + 2]['lng'] == 'rus':
            bot.send_message(message.chat.id,
                             " 1 - ВУЗ\n 2 - Предмет\n 3 - Срок\n 4 - Задание")
        else:
            bot.send_message(message.chat.id,
                             " 1 - University\n 2 - Subject\n 3 - Deadline\n 4 - Task")
        bot.register_next_step_handler(message, correct)
    else:
        if message.text == '2':
            if users[users[0].index(message.chat.id) + 2]['lng'] == 'rus':
                bot.send_message(message.chat.id, 'Введите предмет\n'
                                                  f'{ext}')
            else:
                bot.send_message(message.chat.id, "Enter the subject"
                                                  f"{engext}")
            bot.register_next_step_handler(message, dolbaeb)
        elif message.text == '3':
            if users[users[0].index(message.chat.id) + 2]['lng'] == 'rus':
                bot.send_message(message.chat.id, 'Введите срок выполнения задания\n'
                                                  f'{ext}')
            else:
                bot.send_message(message.chat.id, "Enter the deadline for the task"
                                                  f"{engext}")
            bot.register_next_step_handler(message, eblan)
        elif message.text == '4':
            if users[users[0].index(message.chat.id) + 2]['lng'] == 'rus':
                bot.send_message(message.chat.id,
                                 'Прикрепите условие задания\n'
                                 f'{ext}')
            else:
                bot.send_message(message.chat.id,
                                 "Send the task itself"
                                 f"{engext}")
            bot.register_next_step_handler(message, kon4)
        elif message.text == '1':
            if users[users[0].index(message.chat.id) + 2]['lng'] == 'rus':
                bot.send_message(message.chat.id, 'Введите название вашего университета\n'
                                                  f'{ext}')
            else:
                bot.send_message(message.chat.id, "Enter the name of your university\n"
                                                  f"{engext}")
            bot.register_next_step_handler(message, vegetable)


def dolbaeb(message):
    if message.text != "/exit":
        data[str(message.chat.id)][2] = message.text
        bot.send_message(message.chat.id, "Вы готовы проверить анкету ещё раз?\n"
                                          "Are you ready to check the request again?\n"
                                          f"{engext}")
        bot.register_next_step_handler(message, ok)
    else:
        exit(message)


def eblan(message):
    if message.text != "/exit":
        data[str(message.chat.id)][3] = message.text
        bot.send_message(message.chat.id, "Вы готовы проверить анкету ещё раз?\n"
                                          "Are you ready to check the request again??\n"
                                          f"{engext}")
        bot.register_next_step_handler(message, ok)
    else:
        exit(message)


def kon4(message):
    if message.text != "/exit":
        data[str(message.chat.id)][4] = message.message_id
        bot.send_message(message.chat.id, "Вы готовы проверить анкету ещё раз?\n"
                                          "Are you ready to check the request again?\n"
                                          f"{engext}")
        bot.register_next_step_handler(message, ok)
    else:
        exit(message)


def vegetable(message):
    if message.text != "/exit":
        data[str(message.chat.id)][1] = message.text
        bot.send_message(message.chat.id, "Вы готовы проверить анкету ещё раз?\n"
                                          "Are you ready to check the request again?\n"
                                          f"{engext}")
        bot.register_next_step_handler(message, ok)
    else:
        exit(message)


def exit(message):
    users = users_out('users.json')
    if users[users[0].index(message.chat.id) + 2]['lng'] == 'rus':
        bot.send_message(message.chat.id, "Вы отменили функцию")
    else:
        bot.send_message(message.chat.id, "You have rejected your request")


def feed(message):
    if message.text != "/exit":
        users = users_out('users.json')
        feedback = users_out('feedback.json')
        if str(message.chat.id) not in feedback.keys():
            feedback[str(message.chat.id)] = []
            feedback[str(message.chat.id)].append(message.text)
        else:
            feedback[str(message.chat.id)].append(message.text)
        feedback_in('feedback.json', feedback)
        if users[users[0].index(message.chat.id) + 2]['lng'] == 'rus':
            bot.send_message(message.chat.id, "Спасибо за Ваше мнение!\nВы делаете нас лучше! <3")
        else:
            bot.send_message(message.chat.id,
                             'Thank you for your opinion!\nYou make us better! <3')


bot.send_message(sheluha, 'Скриптонит запущен! Используй как обычно :)')

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except:
            continue
