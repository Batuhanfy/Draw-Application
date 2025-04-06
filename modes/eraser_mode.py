# -------------  
# Batuhan Korkmaz  
# Full Stack Developer & EdTech Girişimcisi  
# https://www.linkedin.com/in/batuhanfy/  
# -------------  

import cv2  
import numpy as np  
from config import settings  
from modes.base_mode import BaseMode  

class EraserMode(BaseMode):  
    def __init__(self, app):  
        super().__init__(app)  
        self.name = "Eraser Mode"  
        self.status_text = settings.STATUS_ERASER  
        self.status_color = (0, 165, 255)  
        self.erasing = False  
        self.prev_point = None  
        self.eraser_size = settings.DEFAULT_ERASER_SIZE  

    def check_activation(self, hand_landmarks, width, height):  
        return (self._is_finger_up(hand_landmarks, self.mp_hands.HandLandmark.INDEX_FINGER_TIP, self.mp_hands.HandLandmark.INDEX_FINGER_PIP) and  
                self._is_finger_up(hand_landmarks, self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP, self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP))  

    def process(self, frame, hand_landmarks, width, height):  
        index_finger_tip = self.get_landmark_position(  
            hand_landmarks,   
            width,   
            height,   
            self.mp_hands.HandLandmark.INDEX_FINGER_TIP  
        )  
        
        ring_finger_up = self._is_finger_up(  
            hand_landmarks,   
            self.mp_hands.HandLandmark.RING_FINGER_TIP,   
            self.mp_hands.HandLandmark.RING_FINGER_PIP  
        )  
        
        self.erasing = not ring_finger_up  
        
        if self.erasing:  
            cv2.circle(frame, index_finger_tip, self.eraser_size, (0, 0, 0), 2)  
            if self.prev_point is not None:  
                self._erase_line(index_finger_tip)  
            status_text = f"Silgi: Boyut {self.eraser_size}px"  
        else:  
            cv2.circle(frame, index_finger_tip, self.eraser_size, (0, 0, 255), 2)  
            status_text = settings.STATUS_ERASER_OFF  
        
        self.prev_point = index_finger_tip  
        return frame, status_text, self.status_color  

    def _erase_line(self, current_point):  
        if self.prev_point:  
            cv2.line(  
                self.app.canvas.canvas,   
                self.prev_point,   
                current_point,   
                (0, 0, 0),   
                self.eraser_size * 2  
            )  
            cv2.circle(  
                self.app.canvas.canvas,   
                current_point,   
                self.eraser_size,   
                (0, 0, 0),   
                -1  
            )  
        if hash(str(current_point)) % 10 == 0:  
            self.app.canvas.save_to_history()  

    def handle_key_press(self, key):  
        if key == ord('+') or key == ord('='):  
            self.eraser_size = min(self.eraser_size + 5, 100)  
            return True  
        elif key == ord('-') or key == ord('_'):  
            self.eraser_size = max(self.eraser_size - 5, 5)  
            return True  
        return False  

    def reset(self):  
        super().reset()  
        self.erasing = False  
        self.prev_point = None  

    def _is_finger_up(self, hand_landmarks, tip_idx, pip_idx):  
        return hand_landmarks.landmark[tip_idx].y < hand_landmarks.landmark[pip_idx].y  

# -------------  
# KOD AÇIKLAMASI:  
# Bu kod, el hareketleriyle dijital bir kanvas üzerinde silme işlemi yapmayı sağlar.  
# İşaret ve orta parmak kaldırıldığında silme modu aktif olur, yüzük parmağı kaldırıldığında pasifleşir.  
# '+' ve '-' tuşlarıyla silgi boyutunu ayarlayabilirsin.  
# Kodun temel mantığı: elin pozisyonunu algılayıp buna göre silme işlemi yapmak.  
# Bu kodu kullanıcı deneyimini geliştirmek için yazdım.  
# -------------  
