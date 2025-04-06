# -----------------------------------------------------------------  
# Batuhan Korkmaz  
# Full Stack Developer & EdTech Girişimcisi  
# https://www.linkedin.com/in/batuhanfy/  
# -----------------------------------------------------------------  

import cv2  
import mediapipe as mp  
from config import settings  
from modes.base_mode import BaseMode  

class DrawingMode(BaseMode):  
    """El hareketleriyle çizim yapma modu"""  
    
    def __init__(self, app):  
        super().__init__(app)  
        self.name = "Drawing Mode"  
        self.status_text = settings.STATUS_DRAWING  
        self.status_color = (0, 255, 0)  # Yeşil  
        
        self.mp_hands = mp.solutions.hands  
        self.is_drawing = False  
        self.prev_point = None  
        self.shapes = ["free", "line", "rectangle", "circle"]  
        self.current_shape = "free"  
        self.shape_start_point = None  
    
    def check_activation(self, hand_landmarks, width, height):  
        """İşaret parmağı açık, orta parmak kapalı ise çizim modu aktif"""  
        return self.app.hand_detector.is_drawing_mode(hand_landmarks)  
    
    def process(self, frame, hand_landmarks, width, height):  
        """El hareketlerini işle ve çizim yap"""  
        index_finger_tip = self.get_landmark_position(  
            hand_landmarks,   
            width,   
            height,   
            self.mp_hands.HandLandmark.INDEX_FINGER_TIP  
        )  
        
        middle_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]  
        middle_finger_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP]  
        self.is_drawing = middle_finger_tip.y > middle_finger_pip.y  
        
        if not self.is_drawing:  
            self.prev_point = None  
            self.shape_start_point = None  
            return frame, settings.STATUS_PEN_OFF, (0, 0, 255)  
        
        current_point = index_finger_tip  
        
        if self.current_shape == "free":  
            if self.prev_point:  
                self.app.canvas.draw_line(self.prev_point, current_point)  
            self.prev_point = current_point  
        
        elif self.current_shape in ["line", "rectangle", "circle"]:  
            if self.shape_start_point is None:  
                self.shape_start_point = current_point  
            
            temp_canvas = self.app.canvas.canvas.copy()  
            
            if self.current_shape == "line":  
                cv2.line(  
                    frame,   
                    self.shape_start_point,   
                    current_point,  
                    self.app.canvas.pen_color,   
                    self.app.canvas.pen_thickness  
                )  
            elif self.current_shape == "rectangle":  
                cv2.rectangle(  
                    frame,   
                    self.shape_start_point,   
                    current_point,  
                    self.app.canvas.pen_color,   
                    self.app.canvas.pen_thickness  
                )  
            elif self.current_shape == "circle":  
                radius = int(((self.shape_start_point[0] - current_point[0]) ** 2 +   
                            (self.shape_start_point[1] - current_point[1]) ** 2) ** 0.5)  
                cv2.circle(  
                    frame,   
                    self.shape_start_point,   
                    radius,  
                    self.app.canvas.pen_color,   
                    self.app.canvas.pen_thickness  
                )  
            
            ring_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]  
            ring_finger_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_PIP]  
            
            if ring_finger_tip.y < ring_finger_pip.y:  
                if self.current_shape == "line":  
                    cv2.line(  
                        self.app.canvas.canvas,   
                        self.shape_start_point,   
                        current_point,  
                        self.app.canvas.pen_color,   
                        self.app.canvas.pen_thickness  
                    )  
                elif self.current_shape == "rectangle":  
                    cv2.rectangle(  
                        self.app.canvas.canvas,   
                        self.shape_start_point,   
                        current_point,  
                        self.app.canvas.pen_color,   
                        self.app.canvas.pen_thickness  
                    )  
                elif self.current_shape == "circle":  
                    radius = int(((self.shape_start_point[0] - current_point[0]) ** 2 +   
                                (self.shape_start_point[1] - current_point[1]) ** 2) ** 0.5)  
                    cv2.circle(  
                        self.app.canvas.canvas,   
                        self.shape_start_point,   
                        radius,  
                        self.app.canvas.pen_color,   
                        self.app.canvas.pen_thickness  
                    )  
                
                self.shape_start_point = None  
                self.app.canvas.save_to_history()  
        
        status = f"Çizim: {self.get_shape_name(self.current_shape)}"  
        return frame, status, self.status_color  
    
    def handle_key_press(self, key):  
        """Tuş basımlarını işle"""  
        if key == settings.KEY_COLOR_CHANGE:  
            self.app.canvas.cycle_color()  
            print(f"Renk değiştirildi: {self.app.canvas.pen_color}")  
            return True  
        elif key == settings.KEY_THICKNESS_INCREASE or key == ord('+'):  
            self.app.canvas.increase_thickness()  
            print(f"Kalem kalınlığı: {self.app.canvas.pen_thickness}")  
            return True  
        elif key == settings.KEY_THICKNESS_DECREASE or key == ord('-'):  
            self.app.canvas.decrease_thickness()  
            print(f"Kalem kalınlığı: {self.app.canvas.pen_thickness}")  
            return True  
        elif key == settings.KEY_SHAPE_CHANGE:  
            current_index = self.shapes.index(self.current_shape)  
            next_index = (current_index + 1) % len(self.shapes)  
            self.current_shape = self.shapes[next_index]  
            print(f"Şekil değiştirildi: {self.get_shape_name(self.current_shape)}")  
            return True  
        return False  
    
    def get_shape_name(self, shape_id):  
        """Şekil ID'sini kullanıcı dostu bir isme dönüştür"""  
        shape_names = {  
            "free": "Serbest",  
            "line": "Çizgi",  
            "rectangle": "Dikdörtgen",  
            "circle": "Daire"  
        }  
        return shape_names.get(shape_id, shape_id)  
    
    def reset(self):  
        """Mod durumunu sıfırla"""  
        super().reset()  
        self.shape_start_point = None  

# -----------------------------------------------------------------  
# Bu kod, el hareketleriyle çizim yapmayı sağlayan bir modül.  
# Temel işlevler:  
# - Serbest çizim yapma  
# - Şekil çizme (çizgi, dikdörtgen, daire)  
# - Renk ve kalınlık ayarları  
# - Geri alma/yineleme özellikleri  
# -----------------------------------------------------------------  
