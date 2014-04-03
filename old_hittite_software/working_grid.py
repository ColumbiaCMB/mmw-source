from Tkinter import *
import Bjorntest3
machine=Bjorntest3.Hittite()

root=Tk()

def turn_on():
    print "ON"
    machine.on()
def turn_off():
    print "OFF"
    machine.off()
def reset():
    print "RESET"
    machine.reset()
def setf():
    f=freq_entry.get()
    print f
    machine.set_freq(f)
def setp():
    p=pow_entry.get()
    print p
    machine.set_power(p)
def sweep_freq():
    s=start_entry.get()
    f=finish_entry.get()
    print s
    print f
    machine.sweep(s,f)
def sweep_pow():
    sp=start_power_entry.get()
    fp=finish_power_entry.get()
    print sp
    print fp
    machine.sweep_power(sp,fp)

on=Button(root,text="ON",width = 10, command=turn_on)
on.grid(row=0,column=1, padx=15,pady=10)#,sticky=W+E+N+S)

off=Button(root,text="OFF",width = 10, command=turn_off)
off.grid(row=0,column=2, padx=15,pady=10)

reset=Button(root,text="RESET",width = 10, command=reset)
reset.grid(row=0,column=3, padx=15,pady=10)

set_pow=Button(root,text="Set",command=setp)
set_pow.grid(row=1,column=3, padx=15,pady=10)

set_freq=Button(root,text="Set",command=setf)
set_freq.grid(row=2,column=3, padx=15,pady=10)

sweep=Button(root,text="Sweep Frequency",command=sweep_freq)
sweep.grid(row=3,column=3, padx=15,pady=10)

sweeppower=Button(root,text="Sweep Power",command=sweep_pow)
sweeppower.grid(row=4,column=3, padx=15,pady=10)

pow_entry=Entry(root, width=15)
pow_entry.grid(row=1,column=1,columnspan=2)

freq_entry=Entry(root, width=15)
freq_entry.grid(row=2,column=1,columnspan=2)

start_entry=Entry(root, width=15)
start_entry.grid(row=3,column=1,columnspan=2, sticky=W)

finish_entry=Entry(root, width=15)
finish_entry.grid(row=3,column=1,columnspan=2, sticky=E)

start_power_entry=Entry(root, width=15)
start_power_entry.grid(row=4,column=1,columnspan=2, sticky=W)

finish_power_entry=Entry(root, width=15)
finish_power_entry.grid(row=4,column=1,columnspan=2, sticky=E)

Label(root,text="Power:").grid(row=1,column=0, padx=15)
Label(root,text="Frequency:").grid(row=2,column=0, padx=15)
Label(root,text="Frequency Range:").grid(row=3,column=0, padx=15)
Label(root,text="Power Range:").grid(row=4,column=0, padx=15)

mainloop()
