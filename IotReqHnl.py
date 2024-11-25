#IotReqHnl: IoT request handler
from http.server import SimpleHTTPRequestHandler

# class 뒤 (...) 의미: 객체 지향의 상속
class IotReqHnl(SimpleHTTPRequestHandler):
    # GET method의 override(덮어쓰기)
    def do_GET(self):
        # URL 사용하여 GET method 처리
        print(self.path) # path: IP 주소 다음에 오는 URL 정보