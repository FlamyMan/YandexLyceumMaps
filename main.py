import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


def generate_request(x, y, spn_x, spn_y, L):
    base = "http://static-maps.yandex.ru/1.x/?"
    out = base + f"ll={x},{y}&spn={spn_x},{spn_y}&l={L}"
    return out


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.x = 37.530887
        self.y = 55.703118
        self.spn_x = 0.002
        self.spn_y = 0.002
        self.L = "map"

        self.getImage()
        self.initUI()


    def getImage(self):
        map_request = generate_request(self.x, self.y, self.spn_x, self.spn_y, self.L)
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
