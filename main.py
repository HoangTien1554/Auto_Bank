import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow, show_custom_error
from api_reader import fetch_and_save_transactions
import time
import threading

from website_checker import check_website

url_check = "https://autobank.cagpro.cloud/ver.php"

def run_api_reader():
    while True:
        fetch_and_save_transactions()
        time.sleep(3)  # Kiểm tra API mỗi 5 giây

if __name__ == "__main__":
    if check_website(url_check):
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()

        # Chạy api_reader trong một thread riêng
        api_thread = threading.Thread(target=run_api_reader)
        api_thread.daemon = True  # Cho phép thread dừng khi ứng dụng đóng
        api_thread.start()

        sys.exit(app.exec_())
    else:
        show_custom_error("Lỗi Kích Hoạt", "❌ Chương trình chưa được kích hoạt! ❌\n❌ Vui lòng liên hệ CAGPRO ❌")