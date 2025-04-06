# -------------  
# Batuhan Korkmaz  
# Full Stack Developer & EdTech Girişimcisi  
# https://www.linkedin.com/in/batuhanfy/  
# -------------  

import cv2  
import numpy as np  
import math  
from config import settings  
from modes.base_mode import BaseMode  

class ShapeMode(BaseMode):  
    def __init__(self, app):  
        super().__init__(app)  
        self.start_point = None  
        self.current_shape = "rectangle"  
        self.shapes = ["rectangle", "circle", "line", "triangle"]  
        self.shape_index = 0  
        self.is_drawing = False  
        self.status_text = "Şekil Modu: Dikdörtgen"  
        self.status_color = (0, 165, 255)  
    
    def check_activation(self, hand_landmarks, frame_width, frame_height):  
        text_mode_active = self.app.hand_detector.is_text_mode(  
            hand_landmarks, frame_width, frame_height  
        )  
        
        if text_mode_active:  
            self.is_active = False  
            return False  
            
        index_tip = hand_landmarks.landmark[self.app.hand_detector.mp_hands.HandLandmark.INDEX_FINGER_TIP]  
        index_pip = hand_landmarks.landmark[self.app.hand_detector.mp_hands.HandLandmark.INDEX_FINGER_PIP]  
        
        middle_tip = hand_landmarks.landmark[self.app.hand_detector.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]  
        middle_pip = hand_landmarks.landmark[self.app.hand_detector.mp_hands.HandLandmark.MIDDLE_FINGER_PIP]  
        
        ring_tip = hand_landmarks.landmark[self.app.hand_detector.mp_hands.HandLandmark.RING_FINGER_TIP]  
        ring_pip = hand_landmarks.landmark[self.app.hand_detector.mp_hands.HandLandmark.RING_FINGER_PIP]  
        
        self.is_active = (  
            index_tip.y < index_pip.y and   
            middle_tip.y < middle_pip.y and  
            ring_tip.y > ring_pip.y  
        )  
        
        return self.is_active  
    
    def process(self, frame, hand_landmarks, frame_width, frame_height):  
        if not self.is_active:  
            self.is_drawing = False  
            self.start_point = None  
            return frame, "Normal Mod", (0, 0, 255)  
        
        index_x, index_y = self.app.hand_detector.get_landmark_position(  
            hand_landmarks,   
            frame_width,   
            frame_height,   
            self.app.hand_detector.mp_hands.HandLandmark.INDEX_FINGER_TIP  
        )  
        
        cv2.circle(frame, (index_x, index_y), 8, (0, 165, 255), -1)  
        
        thumb_tip = hand_landmarks.landmark[self.app.hand_detector.mp_hands.HandLandmark.THUMB_TIP]  
        thumb_ip = hand_landmarks.landmark[self.app.hand_detector.mp_hands.HandLandmark.THUMB_IP]  
        
        thumb_is_open = thumb_tip.y < thumb_ip.y  
        
        current_point = (index_x, index_y)  
        
        if thumb_is_open and not self.is_drawing:  
            self.start_point = current_point  
            self.is_drawing = True  
        elif not thumb_is_open and self.is_drawing:  
            self.is_drawing = False  
            self.draw_shape_on_canvas(self.start_point, current_point)  
            self.start_point = None  
        
        if self.is_drawing and self.start_point:  
            temp_frame = frame.copy()  
            self.draw_shape_preview(temp_frame, self.start_point, current_point)  
            frame = temp_frame  
        
        self.status_text = f"Şekil Modu: {self.get_shape_name()}"  
        self.status_color = (0, 165, 255)  
        
        return frame, self.status_text, self.status_color  
    
    def get_shape_name(self):  
        if self.current_shape == "rectangle":  
            return "Dikdörtgen"  
        elif self.current_shape == "circle":  
            return "Daire"  
        elif self.current_shape == "line":  
            return "Çizgi"  
        elif self.current_shape == "triangle":  
            return "Üçgen"  
        return "Bilinmeyen Şekil"  
    
    def draw_shape_preview(self, frame, start, end):  
        if self.current_shape == "rectangle":  
            cv2.rectangle(frame, start, end, self.app.canvas.pen_color, self.app.canvas.pen_thickness)  
        elif self.current_shape == "circle":  
            radius = int(np.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2))  
            cv2.circle(frame, start, radius, self.app.canvas.pen_color, self.app.canvas.pen_thickness)  
        elif self.current_shape == "line":  
            cv2.line(frame, start, end, self.app.canvas.pen_color, self.app.canvas.pen_thickness)  
        elif self.current_shape == "triangle":  
            dx = end[0] - start[0]  
            dy = end[1] - start[1]  
            side_length = int(np.sqrt(dx**2 + dy**2))  
            angle = np.arctan2(dy, dx)  
            
            pt1 = start  
            pt2 = (int(start[0] + side_length * np.cos(angle)),   
                   int(start[1] + side_length * np.sin(angle)))  
            pt3 = (int(start[0] + side_length * np.cos(angle + 2*np.pi/3)),   
                   int(start[1] + side_length * np.sin(angle + 2*np.pi/3)))  
            
            triangle_points = np.array([pt1, pt2, pt3])  
            cv2.polylines(frame, [triangle_points], True, self.app.canvas.pen_color, self.app.canvas.pen_thickness)  
    
    def draw_shape_on_canvas(self, start, end):  
        if self.current_shape == "rectangle":  
            cv2.rectangle(self.app.canvas.canvas, start, end, self.app.canvas.pen_color, self.app.canvas.pen_thickness)  
        elif self.current_shape == "circle":  
            radius = int(np.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)  
            cv2.circle(self.app.canvas.canvas, start, radius, self.app.canvas.pen_color, self.app.canvas.pen_thickness)  
        elif self.current_shape == "line":  
            cv2.line(self.app.canvas.canvas, start, end, self.app.canvas.pen_color, self.app.canvas.pen_thickness)  
        elif self.current_shape == "triangle":  
            dx = end[0] - start[0]  
            dy = end[1] - start[1]  
            side_length = int(np.sqrt(dx**2 + dy**2))  
            angle = np.arctan2(dy, dx)  
            
            pt1 = start  
            pt2 = (int(start[0] + side_length * np.cos(angle)),   
                   int(start[1] + side_length * np.sin(angle))  
            pt3 = (int(start[0] + side_length * np.cos(angle + 2*np.pi/3)),   
                   int(start[1] + side_length * np.sin(angle + 2*np.pi/3))  
            
            triangle_points = np.array([pt1, pt2, pt3])  
            cv2.polylines(self.app.canvas.canvas, [triangle_points], True, self.app.canvas.pen_color, self.app.canvas.pen_thickness)  
        
        self.app.canvas.save_to_history()  
    
    def cycle_shape(self):  
        self.shape_index = (self.shape_index + 1) % len(self.shapes)  
        self.current_shape = self.shapes[self.shape_index]  
        return self.current_shape  
    
    def get_status(self):  
        return self.status_text, self.status_color  
        
    def handle_key_press(self, key):  
        if key == ord('s') and self.is_active:  
            self.cycle_shape()  
            print(f"Şekil değiştirildi: {self.get_shape_name()}")  
            return True  
            
        return False  

# Bu kod ne yapıyor?  
# - El hareketleriyle dikdörtgen, daire, çizgi ve üçgen çizmeyi sağlıyor  
# - İşaret parmağıyla şeklin boyutunu belirliyor, başparmakla onaylıyor  
# - 's' tuşuyla şekiller arasında geçiş yapılabiliyor  
# - Gerçek zamanlı önizleme gösteriyor  
# - Çizimleri kanvasa kaydediyor  
# - Kullanımı oldukça kolay ve eğlenceli bir şekil çizme deneyimi sunuyor  
