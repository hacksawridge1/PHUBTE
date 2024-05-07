from threading import Thread
import sys
import json
from pprint import pprint
from modules.user import User
from modules.app import App
from modules.new_server import start_server
from modules.objects import encrypt_object, decrypt_object, find_in_object

def get_users():
  users_online = dict()
  with open('objects/self/users-online') as f:
    file_data = decrypt_object(json.load(f), user.private_key)
    k = 0
    while k < len(file_data['users_online']):
      users_online['k'] = file_data['users_online'][k]['user_name']
    f.close()
  for i,k in users_online.items():
    print(f"{i})\t", k )
  return users_online

user_name = input("Введите ваше имя:\t")
print('Генерируем данные...')

app = App()
user = User(user_name)

server_thread = Thread(target=start_server, args=(user, ))
server_thread.start()
init_thread = Thread(target=user.initial)
init_thread.start()

print("Генерация прошла успешно")

while True:
  users_online = get_users()
  reciever = input("Выберите пользователя:\t")
  data = input('Введите сообщение:\t')
  if data == 'stop':
    user.call_to_remove_user()
    sys.exit()
    break
  elif data == 'Пользователи':
    print(users_online)
  else:
    user.send_message(reciever_name, data)
