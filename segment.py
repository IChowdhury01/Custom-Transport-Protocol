# Ivan Chowdhury
# ECE303 Communication Networks
# Shivam Mevawala
# Spring 2019

import sys
import channelsimulator

# Split data into frames of size 1024 bytes, then return a list containing all newly created frames
def createFrames(data_bytes):
    framelist = list()  # List containing all frames
    bytecount = len(data_bytes) # Record size of data in bytes
    bufsize = channelsimulator.ChannelSimulator.BUFFER_SIZE - 3 # Buffer size

    extrabyte = 1 if bytecount % bufsize else 0 
    for i in xrange(bytecount / bufsize + extrabyte):   # Split data into frames
        framelist.append(
            data_bytes[
            i*bufsize:
            i*bufsize + bufsize
            ]
        )
    return framelist

# Compute checksum of data, return as byte array
def checkSum(data): 
    if not isinstance(data, bytearray):     # Check if data is a byte array
        print ("Error: Data must be in ByteArray format")
        exit(-1)

    bitsum = sum(data)  # Compute sum
    return bytearray([(bitsum // 256)%256,bitsum % 256])    # Convert to byte array