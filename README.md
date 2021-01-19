# Transport Protocol

## Description
This is a custom transfer protocol built to send and receive data through a simulated channel. The user may specify any file that they want to send through the channel, and compare the received file's contents to the original file. Channel simulation code was written by Shivam Mevawala. 

## Instructions
1. Install [Python 3+](https://www.python.org/downloads/)
2. Open your Python interpreter to the project directory.
3. Open the Makefile and choose which input file to use, as well as the name of your output file.
4. `make test` to simulate data transfer of the input file through the channel.
5. `make diff` to compare the sent transferred input file and received output file.
6. Other options
    - `make kill` to end the program.
    - `make clean` to clean leftover files.
