
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
      
            client['writer'].write('upload file'.encode())
            await client['writer'].drain()

            file_info = await reader.read(1024)
            file_info = file_info.decode().strip()
            file_name, file_size = file_info.split(' | ')
            file_size = int(file_size)

            # Пересылаем file_info клиенту
            client['writer'].write(file_info.encode())

            received = 0
            while received < file_size:
                chunk = await reader.read(min(4096, file_size - received))
                if not chunk:
                    break
                client['writer'].write(chunk)
                await client['writer'].drain()
                received += len(chunk)

            print(f"[SERVER] Файл {file_name} успешно переслан клиенту.")




