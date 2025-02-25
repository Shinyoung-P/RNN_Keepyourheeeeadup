import serial
import csv
import time
import os  # 파일 및 디렉토리 관리를 위한 os 모듈

# 데이터 폴더 생성
data_folder = 'data'
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# 날짜 및 현재 시각을 파일 이름에 추가 (형식: YYYYMMDD_HHMMSS)
current_datetime = time.strftime("%Y%m%d_%H%M%S")
filename = f"{data_folder}/recorded_data_{current_datetime}.csv"

# CSV 파일 열기 (쓰기 모드)
csv_file = open(filename, mode='w', newline='')
writer = csv.writer(csv_file)
writer.writerow(["Timestamp", "No.", "roll1", "pitch1", "roll2", "pitch2", 
                 "roll3", "pitch3", "roll4", "pitch4", "roll5", "pitch5", 
                 "roll6", "pitch6", "FSR", "gesture"])

# 시리얼 포트 연결 (포트 이름과 baud rate는 환경에 맞게 수정)
try:
    ser = serial.Serial('COM18', 115200, timeout=1)  # 예시: 'COM18' 포트, 115200 baud
except Exception as e:
    print("시리얼 포트 연결 실패:", e)
    csv_file.close()
    exit()

# 시리얼 포트 안정화를 위해 잠시 대기 (장치 초기화 시간)
time.sleep(2)
print("시리얼 데이터 수신 시작 (Ctrl+C로 종료)")

t = 1

try:
    while True:
        # 한 줄씩 읽어 들임 (바이트 형태)
        try:
            # decode() 시 errors='replace'를 사용하여 디코딩 문제를 해결
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
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                try:
                    # 숫자 데이터 변환; 변환 실패 시 해당 행 무시
                    roll1, pitch1, roll2, pitch2, roll3, pitch3, roll4, pitch4, \
                    roll5, pitch5, roll6, pitch6, FSR = map(float, line.split(','))
                    FSR = int(FSR)
                except ValueError:
                    continue

                # 터미널에 출력
                print(t, roll1, pitch1, roll2, pitch2, roll3, pitch3, roll4, 
                      pitch4, roll5, pitch5, roll6, pitch6, FSR, buttonState)

                # CSV 파일에 바로 한 행 추가 후 버퍼 플러시(파일에 즉시 쓰기)
                writer.writerow([timestamp, t, roll1, pitch1, roll2, pitch2, 
                                 roll3, pitch3, roll4, pitch4, roll5, pitch5, 
                                 roll6, pitch6, FSR, buttonState])
                csv_file.flush()
                t += 1

except KeyboardInterrupt:
    print("\n프로그램 종료합니다.")

finally:
    ser.close()
    csv_file.close()
    print(f"Data saved to {os.path.abspath(filename)}")
