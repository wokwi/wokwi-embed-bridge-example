#!/usr/bin/env python

import asyncio
import base64
import json
import sys

import websockets

from gdbserver import GDBServer

PORT = 9012
GDB_PORT = 9333
ELF_PATH = "example/.pio/build/uno/firmware.elf"
HEX_PATH = "example/.pio/build/uno/firmware.hex"
PROJECT_ID = "335697688728175187" # Template project id on wokwi

def base64_file(path: str):
    with open(path, 'rb') as file:
        return base64.b64encode(file.read()).decode('ascii')


gdb_server = GDBServer()


async def handle_client(websocket, path):
    msg = await websocket.recv()
    print("Client connected! {}".format(msg))

    # Send the simulation payload
    await websocket.send(json.dumps({
        "type": "start",
        "elf": base64_file(ELF_PATH),
        "hex": open(HEX_PATH, 'r').read(),
    }))

    gdb_server.on_gdb_message = lambda msg: websocket.send(
        json.dumps({"type": "gdb", "message": msg}))
    gdb_server.on_gdb_break = lambda: websocket.send(
        json.dumps({"type": "gdbBreak"}))

    while True:
        msg = await websocket.recv()
        msgjson = json.loads(msg)
        if msgjson["type"] == "uartData":
            sys.stdout.buffer.write(bytearray(msgjson["bytes"]))
            sys.stdout.flush()
        elif msgjson["type"] == "gdbResponse":
            await gdb_server.send_response(msgjson["response"])
        else:
            print("> {}".format(msg))


start_server = websockets.serve(handle_client, 'localhost', PORT)

asyncio.get_event_loop().run_until_complete(start_server)
print("Web socket listening on port {}".format(PORT))
print("")
print("Now go to https://wokwi.com/_alpha/wembed/{}?partner=platformio&port={}&data=demo".format(PROJECT_ID, PORT))
asyncio.get_event_loop().run_until_complete(gdb_server.start(GDB_PORT))
asyncio.get_event_loop().run_forever()
