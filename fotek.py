import serial
import time
from crccheck.crc import CrcModbus

class pressureMeter(object):

    def __init__(self, id=1, port='COM6', baudrate=19200):
        self.ser = serial.Serial()
        self.id = id
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = 1
        try:
            self.ser.open()
        except:
            print('rs485 error')
    

    def readSingleAddress(self,address):
        if type(address) is int:
            if address < 13 and address >= 0:
                hexAddress = address.to_bytes(2,'big')
            else:
                print("address is out of range")
                return None
        else:
            print("address is not existed !! ")
            return None
        id = self.id.to_bytes(1,'big')
        writeBuffer = id + b'\x03' + hexAddress + b'\x00\x01'
        crcinst = CrcModbus()
        crcinst.process(writeBuffer)
        crcbytes = crcinst.finalbytes()[::-1]
        writeBuffer = writeBuffer + crcbytes
        # print(f'write = {writeBuffer}')
        try:
            self.ser.write(writeBuffer)
        except Exception as e:
            print(f"Read Single Address Error : {e}")
        temp  = self.ser.read(7)
        addressValue = temp[3]*256+temp[4]
        return addressValue


    def readCV(self):
        temp = self.readSingleAddress(0)      # CV address is 0000H
        if temp != None: 
            value = float(temp)/100
            return value


    def readAL1(self):
        temp = self.readSingleAddress(2)      # AL1 address is 0002H
        if temp != None: 
            value = float(temp)/100
            return value


    def readAL2(self):
        temp = self.readSingleAddress(3)      # AL2 address is 0003H
        if temp != None: 
            value = float(temp)/100
            return value


    def readHYS(self):
        temp = self.readSingleAddress(4)      # HYS address is 0004H
        if temp != None: 
            value = float(temp)/100
            return value


    def readOutputStatus(self):
        temp = self.readSingleAddress(5)      # Output status address is 0005H
        if temp != None: 
            value = float(temp)/100
            return value


    def readZeroPointCorrection(self):
        temp = self.readSingleAddress(6)      # Zero point correction address is 0006H
        if temp != None: 
            value = float(temp)/100
            return value


    def readDisplayErrorCorrection(self):
        temp = self.readSingleAddress(7)      # Display error correction address is 0007H
        if temp != None: 
            value = float(temp)/100
            return value


    def readLck(self):
        temp = self.readSingleAddress(8)      # Display error correction address is 0007H
        if temp != None: 
            value = float(temp)/100
            return value


    def readUt(self):
        temp = self.readSingleAddress(9)
        if temp != None:
            return temp


    def readDt(self):
        temp = self.readSingleAddress(12)      # dt address is 000CH
        if temp != None: 
            return temp


    def checkAddr(self,addr):
        if type(addr) is int:
            if addr < 13 and addr >= 0:
                hexAddress = addr.to_bytes(2,'big')
                return hexAddress
            else:
                print("address is out of range")
                return None
        else:
            print("address is not existed !!")
            return None
        

    def writeSingleAddress(self,addr,value):
        hexAddr = self.checkAddr(addr)
        hexValue = value.to_bytes(2,'big')
        id = self.id.to_bytes(1,'big') 
        writeBuffer = id + b'\x06' + hexAddr + hexValue
        crcinst = CrcModbus()
        crcinst.process(writeBuffer)
        crcbytes = crcinst.finalbytes()[::-1]
        writeBuffer = writeBuffer + crcbytes
        print(f'write = {writeBuffer}')
        try:
            self.ser.write(writeBuffer)
        except Exception as e:
            print(f"Write Single Address Error : {e}")
            return False
        try:
            temp  = self.ser.read(7)
            print(temp)
        except Exception as e:
            print(f'Response error : {e}')
            return False
        return True


    def writeUt(self,value):
        '''
        0 : Bar
        1 : Kg/cm2
        2 : Psi
        3 : KPa
        '''
        temp = self.writeSingleAddress(9,value)
        if temp != None:
            return temp


if __name__=="__main__":
    rs = pressureMeter()
    # rs.writeUt(2)
    time.sleep(1)
    while True:
        print(f'CV = {rs.readCV()}')
        # print(f'AL1 = {rs.readAL1()}')
        # print(f'AL2 = {rs.readAL2()}')
        # print(f'HYS = {rs.readHYS()}')
        # print(f'Output Status = {rs.readOutputStatus()}')
        # print(f'Zero Point Correction = {rs.readZeroPointCorrection()}')
        # print(f'dt = {rs.readDT()}')
        # print("\n")
        time.sleep(1)