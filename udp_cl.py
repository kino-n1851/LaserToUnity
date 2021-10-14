import time
import socket
import json

M_SIZE = 1024
serv_addr = ('127.0.0.1',2323)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    try:
        # ②messageを送信する
        print('Input any messages, Type [end] to exit')
        message = input()
        if message != 'end':
            send_len = sock.sendto(message.encode('utf-8'), serv_addr)
            # ※sendtoメソッドはkeyword arguments(address=serv_addressのような形式)を受け付けないので注意

            # ③Serverからのmessageを受付開始
            print('Waiting response from Server')
            rx_meesage, addr = sock.recvfrom(M_SIZE)
            print(f"[Server]: {rx_meesage.decode(encoding='utf-8')}")

        else:
            print('closing socket')
            sock.close()
            print('done')
            break

    except KeyboardInterrupt:
        print('closing socket')
        sock.close()
        print('done')
        break
