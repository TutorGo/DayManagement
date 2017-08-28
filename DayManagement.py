import sys
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QPushButton


class DayManagement(QWidget):
    am_pm_toggle_value = 'PM'

    def __init__(self):
        super().__init__()
        # 시작할때 initUI를 불러온다
        self.initUI()

    def initUI(self):
        # 레이아웃은 그리드 레이아웃으로 설정
        grid = QGridLayout()

        # AM 과 PM을 설정하기 위한 토글 라벨을 설정한다
        am_or_pm_toggle_label = QLabel("AM PM Toggle")
        # AM 과 PM을 설정하기 위해서 버튼을 만든다
        self.am_or_pm_toggle_button = QPushButton("PM")
        # am_or_pm_toggle_button을 토글 버튼으로 만든다
        self.am_or_pm_toggle_button.setCheckable(True)

        # am_or_pm_toggle_label을 grid 레이아웃에 1행에 0열에 설정
        grid.addWidget(am_or_pm_toggle_label,1,0)

        # am_or_pm_toggle_button을 grid 레이아웃에 1행에 1열에 설정
        grid.addWidget(self.am_or_pm_toggle_button,1,1)

        # am_or_pm_toggle_button을 클릭하면 self.am_pm_toggle함수를 실행한다
        self.am_or_pm_toggle_button.clicked.connect(self.am_pm_toggle)
        self.setLayout(grid)
        self.setGeometry(300, 300, 540, 300)
        self.show()

    def am_pm_toggle(self,toggle):
        '''
        self.am_or_pm_toggle_button을 클릭하면 실행되는 함수로 AM PM을 설정한다
        '''
        if toggle:
            # am_or_pm_toggle_buotton버튼의 텍스를 AM으로 변경
            self.am_or_pm_toggle_button.setText('AM')
            self.am_pm_toggle_value = 'AM'
        else:
            # am_or_pm_toggle_buotton버튼의 텍스를 PM으로 변경
            self.am_or_pm_toggle_button.setText('PM')
            self.am_pm_toggle_value = 'PM'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DayManagement()
    sys.exit(app.exec_())