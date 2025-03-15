import sys
import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTimeEdit, QListWidget, QMessageBox
)
from PyQt6.QtCore import QTimer, QTime

class ClockAlarmTimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """ GUI 초기화 및 위젯 배치 """
        self.setWindowTitle('Clock, Alarm & Timer')
        self.setGeometry(100, 100, 400, 500)
        
        layout = QVBoxLayout()
        
        # 현재 시간 표시
        self.current_time_label = QLabel('', self)
        layout.addWidget(self.current_time_label)
        
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_current_time)
        self.clock_timer.start(1000)
        
        # 알람 설정
        self.alarm_list = QListWidget(self)  # 초기화 추가
        layout.addWidget(self.alarm_list)
        
        self.alarm_time_edit = QTimeEdit(self)
        layout.addWidget(self.alarm_time_edit)
        
        self.add_alarm_button = QPushButton('알람 추가', self)
        self.add_alarm_button.clicked.connect(self.add_alarm)
        layout.addWidget(self.add_alarm_button)
        
        self.remove_alarm_button = QPushButton('알람 삭제', self)
        self.remove_alarm_button.clicked.connect(self.remove_alarm)
        layout.addWidget(self.remove_alarm_button)
        
        # 카운트다운 타이머
        self.timer_label = QLabel('타이머: 00:00', self)
        layout.addWidget(self.timer_label)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = 0
        
        self.timer_time_edit = QTimeEdit(self)
        layout.addWidget(self.timer_time_edit)
        
        self.start_timer_button = QPushButton('타이머 시작', self)
        self.start_timer_button.clicked.connect(self.start_timer)
        layout.addWidget(self.start_timer_button)
        
        self.stop_timer_button = QPushButton('타이머 정지', self)
        self.stop_timer_button.clicked.connect(self.stop_timer)
        layout.addWidget(self.stop_timer_button)
        
        self.reset_timer_button = QPushButton('타이머 초기화', self)
        self.reset_timer_button.clicked.connect(self.reset_timer)
        layout.addWidget(self.reset_timer_button)
        
        # 스톱워치 추가
        self.stopwatch_label = QLabel('스톱워치: 00:00.000', self)
        layout.addWidget(self.stopwatch_label)
        
        self.stopwatch_timer = QTimer(self)
        self.stopwatch_timer.timeout.connect(self.update_stopwatch)
        self.elapsed_time = 0
        
        self.start_stopwatch_button = QPushButton('스톱워치 시작', self)
        self.start_stopwatch_button.clicked.connect(self.start_stopwatch)
        layout.addWidget(self.start_stopwatch_button)
        
        self.stop_stopwatch_button = QPushButton('스톱워치 정지', self)
        self.stop_stopwatch_button.clicked.connect(self.stop_stopwatch)
        layout.addWidget(self.stop_stopwatch_button)
        
        self.reset_stopwatch_button = QPushButton('스톱워치 초기화', self)
        self.reset_stopwatch_button.clicked.connect(self.reset_stopwatch)
        layout.addWidget(self.reset_stopwatch_button)
        
        self.setLayout(layout)
        
        self.update_current_time()
    
    def update_current_time(self):
        """ 현재 시간을 업데이트 """
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        self.current_time_label.setText(f'현재 시간: {current_time}')
        self.check_alarms()
    
    def add_alarm(self):
        """ 알람 추가 """
        alarm_time = self.alarm_time_edit.time().toString('HH:mm')
        self.alarm_list.addItem(alarm_time)
    
    def remove_alarm(self):
        """ 선택한 알람 삭제 """
        selected_item = self.alarm_list.currentItem()
        if selected_item:
            self.alarm_list.takeItem(self.alarm_list.row(selected_item))
    
    def check_alarms(self):
        """ 현재 시간이 알람 시간과 일치하는지 확인 """
        current_time = QTime.currentTime().toString('HH:mm')
        for index in range(self.alarm_list.count()):
            if self.alarm_list.item(index).text() == current_time:
                QMessageBox.information(self, '알람', f'알람 시간: {current_time}')
                self.alarm_list.takeItem(index)  # 알람 울린 후 삭제
                break
    
    def start_timer(self):
        """ 타이머 시작 """
        time = self.timer_time_edit.time()
        self.remaining_time = time.minute() * 60 + time.second()
        self.timer.start(1000)
    
    def update_timer(self):
        """ 타이머 시간 업데이트 """
        if self.remaining_time > 0:
            self.remaining_time -= 1
            minutes, seconds = divmod(self.remaining_time, 60)
            self.timer_label.setText(f'타이머: {minutes:02}:{seconds:02}')
        else:
            self.timer.stop()
            QMessageBox.information(self, '타이머 완료', '타이머 시간이 종료되었습니다!')
    
    def stop_timer(self):
        """ 타이머 정지 """
        self.timer.stop()
    
    def reset_timer(self):
        """ 타이머 초기화 """
        self.timer.stop()
        self.timer_label.setText('타이머: 00:00')
        self.remaining_time = 0
    
    def start_stopwatch(self):
        """ 스톱워치 시작 """
        self.stopwatch_timer.start(10)
    
    def update_stopwatch(self):
        """ 스톱워치 시간 업데이트 """
        self.elapsed_time += 10
        minutes, milliseconds = divmod(self.elapsed_time, 60000)
        seconds, milliseconds = divmod(milliseconds, 1000)
        self.stopwatch_label.setText(f'스톱워치: {minutes:02}:{seconds:02}.{milliseconds:03}')
    
    def stop_stopwatch(self):
        """ 스톱워치 정지 """
        self.stopwatch_timer.stop()
    
    def reset_stopwatch(self):
        """ 스톱워치 초기화 """
        self.elapsed_time = 0
        self.stopwatch_label.setText('스톱워치: 00:00.000')
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClockAlarmTimerApp()
    window.show()
    sys.exit(app.exec())
