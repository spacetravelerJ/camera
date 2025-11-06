import cv2
import mediapipe as mp
import numpy as np
import joblib
import os  # 파일 경로를 확인하기 위해 import
import time
import os.path as path
from usingModelFunc import detect_hands
from tts import ttsText

cnt = 0 # 사진 파일 이름 - 한번이면 충분
label = '' # 인식된 라벨 값 저장 - 할때마다 초기화
totalResult = '' # 전체 결과 저장 - 결과 rpi에 보낼때 초기화
name_path = r"J:\My Drive\name.txt" #카메라 파일 이름 받을 곳
signal_path = r"J:\My Drive\signal.txt"
result_path = r"J:\My Drive\result.txt" # 결과 보낼 곳
log = r"J:\My Drive\LogW.txt"

with open(log, 'w') as f:
    f.write("Log Start(W)\n")

# --- 메인 실행 부분 ---
while True:
    logf = open(log, 'a')
    try:
        #파일에서 이름 읽기
        with open(name_path,'r+') as f:
            name = f.read().strip()
            f.write('')
        #이름이 cnt값과 같으면 처리 시작
        if name == str(cnt):
            label = detect_hands(name) #손 인식 모델 함수 호출 후 결과 받기
            logf.write(f"dectectStatus {name} received(W)\n")
            print(f"detected hand sign for image{name}...")
            cnt+=1
            if label == '':
                print("No hand sign saved.")
                logf.write("No hand sign saved.(W)\n")
            elif label == 2: #명령어 실행
                cnt = 0 #초기화
                print("execute your commend...")
                logf.write("execute your commend...(W)\n")
                ttsText("The detected sign is " + totalResult)
                print("Text to Speech function executed.")
                logf.write("Text to Speech function executed(W)\n")
                if totalResult == '':
                    print("No total result to send.")
                    logf.write("No total result to send.(W)\n")
                else:
                    with open(result_path,'w') as f:
                        f.write(totalResult)
                    print(f"Total result '{totalResult}' written to result.txt")
                    logf.write(f"Total result '{totalResult}' written to result.txt(W)\n")
                    totalResult = '' #초기화
                    with open(signal_path,'w') as f:
                        f.write('2')    
            else:
                totalResult += label
                with open(signal_path,'w') as f:
                    f.write('1')

        else:
            logf.write(f"No new signal to process. Current cnt: {cnt}, name in file: {name}(W)\n")
            print(f"No new signal to process. Current cnt: {cnt}, name in file: {name}")
            continue



    except Exception as e:
        print(f"오류 발생(W): {e}\n")

    print(f"Detected Label: {label}, Total Result: {totalResult}, file_name: {name}, next_file_name: {cnt}")
    label = ''

    logf.close()
    time.sleep(0.1)