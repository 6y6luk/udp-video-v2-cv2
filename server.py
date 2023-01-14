import cv2
import socket
import time
import numpy as np

localIP     = "192.168.50.251"
localPort   = 8080
bufferSize  = 131072


def listen(host: str = localIP, port: int = localPort):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    print(f'listening {localIP}:{localPort}')

    fps = 0
    frame_counter = 0
    time_holder = time.time()

    packet_count = 0
    buffer = b''
    while (True):
        try:
            msg, addr = s.recvfrom(bufferSize)
            buffer += msg
            packet_count += 1
            if (packet_count == 4):
                

                np_array = np.frombuffer(buffer, np.uint8)
                img = cv2.imdecode(np_array, cv2.IMREAD_COLOR) 

                img = cv2.putText(img, 'FPS:' + str(fps), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                cv2.imshow('server', img)

                packet_count = 0
                buffer = b''

                frame_counter += 1 
                if (time.time() - time_holder > 0.5):
                    fps = round(frame_counter / (time.time() - time_holder))
                    time_holder = time.time()
                    frame_counter =  0

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except Exception as e:
            print(e)
    
if __name__ == '__main__':
    listen(localIP, localPort)

    vid.release()
    cv2.destroyAllWindows()