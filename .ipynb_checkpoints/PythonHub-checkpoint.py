from serial import Serial
import time
import psycopg

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

    # DB Method
    def connectDb(self):
        self.conn = psycopg.connect(host='localhost', port='5432', dbname='postgres', user='postgres', password='2024')
        self.cursor = self.conn.cursor()

    def closeDb(self):
        self.cursor.close()
        self.conn.close()

    def writeDb(self, cmd):
        self.cursor.execute(cmd)
        self.conn.commit()

    # Voltmeter Method
    def getVolt(self):
        # C++: try-catch; Python: try-except
        try:
            sVolt = self.talkListen('get volt')
            volt = float(sVolt)
            return volt
        except: # try 코드 블록 실행에서 오류가 난 경우에 실행되는 부분
            print('Serial error: get volt')
            return -1 # 오류난 경우는 음수를 반환

    def insertVoltToTable(self):
        volt = self.getVolt()
        if volt >= 0: # 정상적인 측정
            meas_time = time.time() # 현재 시간을 double로 반환
            self.connectDb()
            # f'...': formatted string -> C의 printf()와 비슷
            self.writeDb(f'INSERT INTO volt_table(id, meas_time, volt) VALUES({int(meas_time)}, {meas_time}, {volt})')
            self.closeDb()
            return True
        else: return False # 측정에 류류
            
    def countVoltTable(self):
        self.connectDb()
        self.writeDb('SELECT COUNT(*) FROM volt_table');
        nCount = self.cursor.fetchone()[0] # fetchone() 함수는 tuple을 반환; [0]을 써서 첫번째 원소를 다시 접근
        self.closeDb()
        return nCount

    def sampleVoltsToTable(self, nCount, delay):
        i = 0
        while i < nCount:
            bResult = self.insertVoltToTable()
            if bResult:
                print(f'i = {i}th meas.')
                i += 1
                PythonHub.wait(delay)

    def loadVoltTable(self):
        self.connectDb()
        self.writeDb('SELECT meas_time, volt FROM volt_table')
        results = self.cursor.fetchall() # results는 record를 원소로 하는 list
        self.closeDb()
        # meas_time, volt 값을 나누어서 반환환
        timeData = () # () 의미: 빈 tuple
        voltData = ()
        for record in results:
            timeData += (record[0],) # (a,) 의미: 원소가 1인 tuple
            voltData += (record[1],)
        return (timeData, voltData)



