import sys
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout


class DayManagement(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()

        self.setLayout(grid)
        self.setGeometry(300, 300, 540, 300)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DayManagement()
    sys.exit(app.exec_())