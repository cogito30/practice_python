import sys
import os
import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QListWidgetItem, QMessageBox
)

class DailyStudyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Daily Study')
        self.setGeometry(100, 100, 400, 500)
        
        layout = QVBoxLayout()
        
        self.today_date = self.get_today_date()
        self.label = QLabel(f'[{self.today_date}]', self)
        layout.addWidget(self.label)
        
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText('할 일을 입력하세요...')
        self.input_field.returnPressed.connect(self.add_task)
        layout.addWidget(self.input_field)
        
        self.add_button = QPushButton('확인', self)
        self.add_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_button)
        
        self.task_list = QListWidget(self)
        self.task_list.itemClicked.connect(self.toggle_task_status)
        layout.addWidget(self.task_list)
        
        self.delete_button = QPushButton('삭제', self)
        self.delete_button.clicked.connect(self.delete_task)
        layout.addWidget(self.delete_button)
        
        self.save_button = QPushButton('저장', self)
        self.save_button.clicked.connect(self.save_to_file)
        layout.addWidget(self.save_button)
        
        self.load_tasks()
        
        self.setLayout(layout)
    
    def get_today_date(self):
        now = datetime.datetime.now()
        return now.strftime('%Y-%m-%d(%a)')
    
    def get_file_path(self):
        today = datetime.datetime.now().strftime('%Y-%m-%d_%a')
        directory = 'daily_study_log'
        if not os.path.exists(directory):
            os.makedirs(directory)
        return os.path.join(directory, f'{today}.txt')
    
    def add_task(self):
        text = self.input_field.text().strip()
        if text:
            item = QListWidgetItem(f'- [ ] {text}')
            self.task_list.addItem(item)
            self.input_field.clear()
    
    def toggle_task_status(self, item):
        text = item.text()
        if text.startswith('- [ ]'):
            item.setText(text.replace('- [ ]', '- [X]', 1))
        elif text.startswith('- [X]'):
            item.setText(text.replace('- [X]', '- [ ]', 1))
    
    def delete_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            self.task_list.takeItem(self.task_list.row(selected_item))
    
    def save_to_file(self):
        file_path = self.get_file_path()
        total_tasks = self.task_list.count()
        completed_tasks = sum(1 for i in range(total_tasks) if self.task_list.item(i).text().startswith('- [X]'))
        
        header = f'[{self.today_date}]\n할 일 목록({total_tasks}) / 완료한 목록({completed_tasks})\n\n'
        tasks = '\n'.join([self.task_list.item(i).text() for i in range(total_tasks)])
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(header + tasks + '\n')
        
        QMessageBox.information(self, '저장 완료', '파일이 성공적으로 저장되었습니다!')
    
    def load_tasks(self):
        self.task_list.clear()
        file_path = self.get_file_path()
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines[2:]:  # 첫 2줄은 헤더이므로 제외
                    if line.startswith('- [ ]') or line.startswith('- [X]'):
                        self.task_list.addItem(QListWidgetItem(line.strip()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DailyStudyApp()
    window.show()
    sys.exit(app.exec())
