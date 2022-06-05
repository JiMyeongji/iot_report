import RPi.GPIO as GPIO   # GPIO를 제어 패키지
import picamera # 카메라 모듈 제어 패키지
import urllib.request # AWS 서버를 쪽에다가 URL을 호출을 할 수 있는 패키지 
import datetime #날짜를 처리하기 위한 패키지 
import time #시간 데이터 다루기 위한 패키지 
import os # 운영체제(쉘 명령어)를 위한 패키지 

GPIO.setmode(GPIO.BCM) # GPIO 넘버 모드를 사용

# GPIO 넘버 중 14번을 사용, 입력 신호 사용, 내장 PUD_DOWN 저항 사용 
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  

count =0 # 충격 횟수 변수 
n_d = 0 # 충격이 감지않은 시간 변수 

try : # 예외 처리 
    while True : # 계속 반복 
        if GPIO.input(14) == True : # 충격 감지 센서에서 충격이 감지 되었을 경우 라즈베리파이로 1(True)가 입력
            ctm = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S') # 입력된 순간의 시간을 저장 
            print("Shock Detected") # 충격이 감지됨을 출력 
            count = count +1 #충격이 감지된 횟수를 저장 
            # picamera 객체 생성 
            with picamera.PiCamera() as camera :
                # 사진 미리 보기 시작 (영상 크기 설정, 화면 위치)  
                camera.start_preview(fullscreen=False, window=(100,20,640,480))
                time.sleep(2)
                #사진 찍히는 순간의 날짜와 시간을 기준으로 picture 폴더에 사진 저장
                camera.capture(f"picture/{ctm}.jpg")
                # 사진 미리 보기 종료  
                camera.stop_preview()
        
            # 명령어를 이용하여 aws서버에 날짜와 충격 횟수를 전송한다. 
            urllib.request.urlopen(f"http://3.37.62.156:5000/collision?tm={ctm}&count={count}")
            
            # a 변수에 scp 명령어를 이용하여 aws서버에 사진 파일을 전송한다. 
            a = f'scp -i "/home/pi/iot_collision_detection/oss_key.pem" picture/{ctm}.jpg admin@ec2-3-37-62-156.ap-northeast-2.compute.amazonaws.com:~/AWS/picture'
            os.system(a)
            # 1초마다 반복 
            time.sleep(1)
            # 완료되면 패스 출력 
            print("pass")
        
        else : # 충격 인식이 안될때 
            print("No Detected")
            n_d= n_d+1 
            print("n_count = ", n_d)
            time.sleep(1)

# 키보드를 이용해서 중단           
except KeyboardInterrupt :
    pass
# 종료되면 End of Program 출력 
finally:
    print("End of Program")

GPIO.cleanup() # GPIO 채널을 초기화 한다 