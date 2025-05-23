import socket
import webbrowser
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Для того чтоб не появлялась невзапная ошибка от портов 
server.bind(("0.0.0.0", 10000)) 

server.listen(5) # Прослушивает подключение 

user, adres = server.accept()
print('[+] Connect')
print(adres)


def upload_file():
        file_name = input('$ ')
        file_size = os.path.getsize(file_name)

        user.send(f'{file_name} | {file_size}'.encode('utf-8'))

        with open(file_name, 'rb') as f:
            while True:
                content = f.read(2500)

                if not content:
                    break

                user.sendall(content)
        print('Файл загружен')

def download_file():
        user.send(input('$ ').encode("utf-8"))

        file = user.recv(1024).decode('utf-8')
        file_name, filesize = file.split(' | ')
        file_size = int(filesize)
                
        with open(f"{adres}_{file_name}", 'wb') as f:
            received_butes = 0

            while received_butes < file_size:
                file_content = user.recv(100000)

                if not file_content:
                    break

                f.write(file_content)
                received_butes += len(file_content)
                print('Файл получин')


while True:
    try:    
        user.send(input('$ ').encode("utf-8")) 

        data = user.recv(1024).decode('utf-8')
        if not data:
            print('Нет подключения')
            break
        print(data)

        if data == 'Название файла для скачевания:':
            download_file()
        
        if data == 'Укожите фаил для закгрузки:':
            upload_file()

    except ConnectionResetError: # Обробатывет ошибку 
        print("Соединение сброшено.")
