import serial
import time

class lockinController():
### Initialization ###
    def __init__(self, serial_port='/dev/ttyUSB2', terminator='\n'):
        self.address=serial_port
        self.terminator=terminator
        self.setup_rs232_output()
        
    
    def setup_rs232_output(self):
        ser=serial.Serial(self.address)
        try:
            ser.write('OUTX 0'+self.terminator)
        except Exception as e:
            print e
            raise e
        finally:
            ser.close()

### Basic send and receive methods ###

    def send(self,msg):
        ser=serial.Serial(self.address)
        time.sleep(.1)
        try:
            ser.write(msg+self.terminator)
        except Exception as e:
            print e
            raise e
        finally:
            ser.close()

    def send_and_receive(self,msg):
        ser=serial.Serial(self.address,timeout=2)
        time.sleep(.1)
        # This delay is necessary... for some reason. The system behaves very poorly otherwise.
        # Perhaps the serial port takes some time to initialize?
        try:
            ser.write(msg+self.terminator)
            return self.read_until_terminator(ser)
        except Exception as e:
            print e
            raise e
        finally:
            ser.close()

    def read_until_terminator(self,ser):
        message=''
        new_char=None
        while new_char!='\n':
            new_char=ser.read(1)
            if new_char=='':
                # This means ser has timed out. We don't want an unending loop if the terminator has somehow been lost.
                print 'Serial port timed out while reading.'
                break
            message+=new_char
        return message

### Stub methods ###

    def get_data(self):
        return self.send_and_receive('SNAP? 1,2,3,4')

    def get_idn(self):
        return self.send_and_receive('*IDN?')
