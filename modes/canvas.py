

-------------
# Batuhan Korkmaz
# Full Stack Developer & EdTech Girişimcisi
# https://www.linkedin.com/in/batuhanfy/
--------------

import cv2
import numpy as np
import os
import datetime
from config import settings

class Canvas:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.pen_color = settings.DEFAULT_PEN_COLOR
        self.pen_thickness = settings.DEFAULT_PEN_THICKNESS
        self.font_scale = settings.DEFAULT_FONT_SCALE
        self.font_thickness = settings.DEFAULT_FONT_THICKNESS
        self.color_palette = [
            (0, 0, 255),
            (0, 165, 255),
            (0, 255, 255),
            (0, 255, 0),
            (255, 0, 0),
            (255, 0, 255),
            (255, 255, 255)
        ]
        self.current_color_idx = 0
        self.history = []
        self.history_idx = -1
        self.max_history = 20
        self.save_to_history()

    def clear(self):
        self.canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.save_to_history()

    def resize(self, width, height):
        new_canvas = np.zeros((height, width, 3), dtype=np.uint8)
        h = min(self.height, height)
        w = min(self.width, width)
        new_canvas[:h, :w] = self.canvas[:h, :w]
        self.canvas = new_canvas
        self.width = width
        self.height = height
        self.save_to_history()

    def draw_line(self, point1, point2):
        cv2.line(self.canvas, point1, point2, self.pen_color, self.pen_thickness)

    def draw_text(self, text, position):
        cv2.putText(
            self.canvas,
            text,
            position,
            cv2.FONT_HERSHEY_SIMPLEX,
            self.font_scale,
            self.pen_color,
            self.font_thickness
        )
        self.save_to_history()

    def cycle_color(self):
        self.current_color_idx = (self.current_color_idx + 1) % len(self.color_palette)
        self.pen_color = self.color_palette[self.current_color_idx]

    def increase_thickness(self):
        self.pen_thickness = min(self.pen_thickness + 2, settings.MAX_PEN_THICKNESS)

    def decrease_thickness(self):
        self.pen_thickness = max(self.pen_thickness - 2, settings.MIN_PEN_THICKNESS)

    def increase_font_scale(self):
        self.font_scale = min(self.font_scale + 0.1, settings.MAX_FONT_SCALE)

    def decrease_font_scale(self):
        self.font_scale = max(self.font_scale - 0.1, settings.MIN_FONT_SCALE)

    def save_drawing(self):
        try:
            if not os.path.exists(settings.SAVE_DIRECTORY):
                os.makedirs(settings.SAVE_DIRECTORY)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(settings.SAVE_DIRECTORY, f"drawing_{timestamp}.png")
            cv2.imwrite(file_path, self.canvas)
            return file_path
        except Exception as e:
            print(f"Kayıt hatası: {e}")
            return None

    def save_to_history(self):
        if self.history_idx < len(self.history) - 1:
            self.history = self.history[:self.history_idx + 1]
        self.history.append(self.canvas.copy())
        self.history_idx = len(self.history) - 1
        if len(self.history) > self.max_history:
            self.history.pop(0)
            self.history_idx -= 1

    def undo(self):
        if self.history_idx > 0:
            self.history_idx -= 1
            self.canvas = self.history[self.history_idx].copy()
            return True
        return False

    def redo(self):
        if self.history_idx < len(self.history) - 1:
            self.history_idx += 1
            self.canvas = self.history[self.history_idx].copy()
            return True
        return False

# Çizim yapma, renk değiştirme, boyut ayarlama, geri alma/yineleme gibi temel işlevleri var.
# Kaydetme özelliği sayesinde çizimleri PNG olarak kaydedebiliyoruz.
# Kullanımı oldukça basit ve eğlenceli bir yapı kurmayı hedefledim.
