import serial
import csv
import time
import msvcrt   
import os  # 파일 및 디렉토리 관리를 위한 os 모듈

data = []
t = 1

# 데이터 폴더 생성
data_folder = 'data'
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# 시리얼 포트 연결 (포트 이름과 baud rate는 환경에 맞게 수정)
try:
    ser = serial.Serial('COM9', 115200, timeout=1)  # 예시: 'COM9' 포트, 115200 baud
except Exception as e:
    print("시리얼 포트 연결 실패:", e)
    exit()

# 시리얼 포트 안정화를 위해 잠시 대기 (장치 초기화 시간)
time.sleep(2)

print("시리얼 데이터 수신 시작 (Ctrl+C로 종료)")

try:
    while True:
        # 한 줄씩 읽어 들임 (바이트 형태)
        line, buttonState = ser.readline().decode('utf-8').strip().split('|')

        # 문자열이 있으면 변수에 저장 후 출력
        if line:
            values = line.split(',')
            if len(values) == 13:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

                roll1, pitch1, roll2, pitch2, roll3, pitch3, roll4, pitch4, roll5, pitch5, roll6, pitch6, FSR = map(float, line.split(','))
                FSR = int(FSR)

                print(t, roll1, pitch1, roll2, pitch2, roll3, pitch3, roll4, pitch4, roll5, pitch5, roll6, pitch6, FSR, buttonState)
                data.append([timestamp, t, roll1, pitch1, roll2, pitch2, roll3, pitch3, roll4, pitch4, roll5, pitch5, roll6, pitch6, FSR, buttonState])
                t += 1
        

except KeyboardInterrupt:
    print("\n프로그램 종료합니다.")
finally:
    ser.close()

# 날짜 및 현재 시각을 파일 이름에 추가 (형식: YYYYMMDD_HHMMSS)
current_datetime = time.strftime("%Y%m%d_%H%M%S")
filename = f"{data_folder}/recorded_data_{current_datetime}.csv"

# 만약 이전에 같은 이름의 파일이 존재한다면 삭제 (옵션)
if os.path.exists(filename):
    os.remove(filename)

# CSV 파일로 데이터 저장
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "No.", "roll1", "pitch1", "roll2", "pitch2", "roll3", "pitch3", "roll4", "pitch4", "roll5", "pitch5", "roll6", "pitch6", "FSR", "gesture"])
    writer.writerows(data)

print(f"Data saved to {filename}")
