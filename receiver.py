# Ivan Chowdhury
# ECE303 Communication Networks
# Shivam Mevawala
# Spring 2019

import logging
import channelsimulator
import utils
import sys
import socket

import time
import timeit
from segment import *

class Receiver(object):

    def __init__(self, inbound_port=50005, outbound_port=50006, timeout=10, debug_level=logging.INFO):
        self.logger = utils.Logger(self.__class__.__name__, debug_level)

        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.simulator = channelsimulator.ChannelSimulator(inbound_port=inbound_port, outbound_port=outbound_port,
                                                           debug_level=debug_level)
        self.simulator.rcvr_setup(timeout)
        self.simulator.sndr_setup(timeout)

    def receive(self):
        raise NotImplementedError("The base API class has no implementation. Please override and add your own.")


class BogoReceiver(Receiver):
    ACK_DATA = bytes(123)

    def __init__(self):
        super(BogoReceiver, self).__init__()

    def receive(self):
        self.logger.info("Receiving on port: {} and replying with ACK on port: {}".format(self.inbound_port, self.outbound_port))
        while True:
            try:
                data = self.simulator.u_receive()  # receive data
                self.logger.info("Got data from socket: {}".format(
                data.decode('ascii')))  # note that ASCII will only decode bytes in the range 0-127
                sys.stdout.write(data)
                self.simulator.u_send(BogoReceiver.ACK_DATA)  # send ACK
            except socket.timeout:
                sys.exit()

class MyReceiver(Receiver): # Inherit from BogoReceiver

    def __init__(self):
        super(MyReceiver, self).__init__(timeout=15)

    def receive(self):  # Override receive method
        self.logger.info("Receiving on port {}\nReplying with ACK to port {}".format(self.inbound_port, self.outbound_port))
        seqIDest = 0    # Expected seqID ID

        while True:
            msg = self.simulator.u_receive()    # Receive msg sent by MySender
            received_checksum = msg[:2]  
            seqID = chr(msg[2])
            data = msg[3:]

            if checkSum(data) == received_checksum: # Compare checksums to check for bit errors
                    ACKmsg = bytearray("ACK", "ascii")
                    ACKmsg.append(int(seqID))
                    ACKchecksum = checkSum(ACKmsg)
                    
                    self.logger.info("Checksum correct, no bit errors. Sending ACK: {} {}".format(
                        (list(ACKchecksum)), (list(ACKmsg))))
                    self.simulator.u_send(ACKchecksum + ACKmsg)
                    
                    if seqID == str(seqIDest):  # Compare seq IDs
                        self.logger.info("Received data from socket {}".format(
                            data))  
                        sys.stdout.write(data)
                        seqIDest = 1 - seqIDest # Switch between 0 and 1

            else:   # If Checksums don't match, there are bit errors. Create and send NAK
                NAK = 1 - seqIDest
                NAKmsg = bytearray("ACK", "ascii")
                NAKmsg.append(NAK)
                NAKchecksum = checkSum(NAKmsg)
                self.logger.info("Incorrect checksum, bit errors detected. Sending NAK: {} {}".format(
                    (list(NAKchecksum)), (list(NAKmsg))))
                self.simulator.u_send(NAKchecksum + NAKmsg)

if __name__ == "__main__":
    rcvr = MyReceiver()
    t1 = time.time()

    try:
        rcvr.receive()
    except socket.timeout:
        t2 = time.time()
        duration = t2 - t1

        rcvr.logger.info("Receiver Timeout. Took {} s.".format(duration))
        sys.stderr.write("Receiver Timeout. Took {} s.\nPlease try 'make diff'. If there is any output, keep waiting for the process to complete.\n".format(duration))