import socket
import numpy as np
import cv2

UDP_IP = "127.0.0.1"
UDP_PORT = 9505

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("🔄 수신 대기 중...")

while True:
    try:
        # 첫 번째 패킷: 총 패킷 수 수신
        total_packets, _ = sock.recvfrom(1024)
        total_packets = int(total_packets.decode())

        buffer = b''
        for _ in range(total_packets):
            part, _ = sock.recvfrom(4096)
            buffer += part

        # JPEG 디코딩
        img_np = np.frombuffer(buffer, dtype=np.uint8)
        frame = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        if frame is not None:
            cv2.imshow("server", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except Exception as e:
        print(f"에러: {e}")
        continue

cv2.destroyAllWindows()
