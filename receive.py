import socket
import time

HOST = '127.0.0.1'
PORT = 22323
BUFFSIZE = 1024
local_addr = (HOST,PORT)
def main():
    srv = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    srv.bind(local_addr)
    while True:
        try:
            message, cli_addr = srv.recvfrom(BUFFSIZE)
            if(message is not None):
                message = message.decode(encoding='utf-8')
                print(f'Received :[{message}]')
            time.sleep(0.05)
        except KeyboardInterrupt:
            print ('\n . . .\n')
            srv.close()
            break


if __name__ == "__main__":
    main()