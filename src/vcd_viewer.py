import sys
from PyQt5.QtWidgets import QApplication
from views.main_view import MainView
from model.main_model import MainModel
from controllers.main_controller import MainController


class Application(QApplication):
    def __init__(self, argv):
        super(QApplication,self).__init__(argv)
        
        self.model = MainModel()
        self.controller = MainController(self.model)
        self.mainView = MainView(self.model,self.controller)
        self.mainView.show()


if __name__ == "__main__":
    app = Application(sys.argv)
    sys.exit(app.exec_())