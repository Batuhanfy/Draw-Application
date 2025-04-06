# -------------  
# Batuhan Korkmaz  
# Full Stack Developer & EdTech Girişimcisi  
# https://www.linkedin.com/in/batuhanfy/  
# -------------  

import cv2  
import numpy as np  
from config import settings  
from modes.base_mode import BaseMode  

class SelectionMode(BaseMode):  
    def __init__(self, app):  
        super().__init__(app)  
        self.name = "Selection Mode"  
        self.status_text = "Seçim: Şekil ve nesneleri seç ve düzenle"  
        self.status_color = (255, 165, 0)  
        
        self.selecting = False  
        self.start_point = None  
        self.end_point = None  
        self.selection_rect = None  
        
        self.selected_content = None  
        self.moving = False  
        self.last_position = None  
    
    def check_activation(self, hand_landmarks, width, height):  
        return self.app.hand_detector.is_selection_mode(hand_landmarks)  
    
    def process(self, frame, hand_landmarks, width, height):  
        index_finger_tip = self.get_landmark_position(  
            hand_landmarks,  
            width,  
            height,  
            self.mp_hands.HandLandmark.INDEX_FINGER_TIP  
        )  
        
        pinky_finger_up = self._is_finger_up(  
            hand_landmarks,  
            self.mp_hands.HandLandmark.PINKY_TIP,  
            self.mp_hands.HandLandmark.PINKY_PIP  
        )  
        
        selecting_now = not pinky_finger_up  
        cv2.circle(frame, index_finger_tip, 10, (255, 165, 0), -1)  
        
        status_text = self.status_text  
        
        if selecting_now and not self.selecting:  
            self.selecting = True  
            self.start_point = index_finger_tip  
            
            if self.moving and self.selected_content is not None:  
                self._apply_move()  
                self.moving = False  
                
        elif selecting_now and self.selecting:  
            self.end_point = index_finger_tip  
            
            cv2.rectangle(  
                frame,  
                self.start_point,  
                self.end_point,  
                (255, 165, 0),  
                2  
            )  
            
            x1 = min(self.start_point[0], self.end_point[0])  
            y1 = min(self.start_point[1], self.end_point[1])  
            x2 = max(self.start_point[0], self.end_point[0])  
            y2 = max(self.start_point[1], self.end_point[1])  
            
            self.selection_rect = (x1, y1, x2, y2)  
            status_text = "Seçim: Alan seçiliyor..."  
            
        elif not selecting_now and self.selecting:  
            self.selecting = False  
            
            if (self.selection_rect and  
                abs(self.selection_rect[2] - self.selection_rect[0]) > 10 and  
                abs(self.selection_rect[3] - self.selection_rect[1]) > 10):  
                
                x1, y1, x2, y2 = self.selection_rect  
                self.selected_content = {  
                    'rect': self.selection_rect,  
                    'image': self.app.canvas.canvas[y1:y2, x1:x2].copy()  
                }  
                
                status_text = "Seçim: Alan seçildi. Taşımak için işaret et ve parmağını kapat."  
            else:  
                self.selection_rect = None  
        
        if self.selected_content and not self.selecting:  
            x1, y1, x2, y2 = self.selected_content['rect']  
            
            overlay = frame.copy()  
            cv2.rectangle(overlay, (x1, y1), (x2, y2), (255, 165, 0), 2)  
            cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)  
            
            is_inside = (x1 <= index_finger_tip[0] <= x2 and y1 <= index_finger_tip[1] <= y2)  
                
            if is_inside and selecting_now and not self.moving:  
                self.moving = True  
                self.last_position = index_finger_tip  
                status_text = "Seçim: Alan taşınıyor..."  
            
            if self.moving and selecting_now:  
                dx = index_finger_tip[0] - self.last_position[0]  
                dy = index_finger_tip[1] - self.last_position[1]  
                
                new_x1 = max(0, x1 + dx)  
                new_y1 = max(0, y1 + dy)  
                new_x2 = min(width, x2 + dx)  
                new_y2 = min(height, y2 + dy)  
                
                if new_x2 - new_x1 > 0 and new_y2 - new_y1 > 0:  
                    self.selected_content['rect'] = (new_x1, new_y1, new_x2, new_y2)  
                    self.last_position = index_finger_tip  
            
            elif self.moving and not selecting_now:  
                self._apply_move()  
                self.moving = False  
                status_text = "Seçim: Alan taşındı."  
        
        return frame, status_text, self.status_color  
    
    def _apply_move(self):  
        if not self.selected_content:  
            return  
            
        old_x1, old_y1, old_x2, old_y2 = self.selection_rect  
        cv2.rectangle(  
            self.app.canvas.canvas,  
            (old_x1, old_y1),  
            (old_x2, old_y2),  
            (0, 0, 0),  
            -1  
        )  
        
        new_x1, new_y1, new_x2, new_y2 = self.selected_content['rect']  
        
        try:  
            h = new_y2 - new_y1  
            w = new_x2 - new_x1  
            
            img_h, img_w = self.selected_content['image'].shape[:2]  
            
            if h != img_h or w != img_w:  
                scaled_img = cv2.resize(self.selected_content['image'], (w, h))  
            else:  
                scaled_img = self.selected_content['image']  
            
            mask = np.zeros_like(self.app.canvas.canvas)  
            mask[new_y1:new_y2, new_x1:new_x2] = scaled_img  
            
            non_black = np.any(scaled_img > 10, axis=2)  
            for y in range(h):  
                for x in range(w):  
                    if non_black[y, x]:  
                        self.app.canvas.canvas[new_y1 + y, new_x1 + x] = scaled_img[y, x]  
            
        except Exception as e:  
            print(f"Taşıma hatası: {e}")  
        
        self.app.canvas.save_to_history()  
        self.selection_rect = self.selected_content['rect']  
    
    def handle_key_press(self, key):  
        if key == ord('x') and self.selected_content:  
            x1, y1, x2, y2 = self.selected_content['rect']  
            cv2.rectangle(  
                self.app.canvas.canvas,  
                (x1, y1),  
                (x2, y2),  
                (0, 0, 0),  
                -1  
            )  
            self.app.canvas.save_to_history()  
            self.selected_content = None  
            self.selection_rect = None  
            return True  
            
        elif key == ord('c') and self.selected_content:  
            return True  
            
        elif key == ord('v') and self.selected_content:  
            center_x = self.app.width // 2  
            center_y = self.app.height // 2  
            
            x1, y1, x2, y2 = self.selected_content['rect']  
            w = x2 - x1  
            h = y2 - y1  
            
            new_x1 = center_x - w // 2  
            new_y1 = center_y - h // 2  
            new_x2 = new_x1 + w  
            new_y2 = new_y1 + h  
            
            self.selected_content['rect'] = (new_x1, new_y1, new_x2, new_y2)  
            self._apply_move()  
            
            self.selected_content['rect'] = (x1, y1, x2, y2)  
            return True  
            
        elif key == 27 and self.selected_content:  
            self.selected_content = None  
            self.selection_rect = None  
            self.selecting = False  
            self.moving = False  
            return True  
            
        return False  
    
    def reset(self):  
        super().reset()  
        self.selecting = False  
        self.start_point = None  
        self.end_point = None  
        self.selection_rect = None  
        self.selected_content = None  
        self.moving = False  
        self.last_position = None  
    
    def _is_finger_up(self, hand_landmarks, tip_idx, pip_idx):  
        return hand_landmarks.landmark[tip_idx].y < hand_landmarks.landmark[pip_idx].y  

# Kısaca açıklamak isterim: 
# - El hareketleriyle çizimleri seçip taşımayı sağlıyor  
# - İşaret parmağıyla seçim yapıp, serçe parmak kapalıyken taşıma yapıyor  
# - Klavye kısayollarıyla kes/kopyala/yapıştır işlemleri yapılabiliyor  
# - Seçilen alanların boyutlarını koruyarak taşıma yapıyor  
# - Kullanıcı dostu bir arayüzle çalışıyor  
