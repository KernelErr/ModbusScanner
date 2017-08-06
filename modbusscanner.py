import multiprocessing
import os
import struct
import sys
from pymodbus.pdu import ModbusRequest, ModbusResponse
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

port = 502
lock = multiprocessing.Lock()

class CustomModbusRequest(ModbusRequest):

    function_code = 1

    def __init__(self, address):
        ModbusRequest.__init__(self)
        self.address = address
        self.count = 1

    def encode(self):
        return struct.pack('>HH', self.address, self.count)

    def decode(self, data):
        self.address, self.count = struct.unpack('>HH', data)

    def execute(self, context):
        if not (1 <= self.count <= 0x7d0):
            return self.doException(merror.IllegalValue)
        if not context.validate(self.function_code, self.address, self.count):
            return self.doException(merror.IllegalAddress)
        values = context.getValues(self.function_code, self.address, self.count)
        return CustomModbusResponse(values)

def read_onereg_attempt(addr):
    try:
        global port
        with ModbusClient(addr, port) as client:
            request = CustomModbusRequest(0)
            result  = client.execute(request)
            print '[*] Message from server :',str(result)
            if "ReadBitResponse" in str(result):
                return True
            else:
                return False
    except:
        return False

def attempt(addr):
    print '[*] Attempt reading from ', addr
    if read_onereg_attempt(addr):
        print '[+] Success! IP:', addr
        output = open('successlist','a')
        output.write(str(addr))
        output.write("\n")
    else:
        print '[-] Failed. IP:', addr

def main():
    hostsfile = open('scan','r')
    hosts = []
    for line in hostsfile.readlines():
        addr = line.strip('\r').strip('\n')
        hosts.append(addr)
    pool = multiprocessing.Pool(processes=50)
    pool.map(attempt,hosts)

if __name__ == '__main__':
    main()
