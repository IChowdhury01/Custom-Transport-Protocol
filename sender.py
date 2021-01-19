# Ivan Chowdhury
# ECE303 Communication Networks
# Shivam Mevawala
# Spring 2019

import logging
import socket
import channelsimulator
import utils
import sys

from segment import *

class Sender(object):

    def __init__(self, inbound_port=50006, outbound_port=50005, timeout=15, debug_level=logging.INFO):
        self.logger = utils.Logger(self.__class__.__name__, debug_level)

        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.simulator = channelsimulator.ChannelSimulator(inbound_port=inbound_port, outbound_port=outbound_port,
                                                           debug_level=debug_level)
        self.simulator.sndr_setup(timeout)
        self.simulator.rcvr_setup(timeout)

    def send(self, data):
        raise NotImplementedError("The base API class has no implementation. Please override and add your own.")


class BogoSender(Sender):

    def __init__(self):
        super(BogoSender, self).__init__()

    def send(self, data):
        self.logger.info("Sending on port: {} and waiting for ACK on port: {}".format(self.outbound_port, self.inbound_port))
        while True:
            try:
                self.simulator.u_send(data)  # send data
                ack = self.simulator.u_receive()  # receive ACK
                self.logger.info("Got ACK from socket: {}".format(
                    ack.decode('ascii')))  # note that ASCII will only decode bytes in the range 0-127
                break
            except socket.timeout:
                pass

class MySender(Sender): # Inherit from BogoSender class
    def __init__(self):
        super(MySender, self).__init__()

    def send(self, data):   # Override send method

        self.logger.info("Sending on port: {} and waiting for ACK on port: {}".format(self.outbound_port, self.inbound_port))
        sys.stderr.write("Sending file through channel. Please wait...\n")

        framelist = createFrames(data)  # Divide data into frames
        bitID = 0   # Either 0 or 1
        framecounter = 0    # Tracks current frame

        for frame in framelist:    # Iterate through frame list, increment counter
            framecounter += 1    
            self.logger.info("Sending frame {}".format(framecounter))
            ack_received = False    # Tracks whether an ACK has been received

            while not ack_received:
                prefix = bytearray(checkSum(frame) + str(bitID))    # Headers
                self.simulator.u_send(prefix + frame)   # Send message

                try:   # Receive message
                    msg = self.simulator.u_receive()
                
                except socket.timeout:      # Timeout
                    self.logger.info("Timeout")
                    sys.stderr.write("Sender Timeout. If this keeps occuring, increase timeout value.\n")
                
                else:
                    checksum = msg[:2]
                    ack = msg[5]
                    if checkSum(msg[2:])==checksum and ack == bitID:    # Check ACK # and checksum
                        ack_received = True;    # No error
        
            bitID = 1 - bitID   # Switch between 0 and 1
                
        # Log and print time
        self.logger.info("Data has been sent.")
        sys.stderr.write("Data has been sent. Please wait for the data to be received...\n")
    
        exit(0)

if __name__ == "__main__":
    # test out MySender
    DATA = bytearray(sys.stdin.read())
    sndr = MySender()
    sndr.send(DATA)