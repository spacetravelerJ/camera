from picamera2 import Picamera2, Preview
from time import sleep
import cv2
import RPi.GPIO as g
import os

led = 18


g.setwarnings(False)
g.setmode(g.BCM)
g.setup(led, g.OUT)

image_name = 0 # 사진 파일 이름 인덱스
result = ''
# 파일 초기화
with open('/mnt/gdrive/name.txt','w') as f: #카메라 파일 이름 보낼 곳
    f.write('')
with open('/mnt/gdrive/signal.txt','w') as f: # 컴에서 모든 처리가 완료되어 다른 처리를 기다리는 신호를 받음 
    f.write('0')
with open('/mnt/gdrive/result.txt','w') as f: # 결과 받을 곳
    f.write('')


name_path = '/mnt/gdrive/name.txt'
signal_path = '/mnt/gdrive/signal.txt'
result_path = '/mnt/gdrive/result.txt'
#image_path = '/mnt/gdrive/image'+image_name+'.jpg'

cap = cv2.VideoCapture(0)

while True:
    try:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        flipped_frame = cv2.flip(frame, 1)
        cv2.imshow('', flipped_frame)

        if cv2.waitKey(1) & 0xFF == ord('s'): # 's'키를 누르면 사진 찍고 보내줌
            print('3')
            sleep(1)
            print('2')
            sleep(1)
            print('1')
            sleep(1)
            cv2.imwrite('/mnt/gdrive/image' + str(image_name) + '.jpg', flipped_frame)
            print("Image captured.")
            with open(name_path, 'w') as f:
                f.write(str(image_name))
            print(f"Image saved as image{image_name}.jpg and index written to result.txt")
            image_name += 1

            while True:
                with open(signal_path, 'r+') as f:
                    signal = f.read().strip()
                    f.write('0')
                if signal == '2':
                    print("Processing completed signal received.")
                    with open(result_path, 'r') as f: 
                        result = f.read().strip()
                    
                    print(f"Result received: {result}")
                    break
                elif signal == '1':
                    print("Processing in progress...")
                else:
                    print("Waiting for processing to complete...")
                sleep(0.5)

            if signal=='2':
                if result == '':
                    print("No result received.")
                elif result == 'LH':
                    print("led HIGH")
                    g.output(led, g.HIGH)
                elif result == 'LL':
                    print("led LOW")
                    g.output(led, g.LOW)
                else: 
                    print(f"Unknown result received: {result}")
                
    except Exception as e:
        print(f"처리 중 예기치 않은 오류가 발생했습니다: {e}")
