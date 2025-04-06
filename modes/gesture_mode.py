# -------------  
# Batuhan Korkmaz  
# Full Stack Developer & EdTech Girişimcisi  
# https://www.linkedin.com/in/batuhanfy/  
# -------------  

import cv2  
import mediapipe as mp  
import numpy as np  
import time  
from config import settings  
from modes.base_mode import BaseMode  

class GestureMode(BaseMode):  
    def __init__(self, app):  
        super().__init__(app)  
        self.name = "Gesture Mode"  
        self.status_text = settings.STATUS_GESTURE  
        self.status_color = (255, 0, 255)  
        
        self.mp_hands = mp.solutions.hands  
        
        self.last_gesture_time = 0  
        self.gesture_cooldown = 1.0  
        self.last_positions = []  
        self.position_history_max = 10  
        
        self.gestures = {  
            "swipe_right": "Sağa Kaydır: Sonraki Mod",  
            "swipe_left": "Sola Kaydır: Önceki Mod",  
            "swipe_up": "Yukarı Kaydır: Temizle",  
            "swipe_down": "Aşağı Kaydır: Kaydet",  
            "circle": "Daire: Renk Değiştir",  
            "pinch": "Sıkıştır: Geri Al",  
            "spread": "Genişlet: İleri Al",  
            "fist": "Yumruk: Yeni Sayfa",  
            "palm": "Avuç: Kapat"  
        }  
        
        self.detecting_gesture = False  
        self.current_gesture = None  
        self.gesture_start_time = 0  
        self.gesture_positions = []  
    
    def check_activation(self, hand_landmarks, width, height):  
        return self.app.hand_detector.is_gesture_mode(hand_landmarks)  
    
    def process(self, frame, hand_landmarks, width, height):  
        current_position = self.get_landmark_position(  
            hand_landmarks,   
            width,   
            height,   
            self.mp_hands.HandLandmark.INDEX_FINGER_TIP  
        )  
        
        self.last_positions.append(current_position)  
        if len(self.last_positions) > self.position_history_max:  
            self.last_positions.pop(0)  
        
        self._draw_position_history(frame)  
        
        if not self.detecting_gesture:  
            self.detecting_gesture = True  
            self.gesture_start_time = time.time()  
            self.gesture_positions = [current_position]  
            self.current_gesture = None  
        else:  
            self.gesture_positions.append(current_position)  
            
            current_time = time.time()  
            if current_time - self.gesture_start_time > 1.0:  
                detected_gesture = self._recognize_gesture(self.gesture_positions)  
                
                if detected_gesture and current_time - self.last_gesture_time > self.gesture_cooldown:  
                    self.current_gesture = detected_gesture  
                    self.last_gesture_time = current_time  
                    self._execute_gesture_action(detected_gesture)  
                
                self.detecting_gesture = False  
                self.gesture_positions = []  
        
        status_text = self.status_text  
        if self.current_gesture:  
            status_text = f"Hareket: {self.gestures.get(self.current_gesture, self.current_gesture)}"  
            
        self._draw_gesture_list(frame)  
        
        return frame, status_text, self.status_color  
    
    def _draw_position_history(self, frame):  
        if len(self.last_positions) < 2:  
            return  
            
        for i in range(1, len(self.last_positions)):  
            cv2.line(  
                frame,   
                self.last_positions[i-1],   
                self.last_positions[i],   
                (0, 255, 255),   
                2  
            )  
    
    def _draw_gesture_list(self, frame):  
        height, width = frame.shape[:2]  
        
        cv2.rectangle(  
            frame,   
            (width - 300, 50),   
            (width - 20, 50 + 30 * len(self.gestures)),   
            (0, 0, 0),   
            -1  
        )  
        
        for i, (gesture, description) in enumerate(self.gestures.items()):  
            y_pos = 70 + i * 30  
            color = (0, 255, 0) if gesture == self.current_gesture else (255, 255, 255)  
            
            cv2.putText(  
                frame,   
                description,   
                (width - 290, y_pos),   
                cv2.FONT_HERSHEY_SIMPLEX,   
                0.5,   
                color,   
                1  
            )  
    
    def _recognize_gesture(self, positions):  
        if len(positions) < 5:  
            return None  
            
        start_pos = positions[0]  
        end_pos = positions[-1]  
        
        dx = end_pos[0] - start_pos[0]  
        dy = end_pos[1] - start_pos[1]  
        
        min_swipe_distance = 100  
        
        if abs(dx) > min_swipe_distance and abs(dx) > abs(dy) * 2:  
            if dx > 0:  
                return "swipe_right"  
            else:  
                return "swipe_left"  
        elif abs(dy) > min_swipe_distance and abs(dy) > abs(dx) * 2:  
            if dy > 0:  
                return "swipe_down"  
            else:  
                return "swipe_up"  
        
        if len(positions) > 10:  
            center_x = sum(p[0] for p in positions) / len(positions)  
            center_y = sum(p[1] for p in positions) / len(positions)  
            
            distances = [((p[0] - center_x)**2 + (p[1] - center_y)**2)**0.5 for p in positions]  
            avg_distance = sum(distances) / len(distances)  
            
            std_dev = (sum((d - avg_distance)**2 for d in distances) / len(distances))**0.5  
            
            start_end_distance = ((start_pos[0] - end_pos[0])**2 + (start_pos[1] - end_pos[1])**2)**0.5  
            
            if std_dev < 15 and start_end_distance < avg_distance:  
                return "circle"  
        
        return None  
    
    def _execute_gesture_action(self, gesture):  
        if gesture == "swipe_right":  
            self.app.next_mode()  
            
        elif gesture == "swipe_left":  
            self.app.prev_mode()  
            
        elif gesture == "swipe_up":  
            self.app.canvas.clear()  
            print("Kanvas temizlendi")  
            
        elif gesture == "swipe_down":  
            file_path = self.app.canvas.save_drawing()  
            if file_path:  
                print(f"Çizim kaydedildi: {file_path}")  
            
        elif gesture == "circle":  
            self.app.canvas.cycle_color()  
            print(f"Renk değiştirildi: {self.app.canvas.pen_color}")  
            
        elif gesture == "pinch":  
            if self.app.canvas.undo():  
                print("Son işlem geri alındı")  
            
        elif gesture == "spread":  
            if self.app.canvas.redo():  
                print("İşlem yeniden yapıldı")  
    
    def handle_key_press(self, key):  
        return False  
    
    def reset(self):  
        super().reset()  
        self.last_positions = []  
        self.detecting_gesture = False  
        self.gesture_positions = []  

# Bu kod, el hareketleriyle uygulamayı kontrol etmek için kullanılıyor.  
# Sağa/sola kaydırma mod değiştiriyor, yukarı/aşağı kaydırma temizleme/kaydetme yapıyor.  
# Daire çizince renk değişiyor, sıkıştırma/uzatma geri alma/ileri alma yapıyor.  
# Kısacası el hareketleriyle uygulamayı kontrol etmek için tüm mantık burada.  
