import cv2, imutils
import socket
import time
import numpy as np

localIP     = "192.168.50.251"
localPort   = 8080

def connect(host: str = localIP, port: int = localPort):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((host, port))
    print('connected')

    vid = cv2.VideoCapture(0)      

    while (True):
        try:
            ret, frame = vid.read()

            if (ret):
                image_encode = cv2.imencode('.jpg', frame)[1]
                data_encode = np.array(image_encode) # Converting the image into numpy array
                byte_encode = data_encode.tobytes()  # Converting the array to bytes. #ready for socket
            

                splited = np.array_split(data_encode, 4)
                byte_encode_1 = splited[0]
                byte_encode_2 = splited[1]
                byte_encode_3 = splited[2]
                byte_encode_4 = splited[3]
            
                #print('success')

                #cv2.imshow('client', frame)
                #if cv2.waitKey(1) & 0xFF == ord('q'):
                #    break

    
                s.send(bytearray(byte_encode_1))
                s.send(bytearray(byte_encode_2))
                s.send(bytearray(byte_encode_3))
                s.send(bytearray(byte_encode_4))
        except Exception as e:
            print(e)

if __name__ == '__main__':  
    connect(localIP, localPort)
    
    #vid.release()
    #cv2.destroyAllWindows()