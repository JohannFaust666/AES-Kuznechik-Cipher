from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import shutil
from dotenv import load_dotenv

# Загрузка переменных из .env
load_dotenv()
ENCRYPTION_KEY = bytes.fromhex(os.getenv('ENCRYPTION_KEY'))
BACKUP_DIR = os.getenv('BACKUP_DIR')

class KuznechikCipher:
    def __init__(self, key):
        self.key = key

    def encrypt_file(self, file_path):
        # Чтение исходного файла
        with open(file_path, 'rb') as f:
            plaintext = f.read()

        # Шифрование данных
        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)

        # Создание зашифрованного файла
        encrypted_file_path = file_path + '.enc'
        with open(encrypted_file_path, 'wb') as f:
            f.write(cipher.nonce)
            f.write(tag)
            f.write(ciphertext)

        # Создание бэкапа
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
        shutil.copy(encrypted_file_path, BACKUP_DIR)

        # Удаление оригинального файла
        os.remove(file_path)

        return encrypted_file_path

    def decrypt_file(self, encrypted_file_path):
        # Чтение зашифрованного файла
        with open(encrypted_file_path, 'rb') as f:
            nonce = f.read(16)
            tag = f.read(16)
            ciphertext = f.read()

        # Расшифровка данных
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)

        # Создание расшифрованного файла
        decrypted_file_path = encrypted_file_path.replace('.enc', '')
        with open(decrypted_file_path, 'wb') as f:
            f.write(plaintext)

        # Удаление зашифрованного файла
        os.remove(encrypted_file_path)

        return decrypted_file_path

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QGroupBox
)
from PyQt5.QtGui import QFont, QIcon

class CryptoGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Шифрование данных')
        self.setGeometry(300, 300, 600, 400)
        self.setWindowIcon(QIcon('lock.png'))  # Укажите путь к иконке

        layout = QVBoxLayout()

        # Раздел: Работа с каталогом
        dir_group = QGroupBox("Выбор каталога")
        dir_layout = QVBoxLayout()
        self.path_label = QLabel('Путь к каталогу:')
        self.path_label.setStyleSheet("color: white;")  
        dir_layout.addWidget(self.path_label)

        self.path_input = QLineEdit(self)
        self.path_input.setPlaceholderText("Выберите папку с файлами...")
        dir_layout.addWidget(self.path_input)

        self.browse_button = QPushButton('Обзор', self)
        self.browse_button.setIcon(QIcon('folder_icon.png'))  # Иконка папки
        self.browse_button.clicked.connect(self.browse_file_or_directory)
        dir_layout.addWidget(self.browse_button)
        dir_group.setLayout(dir_layout)

        layout.addWidget(dir_group)

        # Раздел: Действия
        action_group = QGroupBox("Действия")
        action_layout = QHBoxLayout()

        self.encrypt_button = QPushButton('🔒 Зашифровать', self)
        self.encrypt_button.clicked.connect(self.encrypt_data)
        action_layout.addWidget(self.encrypt_button)

        self.decrypt_button = QPushButton('🔓 Расшифровать', self)
        self.decrypt_button.clicked.connect(self.decrypt_data)
        action_layout.addWidget(self.decrypt_button)

        action_group.setLayout(action_layout)
        layout.addWidget(action_group)

        # Раздел: Вывод сообщений
        self.status_label = QLabel('')
        self.status_label.setFont(QFont('Arial', 10))
        self.status_label.setStyleSheet("color: white;")  
        layout.addWidget(self.status_label)

        # Основной контейнер
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def browse_file_or_directory(self):
        path = QFileDialog.getExistingDirectory(self, "Выберите каталог")
        self.path_input.setText(path)

    def encrypt_data(self):
        directory = self.path_input.text()
        if not os.path.exists(directory):
            self.path_label.setText("Указанный путь не существует!")
            return

        cipher = KuznechikCipher(ENCRYPTION_KEY)
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.txt'):
                    full_path = os.path.join(root, file)
                    cipher.encrypt_file(full_path)
        self.status_label.setText("✅ Шифрование завершено!")
	
    def decrypt_data(self):
        directory = self.path_input.text()
        if not os.path.exists(directory):
            self.path_label.setText("Указанный путь не существует!")
            return

        cipher = KuznechikCipher(ENCRYPTION_KEY)
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.enc'):
                    full_path = os.path.join(root, file)
                    cipher.decrypt_file(full_path)
        self.status_label.setText("✅ Расшифровка завершена!")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Применяем темный стиль
    app.setStyleSheet("""
        QMainWindow {
            background-color: #121212;
            color: #ffffff;
        }
        QLabel {
            font-size: 12px;
        }
        QLineEdit {
            background-color: #1e1e1e;
            color: #ffffff;
            border: 1px solid #5e5e5e;
            padding: 5px;
        }
        QPushButton {
            background-color: #3e8e41;
            color: white;
            border-radius: 5px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QGroupBox {
            border: 1px solid #5e5e5e;
            border-radius: 5px;
            margin-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 5px;
            color: #a1a1a1;
        }
    """)

    ex = CryptoGUI()
    ex.show()
    sys.exit(app.exec_())
