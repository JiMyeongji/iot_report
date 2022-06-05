# 라즈베리파이에서 센서를 제어하기 위한 flask 운용 

from flask import Flask
# template 화된 html 페이지를 렌더링 한다. 
from flask import render_template 
# 서브프로세스 패키지를 이용해서 센서제어를 한다. 
import subprocess

# Flask 인스턴스 생성 "__name__"은 모듈의 이름 
app = Flask(__name__)

# 초기값 설정 
proc = -1

# template 화된 html 페이지를 렌더링 한다. 
@app.route("/") # 데코레이터를 이용하여 라우팅 경로 지정 
def index():
    return render_template('control_panel.html')


@app.route("/on") #on일 때 
def on():
    global proc # 위에 있는 proc 변수를 사용한다 
    if proc == -1:
        # 해당 프로그램의 프로세스를 생성하고, 이에 대한 표준 파일 기술자가 생성 
        proc = subprocess.Popen(["python3", "./shock_sen.py"])
    return render_template('control_panel.html')

@app.route("/off") #off일 때 
def off():
    global proc
    if proc != -1:
        proc.kill() # 해당 프로세스를 닫을 때는 kill 메소드를 호출 
        proc =-1
    return render_template('control_panel.html')    



# 모듈을 import 해서 사용하는 경우인지 직접 실행한 경우인지를 구분 
if __name__ == "__main__" :
    try :
        # 들어올 수 있는 주소, 포트는 5000
        app.run(host="0.0.0.0", port = 5000, debug = True)
    except KeyboardInterrupt:
        pass
    finally:
        if proc != -1 :
            proc.kill()
            proc = -1