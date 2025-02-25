import socket
import time

# Completati cu adresa IP a platformei ESP32
PEER_IP = "192.168.89.29"
PEER_PORT = 10001

MESSAGE = b"Salut!"
i = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while 1:
    try:
        if i % 2 == 0:
            MESSAGE = b"GPIO4=1"  # aprinde LED ul
        else:
            MESSAGE = b"GPIO4=0"  # stinge LEDul
        #TO_SEND = MESSAGE + bytes(str(i),"ascii")
        sock.sendto(MESSAGE, (PEER_IP, PEER_PORT))
        print("Am trimis mesajul: ", MESSAGE)
        i = i + 1
        time.sleep(1)
    except KeyboardInterrupt:
        break