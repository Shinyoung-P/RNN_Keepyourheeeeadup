import serial
import csv
import time
import os
import joblib  # 모델 로드용 모듈
import numpy as np  # 데이터 처리용 모듈


# 시리얼 포트 연결 (포트 이름과 baud rate는 환경에 맞게 수정)
try:
    ser = serial.Serial('COM18', 115200, timeout=1)  # 예시: 'COM18' 포트, 115200 baud
except Exception as e:
    print("시리얼 포트 연결 실패:", e)
    exit()

# 시리얼 포트 안정화를 위해 잠시 대기 (장치 초기화 시간)
time.sleep(2)
print("시리얼 데이터 수신 시작 (Ctrl+C로 종료)")

# 분류 모델 로드 (모델 파일 경로는 실제 파일 경로로 수정 필요)
model_path = 'C:\Users\sypza\RNN_Keepyourheeeeadup\model\keepheeead-model-0142.pkl'  # 모델 경로
try:
    classifier = joblib.load(model_path)
    print("모델 로드 성공")
except Exception as e:
    print("모델 로드 실패:", e)
    ser.close()
    exit()

t = 1

try:
    while True:
        # 한 줄씩 읽어 들임 (바이트 형태)
        try:
            raw_line = ser.readline()
            decoded_line = raw_line.decode('utf-8', errors='replace').strip()

            # 구분자 '|'를 기준으로 데이터 분리
            parts = decoded_line.split('|')
            if len(parts) < 2:
                # 구분자가 없으면 데이터를 무시
                continue
            line, buttonState = parts[0], parts[1]
        except Exception as e:
            print("데이터 처리 중 에러:", e)
            continue

        # 문자열이 있을 경우 처리
        if line:
            values = line.split(',')
            if len(values) == 13:
                try:
                    # 숫자 데이터 변환; 변환 실패 시 해당 행 무시
                    roll1, pitch1, roll2, pitch2, roll3, pitch3, roll4, pitch4, \
                    roll5, pitch5, roll6, pitch6, FSR = map(float, line.split(','))
                    FSR = int(FSR)

                    # 모델 입력 데이터 준비
                    input_features = np.array([roll1, pitch1, roll2, pitch2, roll3, pitch3, 
                                                roll4, pitch4, roll5, pitch5, roll6, pitch6, FSR]).reshape(1, -1)

                    # 분류 모델 적용
                    predicted_class = classifier.predict(input_features)[0]
                except ValueError:
                    continue

                # 터미널에 출력
                print(t, roll1, pitch1, roll2, pitch2, roll3, pitch3, roll4, 
                      pitch4, roll5, pitch5, roll6, pitch6, FSR, predicted_class)

                t += 1

except KeyboardInterrupt:
    print("\n프로그램 종료합니다.")

finally:
    ser.close()
    print("끝~!")
