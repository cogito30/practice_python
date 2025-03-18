import sys
import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont

class StopwatchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """ GUI 초기화 및 위젯 배치 """
        self.setWindowTitle('Stopwatch')
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        # 스톱워치 숫자 라벨 (초/분)
        self.stopwatch_label = QLabel('00:00', self)
        self.stopwatch_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stopwatch_label.setFont(QFont("Courier", 36, QFont.Weight.Bold))
        self.stopwatch_label.setFixedWidth(200)
        layout.addWidget(self.stopwatch_label)
        
        # 밀리초 라벨
        self.millisecond_label = QLabel('.000', self)
        self.millisecond_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.millisecond_label.setFont(QFont("Courier", 24, QFont.Weight.Bold))
        self.millisecond_label.setFixedWidth(80)
        layout.addWidget(self.millisecond_label)
        
        # 스톱워치 타이머
        self.stopwatch_timer = QTimer(self)
        self.stopwatch_timer.timeout.connect(self.update_stopwatch)
        self.elapsed_time = 0
        self.running = False
        
        # 시작/일시정지 버튼
        self.toggle_button = QPushButton('시작', self)
        self.toggle_button.clicked.connect(self.toggle_stopwatch)
        layout.addWidget(self.toggle_button)
        
        # 초기화 버튼
        self.reset_button = QPushButton('초기화', self)
        self.reset_button.clicked.connect(self.reset_stopwatch)
        layout.addWidget(self.reset_button)
        
        self.setLayout(layout)
        
    def toggle_stopwatch(self):
        """ 스톱워치 시작/일시정지 """
        if self.running:
            self.stopwatch_timer.stop()
            self.toggle_button.setText('시작')
        else:
            self.stopwatch_timer.start(10)
            self.toggle_button.setText('일시정지')
        self.running = not self.running
    
    def update_stopwatch(self):
        """ 스톱워치 시간 업데이트 """
        self.elapsed_time += 10
        minutes, milliseconds = divmod(self.elapsed_time, 60000)
        seconds, milliseconds = divmod(milliseconds, 1000)
        
        self.stopwatch_label.setText(f'{minutes:02}:{seconds:02}')
        self.millisecond_label.setText(f'.{milliseconds:03}')
    
    def reset_stopwatch(self):
        """ 스톱워치 초기화 """
        self.elapsed_time = 0
        self.stopwatch_label.setText('00:00')
        self.millisecond_label.setText('.000')
        self.stopwatch_timer.stop()
        self.toggle_button.setText('시작')
        self.running = False
    
    def keyPressEvent(self, event):
        """ 스페이스바로 시작/일시정지 기능 추가 """
        if event.key() == Qt.Key.Key_Space:
            self.toggle_stopwatch()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StopwatchApp()
    window.show()
    sys.exit(app.exec())
