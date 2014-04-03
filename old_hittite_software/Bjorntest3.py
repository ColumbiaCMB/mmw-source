class Hittite:
    def connect(self):
        ''' Creates the socket object. Defines host and port used.'''
        import socket
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('192.168.000.71',50000))
        s.settimeout(0.5)
        self.s = s
        return
    def disconnect(self):
        self.s.close()
    def ident(self):
        self.connect()
        response = ''
        try:
            self.s.send('*IDN?\r')
            response = self.s.recv(10000)
        except Exception:
            print
        self.disconnect()
        return response
    def reset(self):
        self.connect()
        response=''
        try:
            self.s.send('*RST\r')
            response =self.s.recv(10000)
        except Exception:
            print
        self.disconnect()
        return response
    def on(self):
        self.connect()
        response = ''
        try:
            self.s.send('OUTP ON\r')
            response = self.s.recv(10000)
        except Exception:
            print
        self.disconnect()
        return response
    def off(self):
        self.connect()
        response = ''
        try:
            self.s.send('OUTP OFF\r')
            response = self.s.recv(10000)
        except Exception:
            print
        self.disconnect()
        return response
    def check(self):
        self.connect()
        response = ''
        try:
            self.s.send('OUTP?\r')
            response =self.s.recv(10000)
        except Exception:
            print
        self.disconnect()
        if response == '1\n':
            onoff = 'On'
        elif response == '0\n':
            onoff = 'Off'
        else:
            onoff = 'Error'
        return onoff
    def set_power(self,power):
        self.connect()
        response = ''
        try:
            self.s.send('pow:mode fix\r')
            # This terminates any sweep mode that may exist.
            self.s.send('POW '+power+'\r')
            self.s.send('POW?\r')
            response =self.s.recv(10000)
        except Exception:
            print
        self.disconnect()
        return response
    def set_f(self):
        # Used for testing frequency out of sweep mode.
        self.connect()
        response = ''
        try:
            self.s.send('sour:freq:fix 8e9\r')
            # According to the Hittite guide (page 31) this should work. However,
            # after a sweep it fails to work. Hence the workaround.
            self.s.send('freq?\r')
            response =self.s.recv(10000)
        except Exception:
            print
        self.disconnect()
        return response
    def set_freq(self, f):
        self.connect()
        response = ''
        try:
            self.s.send('freq:mode cw\r')
            # This terminates any sweep mode that may exist.
            self.s.send('freq '+f+'\r')
            self.s.send('freq?\r')
            response =self.s.recv(10000)
        except Exception:
            print
        self.disconnect()
        return response
    def sweep(self,a,b):
        self.connect()
        response = ''
        try:
            self.s.send('pow:mode fix\r')
            # This terminates any sweep mode that may exist.
            self.s.send('freq:star '+a+'; stop '+b+';step 1e7;mode swe\r')
            self.s.send('trig: source bus\r')
            self.s.send('init\r')
            self.s.send('TRIG\r')
            response=self.s.recv(10000) 
        except Exception:
            print
        self.disconnect()
        return response
    def sweep_power(self,a,b):
        self.connect()
        response = ''
        try:
            self.s.send('freq:mode cw\r')
            # This terminates any sweep mode that may exist.
            self.s.send('pow:star '+a+'; stop '+b+';step .1;mode swe\r')
            self.s.send('trig: source bus\r')
            self.s.send('init\r')
            self.s.send('TRIG\r')
            response=self.s.recv(10000) 
        except Exception:
            print
        self.disconnect()
        return response
