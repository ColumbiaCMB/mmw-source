from gui.basic_sweep_ui import Ui_SweepDialog

from PyQt4.QtCore import *
from PyQt4.QtGui import *


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import IPython
import time
import bisect

import threading

import sys

import mmw_sweep_data

import hittite_controller
import lockin_controller


class SweepDialog(QDialog,Ui_SweepDialog):
    def __init__(self,  qApp, parent=None):
        super(SweepDialog, self).__init__(parent)
        self.__app = qApp
        self.setupUi(self)
        
        self.lockin = lockin_controller.lockinController(serial_port="COM6")
        self.hittite = hittite_controller.hittiteController()
        self.dpi = 72
        self.fig = Figure((9.1, 5.2), dpi=self.dpi)
#        self.fig = Figure(dpi=self.dpi)
        self.plot_layout = QVBoxLayout(self.plot_group_box)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.plot_group_box)
        self.canvas.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.plot_layout.addWidget(self.canvas)
        self.axes = self.fig.add_subplot(211)
        self.axes.set_xlabel('GHz')
        self.axes.set_ylabel('dB')
        self.axes.grid(True)
        self.axes2 = self.fig.add_subplot(212)
        # Use matplotlib event handler
        #self.canvas.mpl_connect('pick_event', self.onclick_plot)
        #self.canvas.mpl_connect('button_release_event', self.onclick_plot)
        self.mpl_toolbar = NavigationToolbar(self.canvas,self.plot_group_box) #self.adc_plot_box)
        self.plot_layout.addWidget(self.mpl_toolbar)
        
            
        self.line = None
        self.phline = None
        self.line2 = None
        self.phline2 = None
        self.peakline = None
        self.psd_text = None
        self.selection_line = None
        self.sweep_data = None
        self.fine_sweep_data = None
        
        self.progress_value = 0
        self.total_subsweeps = 1
        self.current_subsweep = 0
        
        
        self.abort_requested = False
        self.sweep_thread = None
        
        self.push_abort.clicked.connect(self.onclick_abort)
        self.push_start_sweep.clicked.connect(self.onclick_start_sweep)
        self.push_start_fine_sweep.clicked.connect(self.onclick_start_fine_sweep)
        self.push_save.clicked.connect(self.onclick_save)
        self.line_npoints.textEdited.connect(self.recalc_spacing)
        self.line_span_hz.textEdited.connect(self.recalc_spacing)
        #self.tableview_freqs.itemChanged.connect(self.freq_table_item_changed)
        #self.spin_subsweeps.valueChanged.connect(self.onspin_subsweeps_changed)
        self.push_add_resonator.clicked.connect(self.onclick_add_resonator)
        self.push_clear_all.clicked.connect(self.onclick_clear_all)
        self.check_use_cal.stateChanged.connect(self.oncheck_use_cal)
        self.push_save_res.clicked.connect(self.onclick_save_res)
        self.push_load_res.clicked.connect(self.onclick_load_res)
        
        self.logfile = None
        self.fresh = False
        self.fine_sweep_data = None
        #self.recalc_spacing('')
        
        
        QTimer.singleShot(1000, self.update_plot)
        
    def update_plot(self):
        if self.fresh and (self.sweep_data is not None):
            x = self.sweep_data.mmw_freq_ghz
            y = self.sweep_data.power_dbm
#            if self.check_use_cal.isChecked():
#                cal = np.interp(x,self.cal_freq,self.cal_mag)
#                cal *= 10**(-(self.ri.adc_atten+self.ri.dac_atten-31)/20.0)
#            else:
#                cal = 1.0
            if self.line:
                self.line.set_xdata(x)
                self.line.set_ydata(y)
                    
            else:
                self.line, = self.axes.plot(x,y,'b.-',alpha=1.0)
            self.canvas.draw()
            self.fresh = False
        
        self.progress_sweep.setValue(int(self.progress_value*100))
        QTimer.singleShot(1000, self.update_plot)
        
    @pyqtSlot(int)
    def oncheck_use_cal(self,val):
        self.fresh = True
                
    @pyqtSlot(int)
    def onspin_subsweeps_changed(self, val):
        step = 0.0625*2**self.combo_step_size.currentIndex()
        substep = step/float(val)
        nsamp = np.ceil(np.log2(self.ri.fs/substep))
        if nsamp < 18:
            nsamp = 18
        self.label_coarse_info.setText("Spacing: %.3f kHz using 2**%d samples" % (substep*1000,nsamp))
    @pyqtSlot()
    def onclick_add_resonator(self):
        if self.selected_idx is not None:
            if self.selected_sweep == 'coarse':
                freq = self.sweep_data.freqs[self.selected_idx]
            else:
                freq = self.fine_sweep_data.freqs[self.selected_idx]
        reslist = self.reslist.tolist()
        bisect.insort(reslist,freq)
        self.reslist = np.array(reslist)
        self.refresh_freq_table()
        
    @pyqtSlot()
    def onclick_save_res(self):
        fname = str(QFileDialog.getSaveFileName(self, "Save resonators as:",".", "Numpy (*.npy)"))
        np.save(fname,self.reslist)
    
    @pyqtSlot()
    def onclick_load_res(self):
        fname = str(QFileDialog.getOpenFileName(self, "Load resonators from:",".", "Numpy (*.npy)"))
        if fname:
            reslist = np.load(fname)
            self.reslist = reslist
            self.refresh_freq_table()
            
    @pyqtSlot()
    def onclick_clear_all(self):
        self.reslist = np.array([])
        self.refresh_freq_table()
    @pyqtSlot()
    def onclick_save(self):
        if self.logfile:
            self.logfile.close()
            self.logfile = None
            self.push_save.setText("Start Logging")
            self.line_filename.setText('')
        else:
            self.logfile = data_file.DataFile()  
            self.line_filename.setText(self.logfile.filename)
            self.push_save.setText("Close Log File")
    @pyqtSlot()
    def onclick_abort(self):
        self.abort_requested = True
        
    @pyqtSlot(str)
    def recalc_spacing(self,txt):
        msg = None
        span = None
        npoint = None
        try:
            span = float(self.line_span_hz.text())
            if span <= 0:
                raise Exception()
        except:
            msg = "span invalid"
        try:
            npoint = int(self.line_npoints.text())
            if npoint <=0:
                raise Exception()
        except:
            msg = "invalid number of points"
        if msg:
            self.label_spacing.setText(msg)
        else:
            spacing = span/npoint
            samps = np.ceil(np.log2(self.ri.fs*1e6/spacing))
            self.label_spacing.setText("Spacing: %.3f Hz requires 2**%d samples" % (spacing,samps))
    def sweep_callback(self,block):
        self.sweep_data.add_block(block)
        self.fresh = True
        self.progress_value = (block.progress + self.current_subsweep)/float(self.total_subsweeps)
#        print "currently have freqs", self.sweep_data.freqs
        return self.abort_requested
    
    def fine_sweep_callback(self,block):
        self.fine_sweep_data.add_block(block)
        self.fresh = True
        self.progress_value = (block.progress + self.current_subsweep)/float(self.total_subsweeps)
        return self.abort_requested
    
    @pyqtSlot()
    def onclick_start_sweep(self):
        if self.sweep_thread:
            if self.sweep_thread.is_alive():
                print "sweep already running"
                return
        self.sweep_thread = threading.Thread(target=self.do_sweep)
        self.sweep_thread.daemon = True
        self.sweep_thread.start()
        
    @pyqtSlot()
    def onclick_start_fine_sweep(self):
        if np.mod(self.reslist.shape[0],4) != 0:
            print "Number of resonators must be divisible by 4! Add some dummy resonators."
        if self.sweep_thread:
            if self.sweep_thread.is_alive():
                print "sweep already running"
                return
        self.sweep_thread = threading.Thread(target=self.do_fine_sweep)
        self.sweep_thread.daemon = True
        self.sweep_thread.start()
        
    def do_sweep(self):
        self.abort_requested = False
        self.sweep_data = mmw_sweep_data.MmwSweepData()
        start = self.spin_start_freq.value()*1e9/12.0
        stop = self.spin_stop_freq.value()*1e9/12.0
        step = 10e6
#        step = 0.0625*2**self.combo_step_size.currentIndex()
        base_freqs = np.arange(start,stop+1e-3,step)
        print base_freqs
        num_freqs = len(base_freqs)
        self.progress_value = 0.0
        self.hittite.on()
        for k in range(num_freqs):
            if self.abort_requested:
                self.hittite.off()
                return
            self.hittite.set_freq(base_freqs[k])
            print base_freqs[k]
            time.sleep(0.2)
            data_string = self.lockin.get_data()
            data_string=data_string.strip('\r')
            data_list=data_string.split(',')
            x = float(data_list[0])
            y = float(data_list[1])
            r = float(data_list[2])
            theta = float(data_list[3])
            print x
            self.sweep_data.add_points(base_freqs[k],x)
            self.fresh = True
            self.progress_value = float(k+1)/float(num_freqs)
        self.abort_requested = False
        self.hittite.off()
        

def main():
    app = QApplication(sys.argv)
    app.quitOnLastWindowClosed = True
    form = SweepDialog(app)

    form.setAttribute(Qt.WA_QuitOnClose)
    form.setAttribute(Qt.WA_DeleteOnClose)
    #form.setWindowTitle("MM" % dcode)
    
    form.show()
#    form.raise_()
#    app.connect(form, SIGNAL('closeApplication'), sys.exit)#app.exit)
#    print "starting ipython"
    IPython.embed()
#    form.exec_()
#    print "after ipython embed"
    if form.logfile:
        form.logfile.close()
    app.exit()
#    sys.exit()
#    app.exec_()
#    print "after app exec"
    
if __name__ == "__main__":
    main()    
