#IotReqHnl: IoT request handler
from http.server import SimpleHTTPRequestHandler
from PythonHub import PythonHub
import time

# class 뒤 (...) 의미: 객체 지향의 상속
class IotReqHnl(SimpleHTTPRequestHandler):
    # GET method의 override(덮어쓰기)
    def do_GET(self):
        # URL 사용하여 GET method 처리
        print('path = ' + self.path) # path: IP 주소 다음에 오는 URL 정보
        if self.path == '/': self.writeHome()
        else: self.writeNotFound()

    def writeHead(self, code):
        self.send_response(code) # 성공(OK)
        self.send_header('content-type', 'text/html')
        self.end_headers()

    def writeHtml(self, html):
        self.wfile.write(html.encode())
    
    def writeHome(self):
        # 재빠르게 header로 response를 전송
        self.writeHead(200)
        # HTML 전송
        # 현재 서버의 인스턴스 이름은 server로 고정됨; 변경할 수 없음
        nTime = time.time()
        html = '<html>'
        html += '<head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>IoT Web Server</title>'
        html += '</head><body>'
        html += '<div>IoT System Design</div>'
        html += '<div>이름:목원이</div>'
        html += '<div><img src="https://upload.wikimedia.org/wikipedia/commons/e/ed/Research_topics_in_Business-applied_Artificial_Intelligence.png" width="300" height="300"/></div>'
        html += f'<div>현재 날짜와 시간은 {time.ctime(nTime)}입니다.</div>'
        html += f'<div>전압을 측정한 회수는 {self.server.gateway.countVoltTable()}번입니다.</div>'
        html += '</body></html>'
        self.writeHtml(html) # Unicode(가변 코드) -> byte(고정 코드; 크기는 1byte) 변경

    def writeNotFound(self):
        self.writeHead(404)
        html = '<html>'
        html += '<head>'
        html += '<meta http-equiv="content-type" content="text/html" charset="UTF-8">'
        html += '<title>페이지 없음</title>'
        html += '</head><body>'
        html += f'<div>요청하신 페이지 {self.path}가 없습니다.</div>'
        html += '</body></html>'
        self.writeHtml(html)
        
        





