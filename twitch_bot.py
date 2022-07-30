import sys
import random
import config
import utils
import socket
import re
import time
from time import sleep


full_msg = ''
command = ''
message = ''
chater = ''
time_move = 2  # action time
TWITCH_RUN = True

lst_chat = ['BOT', 'Write in the chat to play!', 'BOT', 'Welcome to Tank game!',
            'BOT', 'Enter commands for the game in the chat!', 'BOT', 'Welcome!']
sound = False


def send_mess(x):
    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(config.CHAN).encode("utf-8"))
    utils.mess(s, x)


def run():
    global description
    global description2
    global description3
    global sound
    global command
    global message
    global chater
    global time_move
    global TWITCH_RUN
    global full_msg

    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(config.CHAN).encode("utf-8"))
    # chat_message = re.compile(r"^:\w+!\w+@\w+.tmi\.twitch\.tv PRIVMSG #\w+ :")
    chat_message = re.compile(r"^w+")
    description = utils.mess(s, "The game begining! ")
    description2 = utils.mess(s, "Enter commands for the game in the chat: ")
    description3 = utils.mess(s, "!tank !fire !left !right !up !down")

    while TWITCH_RUN:
        response = s.recv(1024).decode("utf-8")
        sound = False
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("POND :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            # ------ get message ------
            # username = re.search(r"\w+", response).group(0)
            msg = chat_message.sub("", response).lower()
            message = msg[1:]
            # print(message)
            for i in message:
                try:
                    if i == "@":
                        chater = message[message.index('@') + 1:message.index('.')]
                        message = message[message.index(':') + 1:]
                        # Исключать непонятные сообщения
                        if message[len(chater): (len(chater)) + 14] == '.tmi.twitch.tv':
                            message = 'Twitch has been connected'
                        elif message[0:8] == 'tmi.twit':
                            message = 'Twitch has been connected'

                        # Перенос длиных строкw
                        if len(message) < 30:
                            full_msg = message
                            lst_chat.insert(0, message)
                            lst_chat.insert(0, chater)
                        else:
                            lst_chat.insert(0, message[0:30])
                            lst_chat.insert(0, chater)
                            lst_chat.insert(0, f'{message[30:60]}')
                            lst_chat.insert(0, chater)
                            lst_chat.pop()
                            lst_chat.pop()
                            full_msg = message
                        lst_chat.pop()
                        lst_chat.pop()
                except ValueError:
                    continue
                except IndexError:
                    pass

        # ---- get value -----
        lst = message.split()
        if len(lst) > 1:
            value = lst[-1]
        else:
            value = 1
        try:
            value = int(value)
        except ValueError:
            value = 1
        time_move = abs(value)
        command = lst[0]
        command = command.lower()
        # ----- get command -----
        if command == "!fire" or command == "!shot" or \
                command == "!left" or command == "!right" or command == "!up" or command == "!down":
            sleep(0.1)
            command = "!"
        # --- bot hello ---
        answers = ["Привет", "Хай", "Здарова", "Здравствуй", "Рад тебя видеть", "Салют", "Приветик", "Хэлло",
                   "Даров"]
        hello = ["привет", "хай", "здарова", "здравствуй", "добрыйвечер", "здравствуйте", "добрыйдень", "хэлло",
                 "hi", "hello", 'privet']
        if command in hello:
            utils.mess(s, answers[random.randint(0, len(answers) - 1)] + ' ' + chater + '!')
        # -- bot time --
        if command == "!time" or command == "!время":
            named_tuple = time.localtime()  # получить struct_time
            time_string = time.strftime("Дата: %d/%m/%Y, Время: %H:%M", named_tuple)
            utils.mess(s, time_string)
        # --- sound chat ---
        if chater.lower():
            sound = True
            sleep(0.1)
            sound = False

    print('Twitch bot has stoped!')
