# -------------  
# Batuhan Korkmaz  
# Full Stack Developer & EdTech Girişimcisi  
# https://www.linkedin.com/in/batuhanfy/  
# -------------  

import cv2  
import time  
import numpy as np  
from config import settings  
from modes.base_mode import BaseMode  

class TextMode(BaseMode):  
    def __init__(self, app):  
        super().__init__(app)  
        self.name = "Text Mode"  
        self.status_text = "Yazı: İşaret parmağı ve başparmak ile yazı ekle"  
        self.status_color = (255, 0, 0)  
        
        self.typing = False  
        self.text = ""  
        self.cursor_position = 0  
        self.text_position = None  
        self.display_text = ""  
        
        self.keyboard_visible = False  
        self.keyboard_layout = [  
            "1234567890<",  
            "QWERTYUIOP",  
            "ASDFGHJKL;",  
            "ZXCVBNM,.?",  
            " _^>(ENTER)"  
        ]  
        self.key_size = 50  
        self.selected_key = None  
        self.key_press_time = 0  
        self.key_cooldown = 0.5  

    def check_activation(self, hand_landmarks, width, height):  
        return self.app.hand_detector.is_text_mode(hand_landmarks, width, height)  

    def process(self, frame, hand_landmarks, width, height):  
        # Kıskaç hareketi kontrolü  
        thumb_tip = self.get_landmark_position(hand_landmarks, width, height, self.mp_hands.HandLandmark.THUMB_TIP)  
        index_tip = self.get_landmark_position(hand_landmarks, width, height, self.mp_hands.HandLandmark.INDEX_FINGER_TIP)  
        pinch_distance = np.sqrt((thumb_tip[0] - index_tip[0])**2 + (thumb_tip[1] - index_tip[1])**2)  
        is_pinching = pinch_distance < 40  

        # Yazı pozisyonu (başparmak ve işaret parmağı ortası)  
        position = ((thumb_tip[0] + index_tip[0]) // 2, (thumb_tip[1] + index_tip[1]) // 2)  

        # Kıskaç hareketi bırakıldığında yazı modunu sıfırla  
        if not is_pinching and self.typing:  
            self.typing = False  
            self.start_point = None  
            self.keyboard_visible = False  

        # Kıskaç hareketi başladığında yeni yazı pozisyonunu belirle  
        if is_pinching:  
            if not self.typing:  
                self.typing = True  
                self.text_position = position  # Yeni pozisyon  
                self.keyboard_visible = True  
                if not self.text:  # Yeni yazı başlıyorsa  
                    self.cursor_position = 0  

            # Klavye tuş seçimi (mevcut kod)  
            if self.keyboard_visible:  
                selected_key = self._get_key_at_position(position)  
                if selected_key and selected_key != self.selected_key:  
                    self.selected_key = selected_key  
                    self.key_press_time = time.time()  
                elif selected_key and selected_key == self.selected_key and time.time() - self.key_press_time > self.key_cooldown:  
                    self._process_key_press(selected_key)  
                    self.key_press_time = time.time()  

        # Diğer işlemler (mevcut kod)  
        if self.typing:  
            # İmleç ve yazı gösterimi  
            cursor_char = "|" if int(time.time() * 2) % 2 == 0 else " "  
            display_text = self.text[:self.cursor_position] + cursor_char + self.text[self.cursor_position:]  
            # Yazı kutusunu çiz  
            text_box_padding = 10  
            text_size = cv2.getTextSize(display_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]  
            cv2.rectangle(  
                frame,  
                (self.text_position[0] - text_box_padding, self.text_position[1] - text_size[1] - text_box_padding),  
                (self.text_position[0] + text_size[0] + text_box_padding, self.text_position[1] + text_box_padding),  
                (255, 255, 255),  
                -1  
            )  
            cv2.putText(  
                frame,  
                display_text,  
                self.text_position,  
                cv2.FONT_HERSHEY_SIMPLEX,  
                1,  
                (0, 0, 0),  
                2  
            )  

        # Kıskaç durumunu göster  
        pinch_color = (0, 255, 0) if is_pinching else (0, 0, 255)  
        cv2.line(frame, thumb_tip, index_tip, pinch_color, 2)  

        return frame, self.status_text, self.status_color  
    
    def _draw_keyboard(self, frame, position):  
        start_x = max(10, position[0] - 150)  
        start_y = max(100, position[1] - 150)  
        
        cv2.rectangle(  
            frame,  
            (start_x - 10, start_y - 10),  
            (start_x + len(self.keyboard_layout[0]) * self.key_size + 10, start_y + len(self.keyboard_layout) * self.key_size + 10),  
            (200, 200, 200),  
            -1  
        )  
        
        for row_idx, row in enumerate(self.keyboard_layout):  
            for col_idx, key in enumerate(row):  
                key_x = start_x + col_idx * self.key_size  
                key_y = start_y + row_idx * self.key_size  
                
                key_color = (150, 150, 150)  
                if key == self.selected_key:  
                    key_color = (100, 200, 255)  
                
                cv2.rectangle(  
                    frame,  
                    (key_x, key_y),  
                    (key_x + self.key_size, key_y + self.key_size),  
                    key_color,  
                    -1  
                )  
                
                cv2.rectangle(  
                    frame,  
                    (key_x, key_y),  
                    (key_x + self.key_size, key_y + self.key_size),  
                    (50, 50, 50),  
                    1  
                )  
                
                cv2.putText(  
                    frame,  
                    key,  
                    (key_x + 15, key_y + 35),  
                    cv2.FONT_HERSHEY_SIMPLEX,  
                    0.6,  
                    (0, 0, 0),  
                    2  
                )  
    
    def _get_key_at_position(self, position):  
        x, y = position  
        
        start_x = max(10, position[0] - 150)  
        start_y = max(100, position[1] - 150)  
        
        if (x < start_x or   
            x > start_x + len(self.keyboard_layout[0]) * self.key_size or  
            y < start_y or   
            y > start_y + len(self.keyboard_layout) * self.key_size):  
            return None  
        
        row_idx = (y - start_y) // self.key_size  
        col_idx = (x - start_x) // self.key_size  
        
        if (row_idx >= 0 and row_idx < len(self.keyboard_layout) and  
            col_idx >= 0 and col_idx < len(self.keyboard_layout[row_idx])):  
            return self.keyboard_layout[row_idx][col_idx]  
        
        return None  
    
    def _process_key_press(self, key):  
        if key == "<":  
            if self.cursor_position > 0:  
                self.text = self.text[:self.cursor_position-1] + self.text[self.cursor_position:]  
                self.cursor_position -= 1  
        elif key == "(ENTER)":  
            self.display_text = self.text  
            
            if self.text_position and self.display_text:  
                self.app.canvas.draw_text(self.display_text, self.text_position)  
            
            self.reset()  
        elif key == "_":  
            self.text = self.text[:self.cursor_position] + " " + self.text[self.cursor_position:]  
            self.cursor_position += 1  
        elif key == "^":  
            if self.cursor_position > 0:  
                self.cursor_position -= 1  
        elif key == ">":  
            if self.cursor_position < len(self.text):  
                self.cursor_position += 1  
        else:  
            self.text = self.text[:self.cursor_position] + key + self.text[self.cursor_position:]  
            self.cursor_position += 1  
    
    def handle_key_press(self, key):  
        if self.typing:  
            if key == 8:  
                if self.cursor_position > 0:  
                    self.text = self.text[:self.cursor_position-1] + self.text[self.cursor_position:]  
                    self.cursor_position -= 1  
                return True  
            elif key == 13:  
                self.display_text = self.text  
                
                if self.text_position and self.display_text:  
                    self.app.canvas.draw_text(self.display_text, self.text_position)  
                
                self.reset()  
                return True  
            elif key == 27:  
                self.reset()  
                return True  
            elif key in range(32, 127):  
                char = chr(key)  
                self.text = self.text[:self.cursor_position] + char + self.text[self.cursor_position:]  
                self.cursor_position += 1  
                return True  
        
        if key == ord('f'):  
            self.app.canvas.increase_font_scale()  
            return True  
        elif key == ord('v'):  
            self.app.canvas.decrease_font_scale()  
            return True  
        
        return False  
    
    def reset(self):  
        super().reset()  
        self.typing = False  
        self.text = ""  
        self.cursor_position = 0  
        self.text_position = None  
        self.keyboard_visible = False  
        self.selected_key = None  

# Bu kod, el hareketleriyle yazı yazmayı sağlayan bir modül.   
# İşaret parmağı ve başparmak hareketleriyle sanal klavyeyi kontrol edip yazı yazabiliyorsun.  
# Yazıyı tamamladığında direkt olarak kanvasa çiziliyor.  
# Klavyeyi kapatmak için ESC tuşuna basabilirsin.  
