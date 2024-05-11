from threading import Thread
from shutil import get_terminal_size
import os
import json
import pyperclip
from pynput.keyboard import Key, Listener
from modules.user import User
from modules.new_server import start_server
from modules.objects import decrypt_object
from time import sleep

sys_name = os.uname().sysname


def get_users(user: User):
  users_online = dict()
  with open('objects/self/users-online.json') as f:
    file_data = decrypt_object(json.load(f), user.private_key)
    k = 1
    while k < len(file_data['users_online']):
      users_online[f'{k}'] = [ 
                              file_data['users_online'][k]['user_name'],
                              file_data['users_online'][k]['user_ip']
                              ]
    f.close()
  for i,user_info in users_online.items():
    print(f"{i})\t", user_info[0], f"\nIP:{user_info[1]}")
  return users_online

def clear_console():
  if sys_name.lower() == "linux":
    os.system("clear")
  elif sys_name.lower() == "windows":
    os.system("cls")
  else:
    print("Неизвестная система!")

def auth():
  print("Добро пожаловать в PHUB!")
  user_name = input("Введите ваше имя:\t")
  while True:
    agree = input("Ваше имя:\t" + user_name +  "\nВсё верно?(y/n):")
    if agree.lower() == 'y':
      break
    elif agree.lower() == 'n':
      user_name = input("Введите ваше имя:\t")
    else:
      print("Только Y или N")
  return user_name

def welcome_to_chat(user: User):
  clear_console()
  try:
    target = get_users(user)
    choose_user = int(input("Выберите номер  пользователя с которым хотите начать переписку:"))
    chat_window(user, target[f"{choose_user}"])
  except ValueError:
    print("Введите числовое значение")
    welcome_to_chat(user)

def chat_window(user: User, reciever: list):
  clear_console()
  try:
    reciever_name = reciever[0]
    reciever_ip = reciever[1]
    print("Добро пожаловать в окно чата, если вы хотите прекратить переписку нажмите Ctrl+C")
    sleep(5)
    chat(user, reciever_name, reciever_ip)
  except KeyboardInterrupt:
    welcome_to_chat(user)

def chat_updater(user: User, reciever_name: str, reciever_ip: str):
  clear_console()
  sleep(1)
  chat(user, reciever_name, reciever_ip)

def chat(user: User, reciever_name: str, reciever_ip: str):
  try:
    chat_updater_thread = Thread(target=chat_updater, args=(chat, user, reciever_name, reciever_ip, ))
    chat_updater_thread.start()
    chat_info = user.chat_info(reciever_name, reciever_ip)
    cols, lines = get_terminal_size()
    while True:
      i = 0
      if len(chat_info) == 0:
        while i < (lines - 1):
          print("\n")
      else:
        while i < (lines - (len(chat_info) + 1)):
          print("\n")
      for k in chat_info:
        if k['user_name'] == reciever_name:
          output = f'{reciever_name}:{k["message"]}' 
          print(output)
        elif k['user_name'] == user.name:
          output = f"{k['message']}:{user.name}"
          print(output.rjust(cols - len(output)))
      with Listener(on_press=pyperclip.copy(Key)) as listener:
        message = input(f"Введите сообщение: {pyperclip.paste()}")
        user.send_message(reciever_ip, reciever_name, message)
  except KeyboardInterrupt:
    welcome_to_chat(user)

def main():
  clear_console()
  user_name = auth()
  user = User(user_name)
  print('Генерируем данные...')
  server_thread = Thread(target=start_server, args=(user, ))
  server_thread.start()
  init_thread = Thread(target=user.initial)
  init_thread.start()
  init_thread.join()
  print("Генерация прошла успешно")
  welcome_to_chat(user)
  
if __name__ == '__main__':
    main()





