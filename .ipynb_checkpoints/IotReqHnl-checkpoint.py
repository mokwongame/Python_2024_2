#IotReqHnl: IoT request handler
from http.server import SimpleHTTPRequestHandler
import time

# class 뒤 (...) 의미: 객체 지향의 상속
class IotReqHnl(SimpleHTTPRequestHandler):
    # GET method의 override(덮어쓰기)
    def do_GET(self):
        # URL 사용하여 GET method 처리
        print('path = ' + self.path) # path: IP 주소 다음에 오는 URL 정보
        if self.path == '/': self.writeHome()

    def writeHome(self):
        # 재빠르게 header로 response를 전송
        self.send_response(200) # 성공(OK)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        # HTML 전송
        nTime = time.time()
        html = '<html>'
        html += '<head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>IoT Web Server</title>'
        html += '</head><body>'
        html += '<div>IoT System Design</div>'
        html += f'<div>현재 날짜와 시간은 {time.ctime(nTime)}입니다.</div>'
        html += '</body></html>'
        self.wfile.write(html.encode()) # Unicode(가변 코드) -> byte(고정 코드; 크기는 1byte) 변경
        
        





