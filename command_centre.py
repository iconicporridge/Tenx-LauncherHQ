import sys
import signal
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtWidgets import QLabel, QGridLayout, QSizePolicy
from PyQt5.QtWidgets import QGraphicsOpacityEffect, QLabel
from PyQt5.QtGui import QIcon, QColor, QPalette, QIcon, QFont
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QThread, Qt, QRect
from launcher import tenx

class monitor_thread(QThread):

    signal = pyqtSignal()

    def __init__(self, launcher):
        super().__init__()
        self.launcher = launcher

    def run(self):

        self.state = self.launcher.dev

        while True:
            self.new_state = self.launcher.check_connection()
            if (self.new_state == self.state):
                self.sleep(0.1)
            else:
                self.state = self.new_state
                self.launcher.connect_launcher()
                self.signal.emit()
                self.sleep(0.1)


class usb_window(QWidget):

    def __init__(self):
        super().__init__()
        self.launcher = tenx()
        self.launcher.connect_launcher()
        self.spawn_monitor()
        self.add_icon()
        self.initUI()

    def initUI(self):
        self.a_geo = QDesktopWidget().availableGeometry()
        self.setWindowTitle("Missile Command")
        self.size_window()
        self.centre_window()
        self.define_colors()
        self.color_window()
        self.initial_grid()
        self.show()
        self.add_boot_window()
        self.start_monitoring()

    def add_icon(self):
        self.icon = QIcon()
        self.icon.addFile("./Images/missile.png")
        self.setWindowIcon(self.icon)

    def add_boot_window(self):
        self.add_usb_image()
        self.add_boot_label()

    def add_boot_label(self):

        self.boot_label = QLabel()
        font = QFont('Droid Sans', 16)
        font.setBold(True)
        self.boot_label.setFont(font)

        text_color = QColor()
        text_color.setNamedColor(self.grey)

        pal = QPalette()
        pal.setColor(QPalette.WindowText, text_color)
        self.boot_label.setPalette(pal)

        if (self.launcher.dev is None):
            self.boot_label.setText("Please insert your Tenx launcher")
        else:
            self.boot_label.setText("Welcome Commander")
        self.grid.addWidget(self.boot_label, 0, 0, Qt.AlignCenter)

        self.spacing_label = QLabel()
        self.grid.addWidget(self.spacing_label, 2, 0, Qt.AlignCenter)

    def spawn_monitor(self):
        self.connection_monitor = monitor_thread(self.launcher)

    def start_monitoring(self):
        self.connection_monitor.signal.connect(self.usb_toggle)
        self.connection_monitor.start()

    def define_colors(self):
        self.window_color = "#DEDEDE"
        self.rocket_red = "#C20024"
        self.grey = "#4D4D4D"

    def color_window(self):
        pal = QPalette()
        my_window_color = QColor()
        my_window_color.setNamedColor(self.window_color)
        pal.setColor(QPalette.Window, my_window_color)
        self.setPalette(pal)

    def size_window(self):
        self.height = self.a_geo.height()/2
        self.width = self.a_geo.width()/2
        self.resize(self.width, self.height)

    def centre_window(self):
        centre = self.a_geo.center()
        x = centre.x()
        y = centre.y()
        self.move(x-self.width/2, y-self.height/2)

    def initial_grid(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

    def add_usb_image(self):

        self.usb_image = QSvgWidget()
        self.usb_image.image0 = './Images/usb-0.svg'
        self.usb_image.image1 = './Images/usb-1.svg'
        self.usb_image.max_height = self.height/2
        self.update_usb_image()
        self.grid.addWidget(self.usb_image, 1, 0, Qt.AlignHCenter)

    def animate_svg(self, svg_image):
        svg_image.opac_eff = QGraphicsOpacityEffect()
        svg_image.setGraphicsEffect(svg_image.opac_eff)
        svg_image.animation = QPropertyAnimation(svg_image.opac_eff, b"opacity")
        svg_image.animation.setDuration(2000)
        svg_image.animation.setStartValue(0.1)
        svg_image.animation.setEndValue(1)
        svg_image.animation.setEasingCurve(QEasingCurve.OutCirc)
        svg_image.animation.start()

    def update_usb_image(self):

        if (self.launcher.dev is None):
            self.usb_image.load(self.usb_image.image0)
            self.usb_image.aspect_ratio = 1.0
        else:
            self.usb_image.load(self.usb_image.image1)
            self.usb_image.aspect_ratio = 1.0

        height = self.usb_image.max_height
        width = height*self.usb_image.aspect_ratio
        self.usb_image.setFixedWidth(width)
        self.usb_image.setFixedHeight(height)
        self.animate_svg(self.usb_image)

    def usb_toggle(self):
        self.update_usb_image()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    myapp = usb_window()
    sys.exit(app.exec_())