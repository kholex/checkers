"""This module is entry point for client app."""
import tkinter as tk
from canvas_field import CanvasField
import asyncio
import threading
import json
from functools import partial

from canvas_move import CanvasMove
from contracts.authorize_command import AuthorizeCommand
from contracts.authorize_response import AuthorizeResponse
from contracts.field_state_command import FieldStateCommand
from contracts.move_command import MoveCommand
import gettext
translation = gettext.translation('checkers', 'locale', fallback=False, languages=['ru', 'en'])
_ = translation.gettext

cell_size = 60
field_size = cell_size * 8


async def _server_communication(reader, writer, canvas_field: CanvasField, receive_queue: asyncio.Queue,
                                login_entry: tk.Entry, login_button: tk.Button):
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
                if command_json["type"] == "field_state_command":
                    field_state = FieldStateCommand.from_json(command_json)
                    canvas_field.init_checkers(field_state.checkers)
                elif command_json["type"] == "move_command":
                    move = MoveCommand.from_json(command_json)
                    checker_to_move = canvas_field.checkers[move.checker_num]
                    checker_to_remove_icon = None
                    if move.remove_checker_num is not None:
                        checker_to_remove = canvas_field.checkers[move.remove_checker_num]
                        checker_to_remove_icon = checker_to_remove.icon
                    checker_to_move.move(CanvasMove(move.x, move.y, move.new_type,
                                                    move.remove_checker_num, checker_to_remove_icon))
                elif command_json["type"] == "authorize_response":
                    authorize = AuthorizeResponse.from_json(command_json)
                    if not authorize.result:
                        login_entry['state'] = tk.NORMAL
                        login_button['state'] = tk.NORMAL
                    print(authorize.result)
            elif q is receive:
                receive = asyncio.create_task(receive_queue.get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    writer.close()
    await writer.wait_closed()


async def _start_communication(canvas_field: CanvasField, receive_queue: asyncio.Queue,
                               login_entry: tk.Entry, login_button: tk.Button):
    connecting_label = None
    while True:
        if connecting_label is None:
            connecting_label = canvas_field.canvas.create_text(canvas_field.size // 2,
                                                               canvas_field.size // 2,
                                                               text=_("Connecting to server..."),
                                                               fill="#f77902",
                                                               font=('Helvetica', '30', 'bold'))

            connecting_rectangle = canvas_field.canvas.create_rectangle(canvas_field.canvas.bbox(connecting_label),
                                                                        fill="white")
            canvas_field.canvas.tag_lower(connecting_rectangle, connecting_label)

        try:
            reader, writer = await asyncio.open_connection('127.0.0.1', 5000)
            canvas_field.canvas.delete(connecting_label)
            canvas_field.canvas.delete(connecting_rectangle)
            connecting_label = None
            await _server_communication(reader, writer, canvas_field, receive_queue, login_entry, login_button)
        except Exception as ex:
            print(ex)
            await asyncio.sleep(1)


def _login_form(screen: tk.Tk, queue: asyncio.Queue):
    login_canvas = tk.Canvas(screen, width=field_size, height=field_size // 5)
    login_canvas.pack()
    # username label and text entry box
    tk.Label(login_canvas, text=_("User Name")).grid(row=0, column=0, sticky="nsew")
    username = tk.StringVar()
    login_entry = tk.Entry(login_canvas, textvariable=username)
    login_entry.grid(row=0, column=1, sticky="nsew")

    def try_authorize(login):
        authorize_command_json = AuthorizeCommand(login.get()).to_json()
        queue.put_nowait(authorize_command_json)
        queue._loop._write_to_self()
        login_button['state'] = tk.DISABLED
        login_entry['state'] = tk.DISABLED

        return

    validate_login = partial(try_authorize, username)

    # login button
    login_button = tk.Button(login_canvas, text=_("Login"), command=validate_login)
    login_button.grid(row=0, column=2, sticky="nsew")

    return login_entry, login_button


def _main() -> None:
    screen = tk.Tk()
    canvas = tk.Canvas(screen, width=field_size, height=field_size)
    canvas.pack()

    queue = asyncio.Queue()
    field = CanvasField(canvas, cell_size, queue)

    login_entry, login_button = _login_form(screen, queue)

    screen.title(_('Checkers'))
    screen.resizable(0, 0)

    screen.after(0, threading.Thread(target=asyncio.run, args=(_start_communication(field, queue, login_entry,
                                                                                    login_button),)).start())
    screen.mainloop()


if __name__ == '__main__':
    _main()
