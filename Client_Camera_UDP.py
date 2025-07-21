import socket
import cv2

UDP_IP = '127.0.0.1'
UDP_PORT = 9505

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ 카메라 열기 실패")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ 프레임 읽기 실패")
        break

    frame = cv2.resize(frame, (320, 240))  # 크기 줄이면 전송량 더 감소
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]  # 품질 낮춰 압축률 ↑
    result, encimg = cv2.imencode('.jpg', frame, encode_param)

    if not result:
        print("❌ JPEG 인코딩 실패")
        continue

    data = encimg.tobytes()

    # 너무 큰 경우 분할
    max_packet_size = 4096
    total_packets = len(data) // max_packet_size + 1
    sock.sendto(str(total_packets).encode(), (UDP_IP, UDP_PORT))  # 패킷 개수 먼저 전송

    for i in range(total_packets):
        part = data[i*max_packet_size:(i+1)*max_packet_size]
        sock.sendto(part, (UDP_IP, UDP_PORT))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
