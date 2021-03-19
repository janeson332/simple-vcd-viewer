
import pathlib
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow
from PyQt5.QtWidgets import QLabel,QFormLayout,QVBoxLayout,QHBoxLayout
from PyQt5.QtWidgets import QPushButton,QLineEdit,QGroupBox,QListView,QAbstractItemView
from PyQt5.QtWidgets import QFileDialog,QMessageBox

from PyQt5.QtCore import Qt,QAbstractListModel,QModelIndex

from controllers.main_controller import MainController
from model.main_model import MainModel

import os
class MainView(QMainWindow):
    def __init__(self,model:MainModel,controller:MainController):
        #super().__init__(parent=parent, flags=flags)
        super(MainView, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(str(pathlib.Path(__file__).parent.absolute())+"/main_view.ui", self) # Load the .ui file
        self._model = model
        self._controller = controller

        #signalname listview
        self.vcdSignalNameListView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.vcdSignalNameListView.setModel(self._model.vcdSignalNameListModel)

        #plot listview
        self.plotSignalListView.setEnabled(False)
        self.plotSignalListView.setModel(self._model.plotSignalListModel)
        

        #open file dialog
        self.btnFileDialog.clicked.connect(self.onOpenFileClicked)
        self.btnAddSignal.clicked.connect(self.onAddSignalClicked)
        self.btnAddPwl.clicked.connect(self.onAddPWLClicked)
        self.btnPlot.clicked.connect(self._controller.onPlotClicked)

        # connect model events
        self._model.fileChanged.connect(self.onFilenameChanged)
        self._model.timescaleChanged.connect(self.onTimeScaleChanged)
        self._model.warningMessageRaised.connect(self.onWarningMessageRaised)

        self.show() # Show the GUI

    def onOpenFileClicked(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"Select VCD file", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self._controller.setNewFileName(fileName)

    def onAddSignalClicked(self,value):
        self._controller.onAddSignalClicked(self.vcdSignalNameListView.selectedIndexes())
        self.vcdSignalNameListView.clearSelection()

    def onAddPWLClicked(self,value):
        self._controller.onAddPWLClicked(self.vcdSignalNameListView.selectedIndexes())
        self.vcdSignalNameListView.clearSelection()


    def onWarningMessageRaised(self,value):
        msgbox = QMessageBox.warning(self,"Warning",value)
        

    def onFilenameChanged(self,value):
        self.lblFileName.setText(value)

    def onTimeScaleChanged(self,value):
        self.lblTimescale.setText(str(value))

