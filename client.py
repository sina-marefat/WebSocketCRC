import asyncio
import logging
import time

import websockets


@asyncio.coroutine
def receiver():
    logging.basicConfig(level=logging.INFO)
    websocket = yield from websockets.connect('ws://localhost:8765/')
    while True:
        yield from websocket.send("READY")
        frame = yield from websocket.recv()
        errorPattern = yield from websocket.recv()
        hasError = frameCheck(frame, errorPattern)

        time.sleep(5)
        while hasError:
            logging.error("NACK : received frame with error  : {} error pattern {} \n".format(frame, errorPattern))
            yield from websocket.send("NACK")
            frame = yield from websocket.recv()
            errorPattern = yield from websocket.recv()
            hasError = frameCheck(frame, errorPattern)
            time.sleep(5)

        logging.info("ACK : received frame successfully : {} \n".format(frame))
        print("-------------------------------------------------------\n\n")
        yield from websocket.send("ACK")


def frameCheck(frame, errorPattern):
    return True


asyncio.get_event_loop().run_until_complete(receiver())
