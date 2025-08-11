import socket
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 10000)) 

server.listen() # Прослушивает подключение 

def upload_file():
        file_name = input('$ ')
        if check_file(file_name): # если типо он True
            file_size = os.path.getsize(file_name)

            user.send(f'{file_name} | {file_size}'.encode('utf-8'))

            with open(file_name, 'rb') as f:
                while True:
                    content = f.read(2500)

                    if not content:
                        break

                    user.sendall(content)
            print('Файл загружен')
            return True ########################
        else:
            user.send('net'.encode('utf-8'))
            print('Нет такого файла')

def download_file():
    user.send(input('$ ').encode("utf-8")) 

def check_file(file):
    dir_list = os.listdir()
    if file in dir_list:
       return True
    else:
        return False
       

while True:
    user, adres = server.accept()
    print('[+] Connect')
    print(adres)
    while True:
        try:    
            user.send(input('$ ').encode("utf-8")) 

            data = user.recv(1024).decode('utf-8')
            print(data)######

            if data == 'Обновить файл:':
                if upload_file():
                    user.close() ########################
                    break

            if data == 'Укожите фаил для закгрузки:':
                upload_file()

        except ConnectionResetError: # Обробатывет ошибку 
            print(f'[-] Disconect - {adres}, не нажимай на Enter а токонсоль поломаетя   ')
            break
