#!/usr/bin/env python3
import json
import asyncio
from copy import deepcopy

from .field_state import FieldState
from Client.contracts.field_state_command import FieldStateCommand
from Client.contracts.value_objects.possible_move import PossibleMove


clients = {}
# clients_login = {}

client_colors = {}
inv_client_colors = {}

game_state = FieldState()


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
                request_json = q.result().decode().strip()
                request = json.loads(request_json)
                command = request["type"]
                print("Server request:", request)
                print("Server command:", command)

                if command == "authorize_command":

                    if len(client_colors) == 1:
                        client_colors[me] = "black"
                        inv_client_colors["black"] = me

                        # TODO: fix govnokod
                        checkers = deepcopy(game_state.checkers)
                        for checker in checkers:
                            checker.your_checker = not checker.your_checker
                            checker.possible_moves = []

                        await clients[me].put(
                            json.dumps(
                                FieldStateCommand(
                                    checkers
                                ).to_json()
                            )
                        )

                    if len(client_colors) == 0:
                        client_colors[me] = "white"
                        inv_client_colors["white"] = me

                        await clients[me].put(
                            json.dumps(
                                FieldStateCommand(
                                    game_state.checkers
                                ).to_json()
                            )
                        )

                    print("Server client_colors:", client_colors)

                elif command == "move_command":

                    user_color = client_colors[me]
                    openent_color = "black" if user_color == "white" else "white"
                    print("Server user_color:", user_color)
                    print("Server openent_color:", openent_color)

                    checker_num = request["checker_num"]
                    print("Server checker_num:", checker_num)

                    move = PossibleMove.from_json(request)
                    print("Server move:", move)

                    game_state.make_move(checker_num, move)
                    print("Server game_state.make_move Done!")

                    oponent_id = inv_client_colors[openent_color]
                    print('Server oponent_id', oponent_id)

                    # TODO: remove debug statement
                    await clients[oponent_id].put(request_json)

                    # TODO: fix govnokod
                    checkers = deepcopy(game_state.checkers)
                    for checker in checkers:
                        checker.your_checker = not checker.your_checker
                        checker.possible_moves = []

                    await clients[me].put(
                        json.dumps(
                            FieldStateCommand(
                                checkers
                            ).to_json()
                        )
                    )

                    # TODO: fix govnokod
                    for checker in game_state.checkers:
                        checker.your_checker = not checker.your_checker
                        # checker.possible_moves = []

                    await clients[oponent_id].put(
                        json.dumps(
                            FieldStateCommand(
                                game_state.checkers
                            ).to_json()
                        )
                    )

                    print('Server move_command Done!')

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
