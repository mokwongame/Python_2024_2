from serial import Serial
import time

# 파이썬에서 생성자명과 소멸자명은 하나로 정해짐
# 접근 그룹 규칙
# __이름__ -> public group(public:)
# __이름 -> private group(private:)
# self 의미: 현재 인스턴스(instance)의 레퍼런스(reference) -> C++ 기준에서 self = *this
class PythonHub:
    # private 멤버 변수
    __defPortName = 'COM3'
    __defPortSpeed = 9600
    __defWaitTime = 0.1

    # 정적(static) 멤버 함수: 입력에 self가 없음 -> C++에서 static에 해당
    def wait(waitTime = __defWaitTime):
        time.sleep(waitTime)
    
    # 생성자(constructor)
    def __init__(self, portName = __defPortName, portSpeed = __defPortSpeed):
        self.ard = Serial(portName, portSpeed)
        
    #소멸자(destructor)
    def __del__(self):
        if self.ard.isOpen(): # Serial이 열려있으면(is open?)
            self.ard.close() # Serial 닫기(close)

    # Serial Method
    def writeSerial(self, sCmd):
        btCmd = sCmd.encode()
        nWrite = self.ard.write(btCmd)
        self.ard.flush() # 모든 바이트를 출력으로 내보기기
        return nWrite

    def readSerial(self):
        nRead = self.ard.in_waiting
        if nRead > 0:
            btRead = self.ard.read(nRead)
            sRead = btRead.decode()
            return sRead
        else: return ''

    def talk(self, sCmd):
        return self.writeSerial(sCmd + '\n')

    def listen(self):
        PythonHub.wait() # 정적 멤버 접근할 때는 클래스명을 앞에 써줌
        sRead = self.readSerial()
        return sRead.strip() # 문자열 sRead 앞뒤에 공백 제거

    def talkListen(self, sCmd):
        self.talk(sCmd)
        return self.listen()