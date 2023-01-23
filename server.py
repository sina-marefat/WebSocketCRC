import logging

import websocket

import asyncio
import websockets


@asyncio.coroutine
def hello(socket, path):
    logging.basicConfig(level=logging.INFO)
    while True:
        status = yield from socket.recv()
        if status == "READY":
            frame = randomFrame()
            errorPattern = randomErrorPattern()
            print("Sending b")
            yield from socket.send(frame)
            yield from socket.send(errorPattern)
            print("sent frame: {} with Error Patten {}\n".format(frame, errorPattern))
            ack = yield from socket.recv()
            while ack == "NACK":
                errorPattern = randomErrorPattern()
                logging.error("NACK -> Received NACK from receiver retrying with error pattern : {}\n".
                              format(errorPattern))
                yield from socket.send(frame)
                yield from socket.send(errorPattern)
                ack = yield from socket.recv()
            logging.info("ACK -> Received ACK from receiver frame received successfully\n")
            print("-------------------------------------------------------\n\n")
        else:
            continue


def randomFrame():
    return "1001"


def randomErrorPattern():
    return "1001"


logging.basicConfig(level=logging.INFO)
start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
