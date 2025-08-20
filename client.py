import socket
import threading
import os

def upload_file(user):
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
        else:
            user.send('net'.encode('utf-8'))
            print('Нет такого файла')

def download_file(user):
        user.send(input('$ ').encode("utf-8"))

        file = user.recv(1024).decode('utf-8')
        if file == 'Нет такого файла':
            print(file)
        else:
            print(file)########
            file_name, filesize = file.split(' | ')
            file_size = int(filesize)
                    
            with open(f"{file_name}", 'wb') as f:
                received_butes = 0

                while received_butes < file_size:
                    file_content = user.recv(2500)

                    if not file_content:
                        break

                    f.write(file_content)
                    received_butes += len(file_content)
                    print('Файл получин')

def check_file(file):
    dir_list = os.listdir()
    if file in dir_list:
       return True
    else:
        return False
       

def handle_client(user, adres):
    try:   
        while True:
            user.send(input('$ ').encode("utf-8")) 

            data = user.recv(1024).decode('utf-8')
            if not data:
                print('Нет подключения')
            
            print(data)

            if data == 'Название файла для скачевания:':
                download_file()
        
            if data == 'Укожите фаил для закгрузки:':
                upload_file()

    except ConnectionResetError: # Обробатывет ошибку 
        print("Соединение сброшено.")


#
# Реализовать отправку сообщения конкретному пользователю 
#
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Для того чтоб не появлялась невзапная ошибка от портов 
    server.bind(("0.0.0.0", 10000)) 
    server.listen(5) # Прослушивает подключение 
    
    while True:
        user, adres = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(user, adres))
        client_thread.daemon = True
        client_thread.start()
        print('[+] Connect')
        print(adres)


main()
