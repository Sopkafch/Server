import socket
import webbrowser
import time

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        if client.connect_ex(("127.0.0.1", 8080)):
            pass
        else:
            while True:
                data = client.recv(1024).decode("utf-8") 
                print(data)
                if data == 'google':
                    print(23)
                    webbrowser.open("https://www.google.com")
                    
main()
