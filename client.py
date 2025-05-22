import socket
import webbrowser

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Для того чтоб не появлялась невзапная ошибка от портов 
server.bind(("127.0.0.1", 8080)) 

server.listen(5) # Прослушивает подключение 

user, adres = server.accept()
print('[+] Connect')
print(adres)

while True:
    try:    
        user.send(input('$ ').encode("utf-8")) 

        data = user.recv(3065).decode('utf-8')
        if not data:
            print('Нет подключения')
            break
        print(data)

    except ConnectionResetError: # Обробатывет ошибку 
        print("Соединение сброшено.")
