import file_handler
import ui
import sys
from url_finder import UrlCollecter
from PyQt5.QtCore import *

class Controller():

    def __init__(self):
        self.workers = list()
        self.url_list_in_each_site_dict = dict()

    def show_main(self,site_list_in_excel):
        self.main_window = ui.MainWindow(site_list_in_excel)
        self.main_window.EXECUTION.connect(self.show_table)
        self.main_window.DOWNLOAD.connect(self.make_sitemap_file)
        self.main_window.show()
        
    def show_table(self,checked_check_box_list):
        self.temp_file_manager = file_handler.TempFileManager(checked_check_box_list)
        self.set_progress_bar(checked_check_box_list)
        for site in checked_check_box_list:
            worker = UrlCollecter(site)
            worker.PROGRESS.connect(self.progress_bar.update)
            worker.FINISHED.connect(self.finish_progress)
            worker.DUMP.connect(self.dump_temporary_url_list)
            self.workers.append(worker)
            worker.start()
        self.set_timer()
    
    def set_progress_bar(self,checked_check_box_list):
        self.progress_bar = ui.ProgressBar(checked_check_box_list)
        self.progress_bar.STOP.connect(self.stop_progress_bar)

    def set_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeout_progress)
        self.timer.start(900000)

    def timeout_progress(self):
        for worker in self.workers:
            worker.stop_flag = True

    def finish_progress(self,result_tuple):
        main_domain,left_out_url_list = result_tuple
        temporary_url_list = self.temp_file_manager.load_temporary_url_list(main_domain)
        url_list_in_each_site = left_out_url_list + temporary_url_list
        self.url_list_in_each_site_dict[main_domain] = list(set(url_list_in_each_site))
        self.progress_bar.fill_progress_bar()
        self.main_window.ready_to_download()

    def stop_progress_bar(self):
        for worker in self.workers:
            worker.stop_flag = True
            worker.wait()
            worker.quit()

    def dump_temporary_url_list(self,result_tuple):
        main_domain,temporary_url_list = result_tuple
        self.temp_file_manager.dump_temporary_url_list(main_domain,temporary_url_list)

    def make_sitemap_file(self):
        maker = file_handler.SitemapMaker(self.url_list_in_each_site_dict)
        maker.make_file()
        self.temp_file_manager.remove_temp_files()
        
if __name__=='__main__':
    app = ui.qapplication_constructor()
    site_list_in_excel = file_handler.read_excel_line()
    controller = Controller()
    controller.show_main(site_list_in_excel)
    sys.exit(app.exec_())
