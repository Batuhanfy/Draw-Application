# -----------------------------------------------------------------  
# Batuhan Korkmaz  
# Full Stack Developer & EdTech Girişimcisi  
# https://www.linkedin.com/in/batuhanfy/  
# -----------------------------------------------------------------  

import mediapipe as mp  

class BaseMode:  
    def __init__(self, app):  
        self.app = app  
        self.name = "Base Mode"  
        self.status_text = "Base Mode Active"  
        self.status_color = (255, 255, 255)  
        self.mp_hands = mp.solutions.hands  
    
    def check_activation(self, hand_landmarks, width, height):  
        return False  
    
    def process(self, frame, hand_landmarks, width, height):  
        return frame, self.status_text, self.status_color  
    
    def handle_key_press(self, key):  
        return False  
    
    def reset(self):  
        pass  
    
    def get_landmark_position(self, hand_landmarks, width, height, landmark_idx):  
        landmark = hand_landmarks.landmark[landmark_idx]  
        x = int(landmark.x * width)  
        y = int(landmark.y * height)  
        return (x, y)  

# Bu sınıf, tüm çizim modları için temel işlevselliği sağlar. Alt sınıflar tarafından genişletilerek kullanılır.  
