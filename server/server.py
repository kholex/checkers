#!/usr/bin/env python3
import json
import asyncio

import sys
sys.path.insert(0, ".")  # TODO: remove it
from server.utils import generate_new_game
from Client.contracts.field_state_command import FieldStateCommand
from Client.contracts.value_objects.checker import Checker


clients = {}
clients_login = {}
client_colors = {}


async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print("User:", me)

    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    command = ""
    while not reader.at_eof() and command != "exit":
        done, _ = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                request = json.loads(q.result().decode().strip())
                command = request["type"]
                print("Server request:", request)
                print("Server command:", command)

                if command == "authorize_command":

                    white_checkers_list, black_checkers_list = generate_new_game()
                    white_checkers_state = FieldStateCommand(white_checkers_list)
                    black_checkers_state = FieldStateCommand(black_checkers_list)

                    if len(client_colors) == 1:
                        client_colors["black"] = me
                        await clients[me].put(json.dumps(black_checkers_state.to_json()))
                    
                    if len(client_colors) == 0:
                        client_colors["white"] = me
                        await clients[me].put(json.dumps(white_checkers_state.to_json()))
                    
                    print("Server client_colors:", client_colors)

                elif command == "move_command":
                    try:
                        checker = Checker.from_json(request)
                        print("checker", checker)
                    except Exception as tmp:
                        print("exception", tmp)

            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                print("Server receive:", q.result())
                await writer.drain()

    send.cancel()
    receive.cancel()
    print("Server done:", me)

    del clients[me]

    if me in clients_login:
        del clients_login[me]
        
    writer.close()
    await writer.wait_closed()
