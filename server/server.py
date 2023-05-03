#!/usr/bin/env python3
import json
import asyncio

import sys
sys.path.insert(0, ".")  # TODO: remove it
from server.utils import generate_new_game, get_possible_moves
from Client.contracts.field_state_command import FieldStateCommand
from Client.contracts.value_objects.possible_move import PossibleMove


clients = {}
# clients_login = {}

client_colors = {}
inv_client_colors = {}

game_state = {}


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

                    if len(client_colors) == 1:
                        client_colors[me] = "black"
                        inv_client_colors["black"] = me

                        game_state["black"] = black_checkers_list

                        await clients[me].put(
                            json.dumps(FieldStateCommand(black_checkers_list).to_json())
                        )
                    
                    if len(client_colors) == 0:
                        client_colors[me] = "white"
                        inv_client_colors["white"] = me

                        game_state["white"] = white_checkers_list

                        for checker in white_checkers_list:
                            possible_moves = get_possible_moves(checker)
                            checker.possible_moves = possible_moves

                        await clients[me].put(
                            json.dumps(FieldStateCommand(white_checkers_list).to_json())
                        )
                    
                    print("Server client_colors:", client_colors)

                elif command == "move_command":
                    print("Server game_state.keys():", game_state.keys())

                    user_color = client_colors[me]
                    openent_color = "black" if user_color == "white" else "white"
                    print("Server user_color:", user_color)
                    print("Server openent_color:", openent_color)

                    checker_num = request["checker_num"]
                    print("Server checker_num:", checker_num)

                    move = PossibleMove.from_json(request)
                    print("Server move:", move)

                    for checker in game_state[user_color]:
                        checker.possible_moves = []
                        if checker.checker_num == checker_num:
                            checker.x = move.x
                            checker.y = move.y
                    
                    oponent_id = inv_client_colors[openent_color]
                    print('Server oponent_id', oponent_id)

                    for checker in game_state[openent_color]:                        
                        possible_moves = get_possible_moves(checker)
                        checker.possible_moves = possible_moves
                        if checker.checker_num == checker_num:
                            checker.x = move.x
                            checker.y = move.y

                    await clients[me].put(
                        json.dumps(FieldStateCommand(game_state[user_color]).to_json())
                    )
                    await clients[oponent_id].put(
                        json.dumps(FieldStateCommand(game_state[openent_color]).to_json())
                    )

            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                print("Server receive:", q.result())
                await writer.drain()

    send.cancel()
    receive.cancel()
    print("Server done:", me)

    del clients[me]

    # if me in clients_login:
    #     del clients_login[me]

    writer.close()
    await writer.wait_closed()
