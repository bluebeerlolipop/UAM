import cv2
import numpy as np

# GStreamer RTP 파이프라인으로 전송 (H264 인코딩)
gst_str = (
    "appsrc ! videoconvert ! x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! "
    "rtph264pay config-interval=1 pt=96 ! udpsink host=127.0.0.1 port=5000"
)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ 카메라 열기 실패")
    exit()

# GStreamer 파이프라인으로 송출할 VideoWriter 생성
out = cv2.VideoWriter(
    gst_str,
    cv2.CAP_GSTREAMER,
    0,
    30.0,
    (int(cap.get(3)), int(cap.get(4)))
)

if not out.isOpened():
    print("❌ GStreamer 파이프라인 열기 실패")
    cap.release()
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    out.write(frame)

    cv2.imshow("Client (Sending)", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
out.release()
cv2.destroyAllWindows()