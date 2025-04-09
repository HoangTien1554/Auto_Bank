import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel, QVBoxLayout, QWidget, QTableWidget, \
    QSystemTrayIcon, QMenu, QDialog, QLineEdit, QHBoxLayout, QPushButton, QHeaderView, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt, QSharedMemory, QTimer
import datetime
import pyautogui

from autohotkey_executor import execute_transaction
from config_manager import load_config, update_config
from transaction_manager import load_transactions, save_transactions
from website_checker import check_website
from xml_manager import load_xml_info
import xml.etree.ElementTree as ET
import playsound
import time


width, height = pyautogui.size()

shared_memory = QSharedMemory("TestUI_Unique_Instance")

if not shared_memory.create(1):  # Nếu ứng dụng đã chạy
    sys.exit()

class ConfigWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cấu hình")
        self.setGeometry(200, 200, 350, 200)
        self.setWindowModality(Qt.ApplicationModal)

        config = load_config()
        self.ahk_file = config.get("ahk_file", "")
        self.token = config.get("token", "")
        self.bank_number = config.get("bank_number", "")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("AHK File:"))

        button_layout = QHBoxLayout()
        self.csm_button = QPushButton("CSM Billing")
        self.csm_button.clicked.connect(lambda: self.change_ahk("CAGBank_NapTien_CSM.ahk"))
        button_layout.addWidget(self.csm_button)

        self.fnet_button = QPushButton("FNet Billing")
        self.fnet_button.clicked.connect(lambda: self.change_ahk("CAGBank_NapTien_FNet.ahk"))
        button_layout.addWidget(self.fnet_button)

        self.gcafe_button = QPushButton("Gcafe Billing")
        self.gcafe_button.clicked.connect(lambda: self.change_ahk("CAGBank_NapTien_Gcafe.ahk"))
        button_layout.addWidget(self.gcafe_button)

        layout.addLayout(button_layout)

        self.buttons = {
            "CAGBank_NapTien_CSM.ahk": self.csm_button,
            "CAGBank_NapTien_FNet.ahk": self.fnet_button,
            "CAGBank_NapTien_Gcafe.ahk": self.gcafe_button
        }
        # Cập nhật trạng thái focus ban đầu
        self.update_button_focus()

        layout.addWidget(QLabel("Số tài khoản:"))
        self.bank_entry = QLineEdit(str(self.bank_number))
        layout.addWidget(self.bank_entry)

        layout.addWidget(QLabel("Secret Key:"))
        self.token_entry = QLineEdit(self.token)
        layout.addWidget(self.token_entry)

        # Tạo nút Hủy và Lưu
        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Huỷ")
        self.cancel_button.clicked.connect(self.close)
        button_layout.addWidget(self.cancel_button)

        self.save_button = QPushButton("Lưu")
        self.save_button.clicked.connect(self.save_config)
        button_layout.addWidget(self.save_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def update_button_focus(self):
        """ Cập nhật giao diện để focus vào nút tương ứng với file AHK đang chọn """
        config = load_config()
        for file_name, button in self.buttons.items():
            if file_name == config.get("ahk_file", ""):
                button.setStyleSheet(
                    "background-color: green; color: white; font-weight: bold;")
            else:
                button.setStyleSheet("")  # Reset về mặc định

    def change_ahk(self, file_name):
        update_config("ahk_file", file_name)
        QMessageBox.information(self, "Thông báo", f"Đã chuyển sang {file_name}")
        self.update_button_focus()

    def save_config(self):
        """Lưu cấu hình vào file config.json"""
        reply = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc chắn đã nhập đúng dữ liệu?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            update_config("bank_number", self.bank_entry.text())
            update_config("token", self.token_entry.text())
            QMessageBox.information(self, "Thành công", "Đã lưu cấu hình!")
            self.close()

class EditBankInfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sửa thông tin chuyển khoản")
        self.setGeometry(200, 200, 350, 200)
        self.setWindowModality(Qt.ApplicationModal)

        layout = QVBoxLayout()

        bank, account, receiver_name = load_xml_info()

        layout.addWidget(QLabel("Mã ngân hàng:"))
        self.bank_entry = QLineEdit(bank)
        layout.addWidget(self.bank_entry)

        layout.addWidget(QLabel("Số tài khoản:"))
        self.account_entry = QLineEdit(account)
        layout.addWidget(self.account_entry)

        layout.addWidget(QLabel("Tên người nhận:"))
        self.receiver_entry = QLineEdit(receiver_name)
        layout.addWidget(self.receiver_entry)

        # Tạo nút Hủy và Lưu
        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Huỷ")
        self.cancel_button.clicked.connect(self.close)
        button_layout.addWidget(self.cancel_button)

        self.save_button = QPushButton("Lưu")
        self.save_button.clicked.connect(self.save_info)
        button_layout.addWidget(self.save_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_info(self):
        try:
            root = ET.Element("info")
            bank = ET.SubElement(root, "bank")
            bank.text = self.bank_entry.text()
            account = ET.SubElement(root, "account")
            account.text = self.account_entry.text()
            receiver_name = ET.SubElement(root, "receiver_name")
            receiver_name.text = self.receiver_entry.text()

            tree = ET.ElementTree(root)
            tree.write("client/data-client/info.xml")
            QMessageBox.information(self, "Thành công", "Đã lưu thông tin!")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi lưu thông tin: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Danh Sách Giao Dịch")
        self.setGeometry(100, 100, 800, 400)
        self.setWindowIcon(QIcon("data/CAGPRO.ico"))

        menubar = self.menuBar()
        settings_menu = menubar.addMenu("Tuỳ chọn")

        self.settings_action = QAction("Cấu Hình", self)
        self.settings_action.triggered.connect(self.open_config_window)
        settings_menu.addAction(self.settings_action)

        self.bank_info_action = QAction("Sửa thông tin chuyển khoản", self)
        self.bank_info_action.triggered.connect(self.open_bank_info_window)
        settings_menu.addAction(self.bank_info_action)

        self.summary_action = QAction("Tổng kết doanh thu", self)
        self.summary_action.triggered.connect(self.tong_ket_doanh_thu)
        settings_menu.addAction(self.summary_action)

        layout = QVBoxLayout()

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Tài khoản", "Số Tiền", "Ngày", "Trạng Thái"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.total_label = QLabel("Tổng Tiền: 0 VND")
        self.total_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.total_label.setStyleSheet("color: red;")
        layout.addWidget(self.total_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("data/CAGPRO.ico"))
        self.tray_menu = QMenu()

        show_action = QAction("Mở lại", self)
        show_action.triggered.connect(self.show_main_window)
        self.tray_menu.addAction(show_action)

        exit_action = QAction("Thoát", self)
        exit_action.triggered.connect(self.close_application)
        self.tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Khởi tạo QTimer để tự động cập nhật dữ liệu mỗi 5 giây
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_data)
        self.timer.start(1000)  # Cập nhật mỗi 5000ms (5 giây)

        self.load_data()  # Load dữ liệu ngay khi khởi động

    def load_data(self):
        config = load_config()
        last_id = config.get("last_id", 0)
        transactions = load_transactions(last_id)
        self.table.setRowCount(len(transactions))
        total_amount = 0

        for row, transaction in enumerate(transactions):
            self.table.setItem(row, 0, QTableWidgetItem(transaction.get("content", "")))

            amount = transaction.get("amount", 0)
            formatted_amount = f"{amount:,} VND"
            amount_item = QTableWidgetItem(formatted_amount)
            amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 1, amount_item)

            date_item = QTableWidgetItem(transaction.get("datetime", ""))
            date_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, date_item)

            status_item = QTableWidgetItem(transaction.get("status", ""))
            status_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, status_item)

            total_amount += amount

            # Gọi AutoHotkey nếu trạng thái là "Chưa nạp tiền"
            if transaction.get("status") == "Chưa nạp tiền":
                execute_transaction(transaction["content"], transaction["amount"])
                transaction["status"] = "Đã nạp tiền"
                save_transactions(transactions)
                playsound.playsound("data/notification.mp3")
                time.sleep(3) # chờ 3 giây

        self.total_label.setText(f"Tổng Tiền: {total_amount:,} VND")

    def open_config_window(self):
        config_dialog = ConfigWindow(self)
        config_dialog.exec_()

    def open_bank_info_window(self):
        bank_info_dialog = EditBankInfoDialog(self)
        bank_info_dialog.exec_()

    def tong_ket_doanh_thu(self):
        #  Hiển thị hộp thoại xác nhận
        confirm = QMessageBox.question(self, "Xác nhận",
                                       "Sau khi tổng kết sẽ xoá hết lịch sử giao dịch!!!\nBạn có chắc chắn không?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if confirm == QMessageBox.No:
            return

        #  Đọc dữ liệu giao dịch
        config = load_config()
        last_id = config.get("last_id", 0)
        transactions = load_transactions(last_id)

        #  Lọc ra các giao dịch mới
        new_transactions = [t for t in transactions if t.get("id", 0) > last_id]
        total_transactions = len(new_transactions)
        total_amount = sum(int(t.get("amount", 0)) for t in new_transactions if str(t.get("amount", "0")).isdigit())

        #  Ghi tổng kết vào file TXT
        now = datetime.datetime.now()
        today = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")

        summary_file = "data/daily_summary.txt"
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write(f"{today} {current_time} - {total_transactions} giao dịch - {total_amount:,} VND\n")

        #  Cập nhật last_id trong config
        if new_transactions:
            new_last_id = max(t["id"] for t in new_transactions)
            update_config("last_id", new_last_id)

        #  Xoá dữ liệu hiển thị trên giao diện
        self.table.setRowCount(0)
        self.total_label.setText("Tổng Tiền: 0 VND")

        QMessageBox.information(self, "Thành công", "Tổng kết doanh thu thành công!")

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage("Ứng dụng", "Ứng dụng đang chạy dưới system tray", QSystemTrayIcon.Information, 2000)

    def show_main_window(self):
        self.showNormal()
        self.activateWindow()

    def close_application(self):
        self.tray_icon.hide()
        QApplication.quit()

class CustomMessageBox(QDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(400, 255)
        self.setStyleSheet("background-color: white; border-radius: 10px;")
        self.setWindowIcon(QIcon("data/CAGPRO.ico"))

        layout = QVBoxLayout()

        # Thêm hình ảnh lỗi
        icon_label = QLabel(self)
        pixmap = QPixmap("data/CAGPROCLOUD.png")  # Thêm icon nếu có
        icon_label.setPixmap(pixmap.scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        # Nội dung thông báo
        message_label = QLabel(message, self)
        message_label.setFont(QFont("Arial", 12))
        message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(message_label)

        # Nút đóng
        ok_button = QPushButton("ĐÓNG", self)
        ok_button.setStyleSheet(
            "background-color: red; color: white; padding: 12px 40px; border-radius: 5px; font-size: 15px; font-weight: bold;")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

def show_custom_error(title, message):
    app = QApplication(sys.argv)
    dialog = CustomMessageBox(title, message)
    dialog.exec_()
    sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    shared_memory = QSharedMemory("TestUI_Unique_Instance")
    if not shared_memory.create(1):  # Kiểm tra nếu ứng dụng đã chạy
        sys.exit()

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())