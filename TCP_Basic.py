# raspberry_server.py
import socket
import struct
import time

# 이미지 파일 경로 (테스트용)
IMAGE_PATH = "/home/pi/capture.jpg"

# 서버 설정
HOST = "0.0.0.0"  # 모든 인터페이스에서 연결 허용
PORT = 8000

# 1️⃣ 소켓 생성 및 바인드
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print(f"[SERVER] Listening on {HOST}:{PORT}")

# 2️⃣ 클라이언트 연결 대기
conn, addr = server.accept()
print(f"[SERVER] Connected by {addr}")

# 3️⃣ 이미지 파일 읽기
with open(IMAGE_PATH, "rb") as f:
    img_data = f.read()

# 4️⃣ 이미지 길이를 먼저 전송 (4바이트 big-endian 정수)
img_size = len(img_data)
conn.sendall(struct.pack(">I", img_size))

# 5️⃣ 이미지 실제 데이터 전송
conn.sendall(img_data)
print(f"[SERVER] Sent {img_size} bytes")

# 6️⃣ 종료
conn.close()
server.close()
print("[SERVER] Connection closed")
