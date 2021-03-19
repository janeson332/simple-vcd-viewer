from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtCore import Qt,QAbstractListModel,QModelIndex
from PyQt5.QtWidgets import QMessageBox
from copy import deepcopy

from lib.vcdvcd.vcdvcd import VCDVCD
from model.vcd_handler import VCDHandler
from model.vcd_datatypes import vcd_timescale,vcd_tv_to_continous_time,vcd_pwl_tv_to_cont
import matplotlib.pyplot as plt


class VCDSignalNameListModel(QAbstractListModel):
    def __init__(self, parent=None):
        super(QAbstractListModel,self).__init__(parent=parent)
        self._signalNames = []

    def data( self,index:QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if role==Qt.DisplayRole:
            return self._signalNames[index.row()]

    def rowCount(self,index):
        return len(self._signalNames)

    @property
    def signalNames(self):
        return self._signalNames

    @signalNames.setter
    def signalNames(self,data):
        self.modelAboutToBeReset.emit()
        self._signalNames = list(data)
        self.modelReset.emit()

class PlotSignaListModel(QAbstractListModel):
    def __init__(self, parent=None):
        super(QAbstractListModel,self).__init__(parent=parent)
        self._data = {}

    def data( self,index:QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if role==Qt.DisplayRole:
            return list(self._data.keys())[index.row()]
          
          
    def rowCount(self,index):
        return len(self._data.keys())

    def addSignal(self,name,tv):
        self.modelAboutToBeReset.emit()
        self._data[name]=tv
        self.modelReset.emit()
        

    def reset(self):
        self.modelAboutToBeReset.emit()
        self._data = {}
        self.modelReset.emit()
    

class MainModel(QObject):
    fileChanged = pyqtSignal(str)
    timescaleChanged = pyqtSignal(str)
    warningMessageRaised = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self._currentFile = ""
        self.vcdSignalNameListModel = VCDSignalNameListModel()
        self.plotSignalListModel    = PlotSignaListModel()

        self._timescale = vcd_timescale()

        self._vcdHandler = VCDHandler()

    @property
    def currentFile(self):
        return self._currentFile
    
    @currentFile.setter
    def currentFile(self,value):
        if(value != self._currentFile):
            self._currentFile = value
            self.fileChanged.emit(self._currentFile)
    
    def readFromNewFile(self,value):
        self.currentFile = value
        if(value is not None and value != ""):
            self._selectedFile = value
            
            # read vcd file
            self._vcdHandler.filename = self._selectedFile
            if self._vcdHandler.read_vcd_file():
                self.vcdSignalNameListModel.signalNames = self._vcdHandler.signal_names
                self.timescale = self._vcdHandler.timescale
            else:
                self.currentFile = ""
                self.warningMessageRaised.emit("Error during reading of vcd file. Maybe wrong file format")

    def addPlotSignal(self,name):
        if(name in self._vcdHandler.signal_names):
            vcd_tv = self._vcdHandler._tv_signals[name]
            tv = vcd_tv_to_continous_time(vcd_tv)
            t = tv[0]*self._timescale.n_to_time()
            tv = (t,tv[1])
            self.plotSignalListModel.addSignal(name,tv)

    def addPWLPlotSignal(self, name_a,name_b):
        if(name_a in self._vcdHandler.signal_names and name_b in self._vcdHandler.signal_names):
            vcd_tv = self._vcdHandler.build_pwl_vcd(name_a,name_b)
            tv = vcd_pwl_tv_to_cont(vcd_tv)
            t = tv[0]*self._timescale.n_to_time()
            tv = (t,tv[1])
            name = name_a[0:-2]
            self.plotSignalListModel.addSignal(name,tv)

    def plotCurrentSignals(self):
        self.plotData(self.plotSignalListModel._data)
        self.plotSignalListModel.reset()

    def plotData(self,data):
        plt.figure()
        names = data.keys()
        for name in names:
            plt.plot(*(data[name]))
        
        plt.legend(names)
        plt.show()




    @property
    def timescale(self):
        return self._timescale

    @timescale.setter
    def timescale(self,value):
        if(isinstance(value,vcd_timescale)):
            self._timescale = value
            self.timescaleChanged.emit(str(self._timescale))
            