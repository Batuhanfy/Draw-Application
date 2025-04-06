# -------------  
# Batuhan Korkmaz  
# Full Stack Developer & EdTech Girişimcisi  
# https://www.linkedin.com/in/batuhanfy/  
# -------------  

import cv2  
import numpy as np  
from config import settings  
from modes.base_mode import BaseMode  

class DrawingMode(BaseMode):  
    def __init__(self, app):  
        super().__init__(app)  
        self.name = "Drawing Mode"  
        self.status_text = "Çizim: İşaret parmağıyla çiz"  
        self.status_color = (0, 255, 0)  
        self.drawing = False  
        self.prev_point = None  
    
    def check_activation(self, hand_landmarks, width, height):  
        return self.app.hand_detector.is_drawing_mode(hand_landmarks)  
    
    def process(self, frame, hand_landmarks, width, height):  
        index_finger_tip = self.get_landmark_position(  
            hand_landmarks,  
            width,  
            height,  
            self.mp_hands.HandLandmark.INDEX_FINGER_TIP  
        )  
        
        if self.prev_point is None:  
            self.prev_point = index_finger_tip  
            self.drawing = True  
        else:  
            if self.drawing:  
                self.app.canvas.draw_line(self.prev_point, index_finger_tip)  
            self.prev_point = index_finger_tip  
        
        cv2.circle(frame, index_finger_tip, 10, self.app.canvas.pen_color, -1)  
        
        color_name = self._get_color_name(self.app.canvas.pen_color)  
        status_text = f"Çizim: {color_name}, Kalınlık: {self.app.canvas.pen_thickness}px"  
        
        return frame, status_text, self.status_color  
    
    def handle_key_press(self, key):  
        if key == ord('p'):  
            self.app.canvas.cycle_color()  
            return True  
        elif key == ord('+') or key == ord('='):  
            self.app.canvas.increase_thickness()  
            return True  
        elif key == ord('-') or key == ord('_'):  
            self.app.canvas.decrease_thickness()  
            return True  
        return False  
    
    def reset(self):  
        super().reset()  
        self.drawing = False  
        self.prev_point = None  
    
    def _get_color_name(self, color):  
        color_names = {  
            (0, 0, 255): "Kırmızı",  
            (0, 165, 255): "Turuncu",  
            (0, 255, 255): "Sarı",  
            (0, 255, 0): "Yeşil",  
            (255, 0, 0): "Mavi",  
            (255, 0, 255): "Pembe",  
            (255, 255, 255): "Beyaz"  
        }  
        
        min_distance = float('inf')  
        closest_color = "Bilinmeyen"  
        
        for color_code, name in color_names.items():  
            distance = sum((c1 - c2) ** 2 for c1, c2 in zip(color, color_code)) ** 0.5  
            if distance < min_distance:  
                min_distance = distance  
                closest_color = name  
        
        return closest_color  

# Bu kod, el hareketleriyle çizim yapmayı sağlayan modu yönetiyor. İşaret parmağı hareketlerini takip edip  
# canvas üzerinde çizim yapıyor, renk değiştirme ve kalınlık ayarı gibi özellikler ekliyor. 
