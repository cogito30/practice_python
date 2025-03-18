import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QSpinBox, QMessageBox
from PyQt6.QtCore import QTimer

class TimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """ GUI 초기화 및 위젯 배치 """
        self.setWindowTitle('Timer')
        self.setGeometry(100, 100, 300, 200)
        
        layout = QVBoxLayout()
        
        # 타이머 설정 (분 단위)
        self.timer_label = QLabel('타이머: 00:00', self)
        layout.addWidget(self.timer_label)
        
        self.time_input = QSpinBox(self)
        self.time_input.setRange(1, 999999)  # 최소 1분, 최대 제한 없음
        self.time_input.setSuffix(' 분')
        layout.addWidget(self.time_input)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = 0
        
        self.start_timer_button = QPushButton('타이머 시작', self)
        self.start_timer_button.clicked.connect(self.start_timer)
        layout.addWidget(self.start_timer_button)
        
        self.stop_timer_button = QPushButton('타이머 정지', self)
        self.stop_timer_button.clicked.connect(self.stop_timer)
        layout.addWidget(self.stop_timer_button)
        
        self.reset_timer_button = QPushButton('타이머 초기화', self)
        self.reset_timer_button.clicked.connect(self.reset_timer)
        layout.addWidget(self.reset_timer_button)
        
        self.setLayout(layout)
    
    def start_timer(self):
        """ 타이머 시작 """
        self.remaining_time = self.time_input.value() * 60  # 입력된 분을 초로 변환
        self.timer.start(1000)
        self.update_timer()
    
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
        self.remaining_time = 0
        self.timer_label.setText('타이머: 00:00')
        self.time_input.setValue(1)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TimerApp()
    window.show()
    sys.exit(app.exec())
