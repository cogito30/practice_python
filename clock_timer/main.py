import sys
import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTimeEdit, QMessageBox
)
from PyQt6.QtCore import QTimer, QTime

class ClockAlarmTimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.alarm_time = None  # 알람 시간 초기화
        self.timer_running = False  # 타이머 실행 상태
        self.init_ui()
    
    def init_ui(self):
        """ GUI 초기화 및 위젯 배치 """
        self.setWindowTitle('Clock, Alarm & Timer')
        self.setGeometry(100, 100, 300, 200)
        
        layout = QVBoxLayout()
        
        # 현재 시간 표시
        self.clock_label = QLabel('', self)
        layout.addWidget(self.clock_label)
        
        # 알람 설정
        self.alarm_input = QTimeEdit(self)
        layout.addWidget(self.alarm_input)
        
        self.set_alarm_button = QPushButton('알람 설정', self)
        self.set_alarm_button.clicked.connect(self.set_alarm_time)
        layout.addWidget(self.set_alarm_button)
        
        # 타이머 (카운트다운)
        self.timer_label = QLabel('타이머: 00:00', self)
        layout.addWidget(self.timer_label)
        
        self.start_timer_button = QPushButton('타이머 시작', self)
        self.start_timer_button.clicked.connect(self.start_timer)
        layout.addWidget(self.start_timer_button)
        
        # 현재 시간 업데이트 타이머
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)  # 1초마다 업데이트
        
        self.setLayout(layout)
    
    def update_clock(self):
        """ 현재 시간 갱신 """
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        self.clock_label.setText(f'현재 시간: {current_time}')
        
        # 알람 시간 확인
        if self.alarm_time and QTime.currentTime() >= self.alarm_time:
            QMessageBox.information(self, '알람', '알람 시간이 되었습니다!')
            self.alarm_time = None  # 알람 초기화
    
    def set_alarm_time(self):
        """ 알람 시간 설정 """
        self.alarm_time = self.alarm_input.time()
        QMessageBox.information(self, '알람 설정', f'알람이 {self.alarm_time.toString()}로 설정되었습니다.')
    
    def start_timer(self):
        """ 타이머 시작 """
        if not self.timer_running:
            self.timer_running = True
            self.timer_seconds = 10  # 기본 10초 타이머
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_timer)
            self.timer.start(1000)
    
    def update_timer(self):
        """ 타이머 카운트다운 """
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.timer_label.setText(f'타이머: {self.timer_seconds}초')
        else:
            self.timer.stop()
            self.timer_running = False
            QMessageBox.information(self, '타이머 종료', '타이머 시간이 종료되었습니다!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClockAlarmTimerApp()
    window.show()
    sys.exit(app.exec())
