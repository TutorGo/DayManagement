import sys
from datetime import datetime
from functools import partial
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QTextEdit, \
    QDialog


class DayManagement(QWidget):
    am_pm_toggle_value = 'PM'
    task_list = []

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

        # task 라벨 추가
        self.set_task_text_label = QLabel("TASK")
        # set_task_text_label 중앙 정렬
        self.set_task_text_label.setAlignment(Qt.AlignCenter)
        # grid 레이아웃에 5행에 정렬
        grid.addWidget(self.set_task_text_label, 5, 0)
        # task 내용 text 설정
        self.set_task_text = QTextEdit()
        # grid 레이아웃에 task text 6행에 정렬
        grid.addWidget(self.set_task_text, 6, 0)

        # 시간과 할일을 저장하는 save 버튼
        self.task_save_button = QPushButton("save")
        # task_save_button을 def task_save 함수랑 연결
        self.task_save_button.clicked.connect(self.task_save)
        # self.task_save_button을 gird 레이아웃에 7행에 정렬
        grid.addWidget(self.task_save_button, 7, 0)

        # 지금까지 저장한 task 목록을 보여주는 버튼
        self.see_task_list_button = QPushButton("task list")
        # see_task_list 함수랑 see_task_list_button 버튼을 연결
        self.see_task_list_button.clicked.connect(self.see_task_list)
        # see_task_list_button 8행에 정렬
        grid.addWidget(self.see_task_list_button, 8, 0)
        # am_or_pm_toggle_button을 클릭하면 self.am_pm_toggle함수를 실행한다
        self.am_or_pm_toggle_button.clicked.connect(self.am_pm_toggle)
        self.setLayout(grid)
        self.setGeometry(300, 300, 540, 300)
        self.show()

    def see_task_list(self):
        '''
        새로운 윈도우 창을 여는 함수로 TaskList를 불러와서 show 새로운 창을 염
        '''
        self.see_task_new_window = TaskList()
        self.see_task_new_window.show()

    def task_save(self):
        '''
        시간과 할일 목록을 저장하는 함수
        '''
        time_and_task = "{hours}:{minutes}:{seconds}\n{task}".format(hours=self.set_time_hours.text(),
                                                                     minutes=self.set_time_minutes.text(),
                                                                     seconds=self.set_time_seconds.text(),
                                                                     task=self.set_task_text.toPlainText())
        # 시간과 할일을 task_list에 저장한다
        self.task_list.append(time_and_task)

        # 시간과 할일을 저장 후에 text 칸을 clear 시킨다
        self.set_time_hours.clear()
        self.set_time_minutes.clear()
        self.set_time_seconds.clear()
        self.set_task_text.clear()
        print(self.task_list)

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


class TaskList(QWidget):
    '''
    할일 목록을 보여주는 새로운 윈도우 클래스
    '''
    # DayManagement의 task_list(할일)을 저장한다
    task_list = DayManagement.task_list

    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()

        print(self.task_list)
        for index, task in enumerate(self.task_list):
            self.task_list_layout = QHBoxLayout()

            self.text = QTextEdit()
            self.task_list_layout.addWidget(self.text)
            self.text.setPlainText(task)
            self.button = QPushButton('delete', self)
            self.button2 = QPushButton('수정', self)
            self.button.clicked.connect(partial(self.taskdelete, self.task_list_layout))
            self.task_list_layout.addWidget(self.button)

            self.grid.addLayout(self.task_list_layout, index, 0)

        self.setLayout(self.grid)
        self.show()

    def task_delete(self, layout):
        while layout.count() > 0:
            item = layout.takeAt(0)
            if not item:
                continue

            w = item.widget()
            if w:
                w.deleteLater()
        self.setGeometry(300, 300, 400, 300)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DayManagement()
    sys.exit(app.exec_())
