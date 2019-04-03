from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

class MainWindow(QMainWindow):

    EXECUTION = pyqtSignal(list)
    DOWNLOAD = pyqtSignal()

    def __init__(self,site_list_be_sitemap):
        super().__init__()
        self.check_box_list = list()
        self.site_list_to_be_sitemap = site_list_be_sitemap
        self.checked_check_box_list = list()
        self.setup_main_window()

    def setup_main_window(self):
        self.setGeometry(800, 200, 500, 300)
        self.setWindowTitle("사이트맵 제작기")
        self._setup_checkbox()
        self._setup_exe_button()
        self._setup_exit_button()
        self._setup_download_button()
    
    def _setup_checkbox(self):
        self.y_position = 20
        for url in self.site_list_to_be_sitemap:
            checkbox = QCheckBox(url, self)
            self.y_position += 30
            checkbox.move(10,self.y_position)
            checkbox.resize(150,30)
            self.check_box_list.append(checkbox)
            checkbox.stateChanged.connect(self.check_box_state)
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

    def _setup_exe_button(self):
        self.exe_button = QPushButton("해당 목록 실행", self)
        self.exe_button.move(350,self.y_position+50)
        self.exe_button.clicked.connect(self.switch_to_execute)

    def switch_to_execute(self):
        self.EXECUTION.emit(self.checked_check_box_list)
        self.exe_button.setEnabled(False)

    def _setup_exit_button(self):
        exit_button = QPushButton("종료", self)
        exit_button.move(350,self.y_position+110)
        exit_button.clicked.connect(self.close_window)

    def check_box_state(self):
        msg = "Selected: "
        for checkbox in self.check_box_list:
            if checkbox.isChecked() == True:
                msg += checkbox.text()
                msg += ' '
                if checkbox.text() not in self.checked_check_box_list:
                    self.checked_check_box_list.append(checkbox.text())
        self.statusBar.showMessage(msg)
    
    def _setup_download_button(self):
        self.download_button = QPushButton("파일 다운로드",self)
        self.download_button.move(350,self.y_position+80)
        self.download_button.setEnabled(False)
        self.download_button.clicked.connect(self.switch_to_download)

    def switch_to_download(self):
        self.DOWNLOAD.emit()
        self.download_button.setEnabled(False)

    def ready_to_download(self):
        self.download_button.setEnabled(True)

    def close_window(self):
        QCoreApplication.instance().quit()

class ProgressBar(QWidget):

    STOP = pyqtSignal()

    def __init__(self,site_list):
        super().__init__()
        self.progress_bar = QProgressBar(self)
        self.site_list = site_list
        self.progress_bar_value = 0
        self.setGeometry(1300, 200, 350, 150)
        self.set_progress_bar()
        self.set_buttons()
        self.start_time = QDateTime.currentDateTime
        self.show()

    def set_progress_bar(self):
        self.setWindowTitle("진행 상황 알림판")
        self.progress_bar.setGeometry(30, 20, 300, 25)
        self.progress_bar.setMaximum(100)

    def set_buttons(self):
        self.stop_button = QPushButton('작업 중단',self)
        self.exit_button = QPushButton('나가기',self)
        self.stop_button.resize(130,32)
        self.exit_button.resize(130,32)
        self.exit_button.clicked.connect(self.close)
        self.stop_button.clicked.connect(self.stop_progress_bar)
        self.stop_button.move(30,80)
        self.exit_button.move(200,80)

    def update(self,number):
        if self.progress_bar_value < 99:
            self.progress_bar_value += number
            self.progress_bar.setValue(self.progress_bar_value)
        else:
            return

    def stop_progress_bar(self):
        self.STOP.emit()

    def fill_progress_bar(self):
        self.progress_bar.setValue(100)

def qapplication_constructor():
    return QApplication(sys.argv)

