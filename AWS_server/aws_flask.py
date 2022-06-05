# aws 서버내의 flask 운용
from flask import Flask
from flask import request
 
# Flask 인스턴스 생성 "__name__"은 모듈의 이름 
app = Flask(__name__)

@app.route("/") # 데코레이터를 이용하여 라우팅 경로 지정 
def home():
    html = "<html><head></head><body>"
    html += "<h1>hello,raspberry pi!</h1>"
    html += "</body></html>"

    return html

@app.route("/collision") # /collision 주소로 들어왔을때 
def collect_collsion():
    tm = request.args.get("tm") #url에서 받은 정보 저장 
    count = request.args.get("count") #url에서 받은 정보 저장 
    # collison_detection.csv파일이 없다면 생성하고 있다면 열어준다. 
    # with 문은 작업 블록을 보호하고 파일을 열고 다는것을 자동으로 처리한다. 
    with open("collision_detection.csv","a", encoding= "utf-8") as fp :
        # 해당 파일에 입력받은 시간과 충격 횟수를 쓴다.
        fp.write(f"time = {tm}, count = {count}\n")
    
    return "OK"
 # 들어올 수 있는 주소, 포트는 5000
if __name__ == "__main__" : 
    app.run(host="0.0.0.0", post = 5000, debug = True)

