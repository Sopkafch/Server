import socket
import webbrowser

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Для того чтоб не появлялась невзапная ошибка от портов 
server.bind(("0.0.0.0", 10000)) 

server.listen(5) # Прослушивает подключение 

user, adres = server.accept()
print('[+] Connect')
print(adres)

while True:
    user.send(input('$ ').encode("utf-8")) 
