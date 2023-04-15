import tkinter as tk
from canvas_field import CanvasField
import asyncio
import threading
import json

from canvas_move import CanvasMove
from contracts.checker import Checker
from contracts.move import Move

cell_size = 60
field_size = cell_size * 8


async def server_communication(reader, writer, canvas_field: CanvasField, receive_queue: asyncio.Queue):
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(receive_queue.get())
    command = ""
    while not reader.at_eof() and command != "exit":
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                request = q.result().decode().strip()
                command_json = json.loads(request)
                if command_json["Type"] == "FieldState":
                    checkers = [Checker.checker_decoder(checker_json) for checker_json in command_json["Checkers"]]
                    canvas_field.init_checkers(checkers)
                elif command_json["Type"] == "Move":
                    move = Move.move_decoder(command_json["Move"])
                    checker_to_move = canvas_field.checkers[move.checker_num]
                    checker_to_remove_icon = None
                    if move.remove_checker_num is not None:
                        checker_to_remove = canvas_field.checkers[move.remove_checker_num]
                        checker_to_remove_icon = checker_to_remove.icon
                    checker_to_move.move(CanvasMove(move.x, move.y, move.new_type,
                                                    move.remove_checker_num, checker_to_remove_icon))
            elif q is receive:
                receive = asyncio.create_task(receive_queue.get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    writer.close()
    await writer.wait_closed()


async def start_communication(canvas_field: CanvasField, receive_queue: asyncio.Queue):
    while True:
        try:
            reader, writer = await asyncio.open_connection('127.0.0.1', 5000)
            await server_communication(reader, writer, canvas_field, receive_queue)
        except Exception as ex:
            print(ex)
            await asyncio.sleep(1)


def main() -> None:
    screen = tk.Tk()
    canvas = tk.Canvas(screen, width=field_size, height=field_size)
    canvas.pack()

    queue = asyncio.Queue()
    field = CanvasField(canvas, cell_size, queue)
    screen.title('Checkers')
    screen.resizable(0, 0)

    screen.after(0, threading.Thread(target=asyncio.run, args=(start_communication(field, queue),)).start())
    screen.mainloop()


if __name__ == '__main__':
    main()
