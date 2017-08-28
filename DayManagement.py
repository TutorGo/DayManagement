import sys
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit


class DayManagement(QWidget):
    am_pm_toggle_value = 'PM'

    def __init__(self):
        super().__init__()
        # 시작할때 initUI를 불러온다
        self.initUI()

    def initUI(self):
        # 레이아웃은 그리드 레이아웃으로 설정
        grid = QGridLayout()

        # AM_PM_toggle
        # AM 과 PM을 설정하기 위한 토글 라벨을 설정한다
        am_or_pm_toggle_label = QLabel("AM PM Toggle")
        am_or_pm_toggle_label.setAlignment(Qt.AlignCenter)
        # AM 과 PM을 설정하기 위해서 버튼을 만든다
        self.am_or_pm_toggle_button = QPushButton("PM")

        # am_or_pm_toggle_label을 grid 레이아웃에 1행에 0열에 설정
        grid.addWidget(am_or_pm_toggle_label, 1, 0)

        # am_or_pm_toggle_button을 grid 레이아웃에 2행에 0열에 설정
        grid.addWidget(self.am_or_pm_toggle_button, 2, 0)
        # am_or_pm_toggle_button을 토글 버튼으로 만든다
        self.am_or_pm_toggle_button.setCheckable(True)

        # TIME 설정
        # 시간을 설정하기 위한 시간 라벨을 설정한다
        set_time_label = QLabel('TIME')
        # set_time_label을 중간으로 설정한다
        set_time_label.setAlignment(Qt.AlignCenter)
        # set_time_label을 grid 레이아웃에 3행 0열에 설정
        grid.addWidget(set_time_label, 3, 0)

        # 수평에 대한 레이아웃 생성
        self.set_time_layout = QHBoxLayout()
        # 중앙을 맞추기 위한 왼쪽 공백 생성
        self.set_time_layout.addStretch()
        # 시간, 분, 초를 받기위한 텍스트
        self.set_time_hours = QLineEdit()
        self.set_time_minutes = QLineEdit()
        self.set_time_seconds = QLineEdit()
        # 시간, 분, 초 텍스트 사이즈 조정
        self.set_time_hours.setMaximumSize(25, 20)
        self.set_time_minutes.setMaximumSize(25, 20)
        self.set_time_seconds.setMaximumSize(25, 20)
        # 시간, 분, 초 를 수평 레이아웃(set_time_layout) 집어넣어 설정함
        self.set_time_layout.addWidget(self.set_time_hours)
        self.set_time_layout.addWidget(QLabel(':'))
        self.set_time_layout.addWidget(self.set_time_minutes)
        self.set_time_layout.addWidget(QLabel(':'))
        self.set_time_layout.addWidget(self.set_time_seconds)
        # 중앙을 맞추기 위한 오른쪽 공백 생성
        self.set_time_layout.addStretch()

        # set_time_layout를 grid레이아웃에 추가함
        grid.addLayout(self.set_time_layout, 4, 0)

        self.task_save_button = QPushButton("save")
        self.task_save_button.clicked.connect(self.task_save)

        grid.addWidget(self.task_save_button, 5, 0)

        # am_or_pm_toggle_button을 클릭하면 self.am_pm_toggle함수를 실행한다
        self.am_or_pm_toggle_button.clicked.connect(self.am_pm_toggle)
        self.setLayout(grid)
        self.setGeometry(300, 300, 540, 300)
        self.show()

    def task_save(self):
        now = datetime.today()
        now_hours = now.hour
        print(now_hours)
        print(self.set_time_hours.text(), self.set_time_minutes.text(), type(self.set_time_hours.text()))

    def am_pm_toggle(self, toggle):
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
