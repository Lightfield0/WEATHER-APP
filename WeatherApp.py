import sys
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QLineEdit, QStyle
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt, QSize
import qdarktheme
import subprocess
import json
import os

def path_(yol):
    if hasattr(sys, '_MEIPASS'):
        path = os.path.join(sys._MEIPASS, yol)
    else:
        path = yol
    return path

def check_windows_theme():
    try:
        result = subprocess.run(["powershell", "-Command", "(Get-ItemProperty HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize).AppsUseLightTheme"], capture_output=True)
        return json.loads(result.stdout)
    except Exception as e:
        print("Hata:", e)
        return None

tema = check_windows_theme()

class HavaDurumuUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.koyu_tema_aktif = bool(tema)
        self.setWindowTitle("Hava Durumu Uygulaması")
        self.setWindowIcon(QIcon(path_('icons/logo.png')))  # İkonu ayarla
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.sehir_girisi = QLineEdit(self)
        self.sehir_girisi.setPlaceholderText("Şehir adı girin")
        layout.addWidget(self.sehir_girisi)

        sorgula_butonu = QPushButton("Hava Durumunu Sorgula", self)
        sorgula_butonu.clicked.connect(self.hava_durumu_sorgula)
        layout.addWidget(sorgula_butonu)

        self.hava_durumu_icon = QLabel(self)
        layout.addWidget(self.hava_durumu_icon)

        self.sehir_adi_label = QLabel("", self)  # Şehir adı için etiket
        self.sehir_adi_label.setFont(QFont("Arial", 30))
        layout.addWidget(self.sehir_adi_label)
        self.sehir_adi_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hava_durumu_bilgisi = QLabel("", self)  # Derece için etiket
        self.hava_durumu_bilgisi.setFont(QFont("Arial", 40, QFont.Weight.Bold))  # Kalın yazı tipi
        layout.addWidget(self.hava_durumu_bilgisi)
        self.hava_durumu_bilgisi.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hava_durumu_durum = QLabel("", self)  # Durum için etiket
        self.hava_durumu_durum.setFont(QFont("Arial", 20))
        layout.addWidget(self.hava_durumu_durum)
        self.hava_durumu_durum.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Tema değiştirme butonu (Qt'nin standart ikonu ile)
       # Tema değiştirme butonu
        self.tema_degistirme_butonu = QPushButton(self)
        self.tema_degistirme_butonu.setIcon(QIcon(path_("icons/moon.png")))  # Özel ikon dosya yolu
        self.tema_degistirme_butonu.setIconSize(QSize(30, 30))  # İkon boyutunu ayarla
        self.tema_degistirme_butonu.setFixedSize(40, 40)  # Buton boyutunu ayarla
        self.tema_degistirme_butonu.setStyleSheet("""
            QPushButton {
                border-radius: 20px;  # Yuvarlak buton
                background-color: transparent;  # Saydam arka plan
            }
            QPushButton:hover {
                background-color: rgba(200, 200, 200, 0.2);  # Hover durumunda arka plan rengi
            }
        """)
        self.tema_degistirme_butonu.clicked.connect(self.tema_degistir)
        layout.addWidget(self.tema_degistirme_butonu, alignment=Qt.AlignmentFlag.AlignRight)  # Sağ tarafa hizala

        self.tema_degistir()

    def tema_degistir(self):
        if self.koyu_tema_aktif:
            qdarktheme.setup_theme("light")
            self.koyu_tema_aktif = False
            self.tema_degistirme_butonu.setIcon(QIcon(path_("icons/moon.png")))
        else:
            qdarktheme.setup_theme("dark")
            self.koyu_tema_aktif = True
            self.tema_degistirme_butonu.setIcon(QIcon(path_("icons/sun-xxl.png")))

    def hava_durumu_sorgula(self):
        sehir = self.sehir_girisi.text()
        api_key = "6ca02032fc50d693a739ba2bf94a4ec6"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={api_key}&units=metric&lang=tr"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            durum = data['weather'][0]['description']
            icon_code = data['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

            self.sehir_adi_label.setText(sehir)
            self.hava_durumu_bilgisi.setText(f"{temp} °C")
            self.hava_durumu_durum.setText(durum)

            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(icon_url).content)
            
            # Pixmap'i yeniden boyutlandır

            self.hava_durumu_icon.setPixmap(pixmap)
            self.hava_durumu_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.sehir_adi_label.setText("")
            self.hava_durumu_bilgisi.setText("Hava durumu bilgisi alınamadı.")
            self.hava_durumu_durum.setText("")
            self.hava_durumu_icon.clear()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.enable_hi_dpi()
    pencere = HavaDurumuUygulamasi()
    pencere.show()
    sys.exit(app.exec())
