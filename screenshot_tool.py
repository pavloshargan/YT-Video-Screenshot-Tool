import sys
import glob
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QSpinBox, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QPalette, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QRect
import os
import keyboard
SCREENSHOTS_DIR = "dataset"
image_count = 0


# Ensure the directory exists
if not os.path.exists(SCREENSHOTS_DIR):
    os.makedirs(SCREENSHOTS_DIR)

# Get the current count
existing_files = glob.glob(os.path.join(SCREENSHOTS_DIR, '*.png'))
if existing_files:
    existing_files.sort()
    last_file = os.path.basename(existing_files[-1])
    image_count = int(last_file.split('.')[0]) + 1
else:
    image_count = 1


class TransparentWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowOpacity(0.99)
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.transparent)
        self.setPalette(palette)

        # Initialize with default values
        screen_width = app.desktop().screenGeometry().width()
        screen_height = app.desktop().screenGeometry().height()
        self.rect_top_left_x = int(50)
        self.rect_top_left_y = int(50)
        self.rect_bottom_right_x = int(screen_width)
        self.rect_bottom_right_y = int(screen_height)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(255, 0, 0, 127))
        painter.drawRect(self.rect_top_left_x, self.rect_top_left_y,
                         self.rect_bottom_right_x - self.rect_top_left_x,
                         self.rect_bottom_right_y - self.rect_top_left_y)

    def update_coordinates(self):
        self.rect_top_left_x = top_left_x_spinbox.value()
        self.rect_top_left_y = top_left_y_spinbox.value()
        self.rect_bottom_right_x = bottom_right_x_spinbox.value()
        self.rect_bottom_right_y = bottom_right_y_spinbox.value()
        self.update()


def on_button_clicked():
    global image_count
    region = QRect(w.rect_top_left_x, w.rect_top_left_y,
                   w.rect_bottom_right_x - w.rect_top_left_x,
                   w.rect_bottom_right_y - w.rect_top_left_y)

    w.hide()

    screen = QApplication.primaryScreen()
    screenshot = screen.grabWindow(0, region.x() + w.x(), region.y() + w.y(), region.width(), region.height())
    file_path = os.path.join(SCREENSHOTS_DIR, f"{image_count:06}.png")  # Format image_count to 6 digits
    screenshot.save(file_path, 'PNG')

    w.show()
    image_count += 1

def setup_global_hotkeys():
    keyboard.add_hotkey('s', on_button_clicked)
setup_global_hotkeys()
app = QApplication(sys.argv)

# Get the screen size
screen_rect = app.desktop().screenGeometry()

w = TransparentWidget()
w.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
w.setAttribute(Qt.WA_TranslucentBackground)
w.setGeometry(screen_rect)

# Coordinate SpinBoxes
top_left_x_spinbox = QSpinBox(w)
top_left_x_spinbox.setRange(0, screen_rect.width())
top_left_x_spinbox.setValue(50)
top_left_x_spinbox.valueChanged.connect(w.update_coordinates)

top_left_y_spinbox = QSpinBox(w)
top_left_y_spinbox.setRange(0, screen_rect.height())
top_left_y_spinbox.setValue(50)
top_left_y_spinbox.valueChanged.connect(w.update_coordinates)

bottom_right_x_spinbox = QSpinBox(w)
bottom_right_x_spinbox.setRange(0, screen_rect.width())
bottom_right_x_spinbox.setValue(screen_rect.width() - 50)
bottom_right_x_spinbox.valueChanged.connect(w.update_coordinates)

bottom_right_y_spinbox = QSpinBox(w)
bottom_right_y_spinbox.setRange(0, screen_rect.height())
bottom_right_y_spinbox.setValue(screen_rect.height() - 50)
bottom_right_y_spinbox.valueChanged.connect(w.update_coordinates)

# Top Controls Layout
controls_layout = QHBoxLayout()
controls_layout.addWidget(QLabel("Top-left X:"))
controls_layout.addWidget(top_left_x_spinbox)
controls_layout.addWidget(QLabel("Top-left Y:"))
controls_layout.addWidget(top_left_y_spinbox)
controls_layout.addWidget(QLabel("Bottom-right X:"))
controls_layout.addWidget(bottom_right_x_spinbox)
controls_layout.addWidget(QLabel("Bottom-right Y:"))
controls_layout.addWidget(bottom_right_y_spinbox)

button = QPushButton("Screenshot", w)
button.clicked.connect(on_button_clicked)
controls_layout.addWidget(button)

exit_button = QPushButton("Exit", w)
exit_button.clicked.connect(app.exit)
controls_layout.addWidget(exit_button)

# Position the controls at the top
controls_container = QWidget(w)
controls_container.setLayout(controls_layout)
controls_container.setGeometry(0, 0, w.width(), 50)

w.show()
sys.exit(app.exec_())
