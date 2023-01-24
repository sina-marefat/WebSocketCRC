import logging
import random
import time

import websocket

import asyncio
import websockets

from CRC import CRC
from configReader import ConfigReader

@asyncio.coroutine
def handler(socket, path):
    crc = CRC()
    configReader = ConfigReader("config.ini")
    cfg = configReader.Config()
    bitLength = int(cfg['DEFAULT']['bitLength'])
    crcFunc = cfg['DEFAULT']['crcFunction']
    while True:
        status = yield from socket.recv()
        if status == "READY":
            frame = createRandomData(bitLength)
            crcFrame = crc.encodedData(frame, crcFunc)
            errPattern = createRandomErrPattern(bitLength + len(crcFunc) - 1)
            tryTime = 1
            yield from socket.send(crc.xor(crcFrame, errPattern))
            time.sleep(5)
            print("try number {}:\n".format(tryTime))
            logging.info("sent data : {} with frame {} with Error Patten {}\n".format(frame, crcFrame, errPattern))

            ack = yield from socket.recv()
            while ack == "NACK":
                errPattern = createRandomErrPattern(bitLength + len(crcFunc) - 1)
                logging.error("NACK -> Received NACK from receiver retrying with error pattern : {}\n".
                              format(errPattern))

                time.sleep(5)
                tryTime+=1
                print("try number {}:\n".format(tryTime))
                yield from socket.send(crc.xor(crcFrame, errPattern))
                logging.info("sent data : {} with frame {} with Error Patten {}\n".format(frame, crcFrame, errPattern))
                time.sleep(5)
                ack = yield from socket.recv()
            logging.info("ACK -> Received ACK from receiver frame received successfully\n")
            print("-------------------------------------------------------")


def createRandomData(bitLength):
    frame = ''
    i = 0
    while i < bitLength:
        frame += str(random.randint(0, 1))
        i+=1
    return frame


def createRandomErrPattern(frameLength):
    pattern = ''
    i = 0
    while i < frameLength:
        i += 1
        rand = random.randint(0, 101)
        if rand > 80:
            pattern += '1'
            continue
        pattern += '0'
    return pattern


logging.basicConfig(level=logging.INFO)

start_server = websockets.serve(handler, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
