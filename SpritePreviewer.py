# github repo is at https://github.com/Incom1ng174/programming2026

import math

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

# This function loads a series of sprite images stored in a folder with a
# consistent naming pattern: sprite_# or sprite_##. It returns a list of the images.
def load_sprite(sprite_folder_name, number_of_frames):
    frames = []
    padding = math.ceil(math.log(number_of_frames - 1, 10))
    for frame in range(number_of_frames):
        folder_and_file_name = sprite_folder_name + "/sprite_" + str(frame).rjust(padding, '0') + ".png"
        frames.append(QPixmap(folder_and_file_name))

    return frames

class SpritePreview(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sprite Animation Preview")
        # This loads the provided sprite and would need to be changed for your own.
        self.num_frames = 21
        self.frames = load_sprite('spriteImages',self.num_frames)
        self.current_frame = 0
        self.is_animating = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)
        self.setupUI()
        self.build_menu()

    def setupUI(self):
        # An application needs a central widget - often a QFrame
        frame = QFrame()
        main_layout = QVBoxLayout(frame)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 20, 20, 20)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(300, 200)
        if self.frames:
            self.image_label.setPixmap(self.frames[0])
        self.filename_label = QLabel("sprite_00.png")
        self.filename_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.image_label)
        main_layout.addWidget(self.filename_label)
        fps_row = QHBoxLayout()
        fps_text = QLabel("Frames per second")
        self.fps_value_label = QLabel("10 FPS")
        fps_row.addWidget(fps_text)
        fps_row.addStretch()
        fps_row.addWidget(self.fps_value_label)
        main_layout.addLayout(fps_row)
        self.fps_slider = QSlider(Qt.Orientation.Horizontal)
        self.fps_slider.setMinimum(1)
        self.fps_slider.setMaximum(100)
        self.fps_slider.setValue(10)
        self.fps_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.fps_slider.setTickInterval(10)
        self.fps_slider.valueChanged.connect(self.on_fps_changed)
        main_layout.addWidget(self.fps_slider)
        self.start_stop_btn = QPushButton("Start")
        self.start_stop_btn.clicked.connect(self.on_start_stop)
        main_layout.addWidget(self.start_stop_btn)
        self.setCentralWidget(frame)
    def build_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        pause_action = QAction("Pause", self)
        pause_action.triggered.connect(self.pause_animation)
        file_menu.addAction(pause_action)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(QApplication.quit)
        file_menu.addAction(exit_action)
    def on_fps_changed(self, fps_value):
        """updates fps"""
        self.fps_value_label.setText(f"{fps_value} FPS")
        if self.is_animating:
            self.timer.setInterval(int(1000 / fps_value))
    def on_start_stop(self):
        """starts and stops animation"""
        if not self.is_animating:
            fps = self.fps_slider.value()
            self.timer.start(int(1000 / fps))
            self.is_animating = True
            self.start_stop_btn.setText("Stop")
        else:
            self.timer.stop()
            self.is_animating = False
            self.start_stop_btn.setText("Start")
    def next_frame(self):
        """move to next sprite"""
        self.current_frame = (self.current_frame + 1) % self.num_frames
        self.image_label.setPixmap(self.frames[self.current_frame])
        # Build the filename string to match the zero-padded format
        padding = math.ceil(math.log(self.num_frames - 1, 10))
        filename = "sprite_" + str(self.current_frame).rjust(padding, '0') + ".png"
        self.filename_label.setText(filename)
    def pause_animation(self):
        """Stops animation from the File > Pause menu."""
        self.timer.stop()
        self.is_animating = False
        self.start_stop_btn.setText("Start")

def main():
    app = QApplication([])
    # Create our custom application
    window = SpritePreview()
    # And show it
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
