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
    
    # 생성자(constructor)
    def __init__(self, portName = __defPortName, portSpeed = __defPortSpeed):
        self.ard = Serial(portName, portSpeed)
        
    #소멸자(destructor)
    def __del__(self):
        if self.ard.isOpen(): # Serial이 열려있으면(is open?)
            ard.close() # Serial 닫기(close)
    