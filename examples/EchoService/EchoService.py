# Echo Service Example using Little Less Protocol for Python
#
# This Example sends an echo request to an Arduino and wait for the echo response.
#
# Copyright (C) 2021 Frank Mueller
#
# SPDX-License-Identifier: MIT

import argparse
import sys
import littlelessprotocol as llp
import time
import serial
from serial.tools import list_ports
import threading

class EchoServiceProtocol(llp.LittleLessProtocolA):
    def __init__(self):
        super(EchoServiceProtocol, self).__init__()
        self.echo_event = threading.Event()

    def get_cmd_id(self, cmd_str: str) -> int:
        if cmd_str == 'ECH':
            return 0
        else:
            return super(EchoServiceProtocol, self).get_cmd_id(cmd_str)

    def get_cmd_str(self, cmd_id: int) -> str:
        if cmd_id == 0:
            return 'ECH'
        else:
            return super(EchoServiceProtocol, self).get_cmd_str(cmd_id)

    def handle_msg(self, msg_type: llp.MessagesType, cmd_id: int, msg):
        self.echo_event.set()

    def handle_unknown_frame(self, frame, err):
        print('Unknown frame:', frame, err)
    
    def send_echo_request(self, data=b'\x01\x02\x03'):
        self.send_message(llp.MessagesType.REQUEST, 0, data)

    def wait_for_echo(self, timeout=5):
        result = self.echo_event.wait(timeout)
        self.echo_event.clear()
        return result

def echo_requests(dev, baudrate, n):
    ser = serial.serial_for_url(dev, baudrate)
    t = serial.threaded.ReaderThread(ser, EchoServiceProtocol)
    t.start()
    transport, protocol = t.connect()
    
    # give Arduino time to boot
    time.sleep(1)
    
    for i in range(n):
        time.sleep(1)
        print('{}. echo request '.format(i+1), end='', flush=True)
        start = time.monotonic()
        protocol.send_echo_request()
        if protocol.wait_for_echo():
            end = time.monotonic()
            duration = end - start
            print('answered in {:.3}s'.format(duration))
        else:
            print('results in timeout')
    
    t.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Echo Request example for Little Less Protocol')
    parser.add_argument('-d', '--device', help='serial device name, default first device found', nargs=1, dest='device', default=[None])
    parser.add_argument('-b', '--baud', help='baudratem default 9600', nargs=1, dest='baudrate', default=[9600], type=int)
    parser.add_argument('-c', help='Count of repeats, default 5', nargs=1, dest='count', default=[5], type=int)
    args = parser.parse_args()
    
    dev = args.device[0]
    if dev is None:
        devs = list_ports.comports()
        if len(devs) > 0:
            dev = devs[0].device

    if dev is None:
        print('No device')
        sys.exit(1)

    baud = args.baudrate[0]
    count = args.count[0]

    print('Dev: {} baud: {} count: {}'.format(dev, baud, count))
    
    echo_requests(dev, baud, count)