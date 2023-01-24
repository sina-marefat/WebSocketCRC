import asyncio
import logging
import time

import websockets

from CRC import CRC
from configReader import ConfigReader


@asyncio.coroutine
def receiver():
    websocket = yield from websockets.connect('ws://localhost:8765/')
    crc = CRC()
    configReader = ConfigReader("config.ini")
    cfg = configReader.Config()
    crcFunc = cfg['DEFAULT']['crcFunction']
    while True:
        yield from websocket.send("READY")
        frame = yield from websocket.recv()
        hasError, data = crc.checkError(frame, crcFunc)
        time.sleep(5)
        while hasError:
            logging.error("NACK : received frame : {} with error \n".format(frame))
            yield from websocket.send("NACK")
            time.sleep(5)
            frame = yield from websocket.recv()
            hasError, data = crc.checkError(frame, crcFunc)
            time.sleep(5)

        logging.info("ACK : received data successfully : {} \n".format(data))
        print("-------------------------------------------------------\n\n")
        yield from websocket.send("ACK")


logging.basicConfig(level=logging.INFO)
asyncio.get_event_loop().run_until_complete(receiver())
