import Bjorntest
b=Bjorntest.Hittite()

x=raw_input('Enter command: ')
while x!='exit':
    if x == 'on':
        b.on()
    if x == 'off':
        b.off()
    if x == 'set freq':
        f = raw_input('Enter frequency: ')
        b.set(f)
    if x == 'set pow':
        p = raw_input('Enter power: ')
        b.set_power(p)
    if x == 'reset':
        b.reset()
    if x=='sweep':
        start = raw_input('Enter start: ')
        end = raw_input('Enter end: ')
        b.sweep(start, end)
    if x=='help':
        print 'Valid commands are: '
        print 'on: turns on'
        print 'off: turns off'
        print 'set freq: asks for frequency and sets it'
        print 'set pow: asks for power and sets it.'
        print 'reset: resets Hittite'
        print 'sweep: asks for start and end and immediately sweeps'
	print 'exit: exits program.'
        print 'help: displays this'
    x=raw_input('Enter command: ')
