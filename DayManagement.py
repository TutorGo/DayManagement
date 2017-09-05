import sys
import os
import vlc
from datetime import datetime, time
from functools import partial
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit, QTextEdit, \
    QDialog, QVBoxLayout, QWidgetItem, QMessageBox, QMainWindow
import time as stime

sort_task_list = []


class TimeThread(QThread):
    """
    시간을 설정하는 쓰레드
    """
    # 일반적으로 pyqt5에서는 메인 쓰레드가 아닌 경우에는 pyqt5의 messagebox나 새로운 윈도우창을 키는 행동을 할수가 없다
    # 그래서 message 박스를 불러오는 통로 같은것을 만드는 것
    messagebox = pyqtSignal()
    latest_time_hour = 0
    latest_time_minute = 0

    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    def latest_task_time(self):
        # task_list의 첫 번쨰 키를 : 스플릿 함
        latest_time_keys = list(DayManagement.task_list[0].keys())[0].split(':')
        # self.am_pm_toggle_value가 PM 이면 12를 더해줘여함 datetime에서 1시는 13시로 표현함
        if latest_time_keys[0] == 'PM':
            self.latest_time_hour = int(latest_time_keys[1]) + 12
            self.latest_time_minute = int(latest_time_keys[2])
        # AM 12시는 datetime에서 0시로 표현
        elif latest_time_keys[0] == 'AM' and latest_time_keys[1] == '12':
            self.latest_time_hour = 0
        else:
            self.latest_time_hour = int(latest_time_keys[1])
            self.latest_time_minute = int(latest_time_keys[2])

        return self.latest_time_hour, self.latest_time_minute

    # TimeThread를 .start() 를하면 실행되는 함수
    def run(self):
        # 시간을 체크함
        while True:
            if DayManagement.task_list == []:
                break
            # 제일 처음 task의 시간, 분 을 받아옴
            hour, minute = self.latest_task_time()
            stime.sleep(20)
            # 현재시각이랑 비교해서 현재시각이 더 크면 메세지 박스 불러옴
            if datetime.today().time() >= time(hour, minute):
                # 메인 view에서 messagebox와 connect와 연결된 함수를 싱햄
                print(time(hour, minute))
                print(datetime.today().time())
                self.messagebox.emit()
                # os.system('open /Users/goseonghyeon/study/ScheduleManagement/black.mp3')
                DayManagement.task_list.pop(0)


class DayManagement(QWidget):
    am_pm_toggle_value = 'PM'
    task_list = []
    thread_count = 0

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
        # 시간, 분 을 받기위한 텍스트
        self.set_time_hours = QLineEdit()
        self.set_time_minutes = QLineEdit()
        # 시간, 분 텍스트 사이즈 조정
        self.set_time_hours.setMaximumSize(25, 20)
        self.set_time_minutes.setMaximumSize(25, 20)
        # 시간, 분 수평 레이아웃(set_time_layout) 집어넣어 설정함
        self.set_time_layout.addWidget(self.set_time_hours)
        self.set_time_layout.addWidget(QLabel(':'))
        self.set_time_layout.addWidget(self.set_time_minutes)
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

    def open_message_box(self):
        QApplication.alert(QMessageBox.about(self, 'gdsagdsa', 'gdsaasgdsa'))

    def task_save(self):
        '''
        시간과 할일 목록을 저장하는 함수
        '''
        global sort_task_list
        # am_pm을 받고 ap_or_pm:시간:분 저장
        hours_minutes = "{am_or_pm}:{hours}:{minutes}".format(am_or_pm=self.am_pm_toggle_value,
                                                              hours=self.set_time_hours.text(),
                                                              minutes=self.set_time_minutes.text())
        # am_or_pm:시간:분 : 할일 해서 딕셔너리로 저장
        time_and_task = {hours_minutes: self.set_task_text.toPlainText()}

        # 시간과 할일을 task_list에 저장한다
        self.task_list.append(time_and_task)
        sort_task_list = self.task_list_sort(self.task_list)
        # task_list를 pm

        # 시간과 할일을 저장 후에 text 칸을 clear 시킨다
        self.set_time_hours.clear()
        self.set_time_minutes.clear()
        self.set_task_text.clear()
        # 쓰레드는 한 번만 실행되면 되기 떄문에 카운트가 0일 때만 실행 또는 하나만 있을 떄만 실행
        if self.thread_count == 0 or len(self.task_list) == 1:
            # TimeThread을 할당
            self.time_check_thread = TimeThread()
            # 메인 쓰레드가 종료되면 자식 쓰레드인 self.time_check_thread 종료
            self.time_check_thread.daemon = True
            # TimeThread에 있는 messagebox 시그널과 연결
            self.time_check_thread.messagebox.connect(self.open_message_box)
            # 쓰레드 실행
            self.time_check_thread.start()
            # 한 번만 실행되야 하기때문에 수를 올림
            self.thread_count += 1

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

    def sort_key_dict_fuction(self, task):
        '''
        task_list에 key를 뺴와서 time으로 리턴해서 sort 하는 함수
        '''
        # task의 keys를[0] :를 기준으로 나눠서 am_pm, hour, minute
        time_h_s = list(task.keys())[0].split(':')
        hour = int(time_h_s[1])
        minute = int(time_h_s[2])
        return time(hour, minute)

    def task_list_sort(self, task_list):
        """
        task_list 를 pm, am으로 리스트를 나누어서 정렬함
        """
        pm_task_list = []
        am_task_list = []
        # am 은 pm을 나눠서 각 리스트에 정렬
        for task in task_list:
            task_am_or_pm = list(task.keys())[0].split(':')[0]
            if task_am_or_pm == 'PM':
                pm_task_list.append(task)
            elif task_am_or_pm == 'AM':
                am_task_list.append(task)

        # pm_task_list == [] 이면 am_task_list만 출력
        if pm_task_list == []:
            am_task_list.sort(key=self.sort_key_dict_fuction)
            return am_task_list
        # am_task_list == [] 이면 pm_task_list만 출력
        elif am_task_list == []:
            pm_task_list.sort(key=self.sort_key_dict_fuction)
            return pm_task_list
        # 12시 이상이면 pm_task_list 가 먼저 옴
        elif datetime.today().time().hour >= 12:
            am_task_list.sort(key=self.sort_key_dict_fuction)
            pm_task_list.sort(key=self.sort_key_dict_fuction)
            return pm_task_list + am_task_list
        else:
            am_task_list.sort(key=self.sort_key_dict_fuction)
            pm_task_list.sort(key=self.sort_key_dict_fuction)
            return am_task_list + pm_task_list


class TaskList(QWidget):
    '''
    할일 목록을 보여주는 새로운 윈도우 클래스
    '''
    # 할일 목록을 할당
    global sort_task_list
    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()
        # 할일 목록 하나당 배정함
        for index, task in enumerate(sort_task_list):
            # 각 할 일 마다 am_or_pm, hours, minutes 구함
            am_or_pm, hours, minutes = list(task.keys())[0].split(':')
            # 할 일을 구함
            task = list(task.values())[0]
            # 모든 레이아웃을 감쌀 수직 레이아웃
            self.task_list_wrap_layout = QVBoxLayout()
            # ex)AM:시간:분을 감싸는 수평 레이아웃
            self.task_list_top_layout = QHBoxLayout()
            # 삭제, 수정 버튼을 감싸는 수평 레이아웃
            self.task_list_button_layout = QHBoxLayout()

            # 시간, 분을 넣을 text창
            self.task_time_hours = QLineEdit()
            self.task_time_minutes = QLineEdit()

            # hours을 task_time_hours을 text창에 할당, minutes을 task_time_minutes을 text 창에 할당
            self.task_time_hours.setText(hours)
            self.task_time_minutes.setText(minutes)

            # 크기 조정
            self.task_time_hours.setMaximumSize(25, 20)
            self.task_time_minutes.setMaximumSize(25, 20)

            # task_list_top_layuout에 ex)AM:hour:minute을 설정
            self.task_list_top_layout.addWidget(QLabel(am_or_pm))
            self.task_list_top_layout.addWidget(self.task_time_hours)
            self.task_list_top_layout.addWidget(QLabel(":"))
            self.task_list_top_layout.addWidget(self.task_time_minutes)

            # task_list_top_layout오른쪾에 빈 공간을 만듬
            self.task_list_top_layout.addStretch()

            # 큰 text 창을 생성
            self.text = QTextEdit()
            # task를 text에 할당
            self.text.setPlainText(task)

            # 삭제, 수정 버튼
            self.task_list_delete_button = QPushButton('Delete', self)
            self.task_list_modified_button = QPushButton('Modified', self)

            # 수정 버튼을 task_modified 함수에 할당 인자를 주기위해 partial 사용
            self.task_list_modified_button.clicked.connect(partial(self.task_modified, index))
            self.task_list_delete_button.clicked.connect(
                partial(self.task_delete, self.task_list_wrap_layout, index, True))

            # task_list_button_lalyout에 삭제, 수정 버튼을 추가
            self.task_list_button_layout.addWidget(self.task_list_delete_button)
            self.task_list_button_layout.addWidget(self.task_list_modified_button)

            # task_list_wrap_layout(전체를 감싸는 layout)에 task_list_top_layout, text, task_list_button_layout을 추가
            self.task_list_wrap_layout.addLayout(self.task_list_top_layout)
            self.task_list_wrap_layout.addWidget(self.text)
            self.task_list_wrap_layout.addLayout(self.task_list_button_layout)

            # task_list_wrap_layout을 grid레이아웃에 추가
            self.grid.addLayout(self.task_list_wrap_layout, index, 0)

        self.setLayout(self.grid)
        self.show()

    def task_modified(self, index):
        # 수정할 task를 받음
        modified_task = sort_task_list[index]
        # 키를 변경하기 위해 현재 시간 반환
        old_task_time = list(sort_task_list[index].keys())[0]
        modified_task_time = "{hours}:{minutes}".format(hours=self.task_time_hours.text(),
                                                        minutes=self.task_time_minutes.text())
        modified_task[modified_task_time] = modified_task.pop(old_task_time)
        modified_task[modified_task_time] = self.text.toPlainText()

    def task_delete(self, layout, index, remove=True):
        # task_list[index]를 한 번만 삭제시키기 remove=True 일떄만 삭제
        if remove:
            del sort_task_list[index]
        # layout자체를 삭제 할 수 없으므로 안에 아이템을 삭제 해야함
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.task_delete(item.layout(), index, remove=False)
        # 레이아웃 재 설정
        self.setGeometry(300, 300, 400, 300)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DayManagement()
    sys.exit(app.exec())
