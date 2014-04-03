import serial
import time

class lockinController():
	def __init__(self, serial_port='/dev/ttyUSB2', terminator='\r'):
		self.address=serial_port
		self.setup_rs232_output()
		self.terminator='\r'
	
	def setup_rs232_output(self):
		ser=serial.Serial(self.address)
		try:
			ser.write('OUTX 0\r')
		except Exception as e:
			print e
			raise e
		finally:
			ser.close()

	def send(self,msg):
		ser=serial.Serial(self.address)
		try:
			ser.write(msg+self.terminator)
		except Exception as e:
			print e
			raise e
		finally:
			ser.close()

	def response(self,msg):
		ser=serial.Serial(self.address,timeout=2)
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
		metatimeout=3.0
		while new_char!=self.terminator:
			new_char=ser.read(1)
			if new_char=='':
				# This means ser has timed out. We don't want an unending loop if the terminator has somehow been lost.
				print 'Serial port timed out while reading.'
				break
			message+=new_char
		return message


	def receive(self):
		# This doesn't work. From my observations, it seems that a serial port cannot be closed between writing and reading.
		ser=serial.Serial(self.address, timeout=1)
		try:
			print ser.read(50)
		except Exception as e:
			print e
			raise e
		finally:
			ser.close()
