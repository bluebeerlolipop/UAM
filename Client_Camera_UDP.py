import socket
import cv2

UDP_IP = '127.0.0.1'
UDP_PORT = 9505

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 통신 종류 선택 후 소켓 생성

cap = cv2.VideoCapture(0)
# client에 연결되어있는 카메라 인식
# 괄호 안에 있는 숫자난 문자에 따라 카메라를 인식하거나 이미지 인식할 수 있게 함.

while True:
    ret, frame = cap.read()
    d = frame.flatten()
    s = d.tostring()

    for i in range(20):
        sock.sendto(s[i*46080:(i+1)*46080], (UDP_IP, UDP_PORT))
        # 프레임 분할 후 순차적으로 전송

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break