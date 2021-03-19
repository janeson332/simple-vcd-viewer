from PyQt5.QtCore import QObject, pyqtSlot,QModelIndex
from PyQt5.QtWidgets import QFileDialog

from model.main_model import MainModel


class MainController(QObject):

    def __init__(self,model:MainModel):
        super().__init__()

        self._mainModel = model

    @pyqtSlot(str)
    def setNewFileName(self,value):
        self._mainModel.readFromNewFile(value)
    
    @pyqtSlot(list)
    def onAddSignalClicked(self,index:list[QModelIndex]):
        for i in index:
            signalName = self._mainModel.vcdSignalNameListModel._signalNames[i.row()]
            self._mainModel.addPlotSignal(signalName)

    @pyqtSlot(list)
    def onAddPWLClicked(self,index:list[QModelIndex]):
        if len(index)!=2:
            self._mainModel.warningMessageRaised.emit("On adding pwl only add a and b value")

        name_a = None 
        name_b = None
        for i in index:
            signalName = self._mainModel.vcdSignalNameListModel._signalNames[i.row()]
            if(signalName.find(".a")>=0):
                name_a = signalName

            if(signalName.find(".b")>=0):
                name_b = signalName

        if(name_a is not None and name_b is not None):
            self._mainModel.addPWLPlotSignal(name_a,name_b)
        else:
            self._mainModel.warningMessageRaised.emit("slope and/or offsent of pwl not found")

            

    def onPlotClicked(self):
        self._mainModel.plotCurrentSignals()