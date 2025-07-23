import cv2

# RTP over UDP로 수신하는 GStreamer 파이프라인
gst_str = (
    "udpsrc port=5000 caps=\"application/x-rtp, encoding-name=H264, payload=96\" ! "
    "rtph264depay ! avdec_h264 ! videoconvert ! appsink"
)

cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)
if not cap.isOpened():
    print("❌ GStreamer 수신 파이프라인 열기 실패")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    cv2.imshow("Server (Receiving)", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()