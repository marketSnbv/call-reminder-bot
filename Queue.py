import random
import telebot
import time
import pycron
import threading
import datetime


def find_in(word, list_of_people):
    for i in range(len(list_of_people)):
        if list_of_people[i][0] == word:
            return i
    return -1


def get_info(file):
    f = open(file)
    people = f.readlines()
    f.close()
    number_of_round = int(people[0].split(" ")[0])
    people.remove(people[0])
    for i in range(len(people)):
        man = people[i].strip().split(" ")
        people[i] = man
    return number_of_round, people


def find_caller(people, number_of_round):
    pretenders = []
    for acc in people:
        if int(acc[1]) < number_of_round:
            pretenders.append(acc)
    num = random.randint(0, len(pretenders) - 1)
    return pretenders[num][0]


def write_new_info(file, people, number_of_round):
    fl = open(file, 'w')
    fl.write(str(number_of_round) + " (Number of call)" + '\n')
    for man in people:
        fl.write(" ".join(man) + '\n')
    fl.close()


def main_finder():
    file = "who_calls.txt"
    number_of_round, people = get_info(file)
    caller = find_caller(people, number_of_round)
    index = find_in(caller, people)
    people[index][1] = str(int(people[index][1]) + 1)
    count_called = 0
    for man in people:
        if int(man[1]) == number_of_round:
            count_called += 1
    if count_called == len(people):
        number_of_round += 1
    write_new_info(file, people, number_of_round)
    print(caller)
    who = open("who.txt", 'w')
    who.write(caller + ". Последнее обновление " + str(datetime.date.today()))
    who.close()
    return caller


def send_next_caller():
    caller = main_finder()
    bot.send_message(chat_id, "Завтра утром Владлене звонит " + caller +
                     ".\nВ связи с отпуском время звонка переносится на 12:00 по екб")


def start():
    bot.infinity_polling()


def scheduling():
    while True:
    #                     |----------------- on minute 0, so every full hour
    #                     |  |--------------- on hour 16
    #                     |  |   | |-------- every day in month and every month
    #                     V  V   V V  v------ on weekdays Sunday till Thursday
        if pycron.is_now('00 16 * * sun-thu'):  # 19 in Moscow, server time
            send_next_caller()
            time.sleep(60)
        elif pycron.is_now('55 6 * * mon-fri'):  # 9:55 in Moscow, server time
            remind()
            time.sleep(60)


def remind():
    f = open("who.txt")
    caller = f.readline().split(".")[0]
    f.close()
    bot.send_message(chat_id, caller + " не забудь порадовать Владлену!")


def check():
    who = open("who.txt")
    data = who.readline()
    who.close()
    return "Сегодня звонит " + data


chat_id = "chat_id"
bot = telebot.TeleBot("token")
bot_name = "bot_name"  # for example @qwe_bot


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.text == "/help" or message.text == "/start" \
            or message.text == "/start" + bot_name or message.text == "/help" + bot_name:
        text = "Привет! Я бот, который помогает ннгшникам понять, чья сегодня очередь звонить Владлене. " \
               "Звонить нужно в 5:40 по МСК (7:40 по ЕКБ). Номер в целях безопасности спрашивать у участников чата.\n" \
               "Рерольнуть участника можно командой /choose, но человек, который выпал до реролла, " \
               "пропустит свою очередь "
        bot.reply_to(message, text)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "/help" or message.text == "/start" \
            or message.text == "/start@" + bot_name or message.text == "/help" + bot_name:
        text = "Привет! Я бот, который помогает ннгшникам понять, чья сегодня очередь звонить Владлене. " \
               "Звонить нужно в 5:40 по МСК (7:40 по ЕКБ). Номер в целях безопасности спрашивать у участников чата.\n" \
               "Рерольнуть участника можно командой /choose, но человек, который выпал до реролла, " \
               "пропустит свою очередь "
    elif message.text == "/choose" or message.text == "/choose" + bot_name:
        text = "Я выбрал " + main_finder()
    elif message.text == "/check" or message.text == "/check" + bot_name:
        text = check()
    else:
        text = "Такого не знаю, дружок, ты ошибся командой"
    bot.reply_to(message, text)


t1 = threading.Thread(target=scheduling)
t2 = threading.Thread(target=start)
t1.start()
t2.start()
