# v: 0.0.1 | 11.08.2025
# v: 0.2 | 05.10.2025 
import asyncio

ip = 'misss'
port = LoL

clients = []
admin = None

                    msg_data = await reader.read(1024)
                    if not msg_data:
                        break
                    msg = msg_data.decode().strip()
                    print(msg)

                    for cl in clients:
                        try:
                            cl['writer'].write(msg.encode())
                            await cl['writer'].drain()
                   тправлено всем.\n".encode())
                    await writer.drain()
                        await writer.drain()
                        return
           f"Имя клиента {id} изменено на {new_name}\n".encode())
                        await writer.drain()
                    except ValueError:
                        writer.write("ID должен быть числом!\n".encode())
                        await writer.drain()
                    except:
                        writer.write("Нет такого ID".encode())
                 encode())
                    for i, client in enumerate(clients):
         
                chunk = await reader.read(min(4096, file_size - received))
                if not chunk:
                    break
    
    asyncio.run(main())

