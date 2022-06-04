import RPi.GPIO as GPIO
import time
import picamera
import urllib.request
import datetime
import os


GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

count =0
n_d = 0
try :
    while True :
        if GPIO.input(14) == True :
            ctm = datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
            print("Shock Detected")
            count = count +1
            with picamera.PiCamera() as camera :
                camera.start_preview(fullscreen=False, window=(100,20,640,480))
                time.sleep(2)
                camera.capture(f"picture/{ctm}.jpg")
                camera.stop_preview()
        
                
            urllib.request.urlopen(f"http://3.37.62.156:5000/temp_hum?tm={ctm}&count={count}")
            
            a = f'scp -i "/home/pi/iot_collision_detection/oss_key.pem" picture/{ctm}.jpg admin@ec2-3-37-62-156.ap-northeast-2.compute.amazonaws.com:~/'
            os.system(a)
            
            time.sleep(1)
            print("p")
        
        else :
            print("No Detected")
            n_d= n_d+1
            print("n_count = ", n_d)
            time.sleep(1)
            
except KeyboardInterrupt :
    pass
finally:
    print("End of Program")
GPIO.cleanup()