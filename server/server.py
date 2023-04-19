#!/usr/bin/env python3
import asyncio
import shlex

from utils import generate_new_game  # TODO: fix relative import


clients = {}
clients_login = {}


async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print("tmp", me)
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    command = ""
    while not reader.at_eof() and command != "exit":
        done, _ = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                request = q.result().decode().strip()
                command = shlex.split(request)[0]
                command_args = shlex.split(request)[1:]
                if command == "login":  # TODO: auth
                    login = command_args[0]
                    if login not in clients_login.values():
                        clients_login[me] = login
                        await clients[me].put(f"Success login as {login}")
                    else:
                        await clients[me].put(f"Login {login} already in use")
                elif command == "who":
                    await clients[me].put('\n'.join(clients_login.values()))
                elif command == "play":
                    if me in clients_login:
                        if command_args[0] in clients_login.values():
                            for key in clients:
                                if clients_login[key] == command_args[0]:
                                    await clients[key].put(f"{me} wants to play with you")
                                    # send
                                    print("a", me)
                                    print("b", key)
                                    checker_list = generate_new_game()
                                    print("checker_list")#, checker_list)
                        else:
                            await clients[me].put(f"There is no client with login {command_args[0]}!")
                    else:
                        await clients[me].put(f"Not authorized can't send any messages to other clients!")
                elif command == "exit":
                    break
                else:
                    for out in clients.values():
                        if out is not clients[me]:
                            await out.put(f"{me} {q.result().decode().strip()}")
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    if me in clients_login:
        del clients_login[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
