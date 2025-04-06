# -----------------------------------------------------------------  
# Batuhan Korkmaz  
# Full Stack Developer & EdTech Girişimcisi  
# https://www.linkedin.com/in/batuhanfy/  
# -----------------------------------------------------------------  

import cv2  
import mediapipe as mp  
import numpy as np  
import time  
from config import settings  

class HandDetector:  
    def __init__(self, static_mode=False, max_hands=2, model_complexity=1, detection_confidence=0.5, tracking_confidence=0.5):  
        self.static_mode = static_mode  
        self.max_hands = max_hands  
        self.model_complexity = model_complexity  
        self.detection_confidence = detection_confidence  
        self.tracking_confidence = tracking_confidence  
        
        self.mp_hands = mp.solutions.hands  
        self.mp_drawing = mp.solutions.drawing_utils  
        self.mp_drawing_styles = mp.solutions.drawing_styles  
        
        self.hands = self.mp_hands.Hands(  
            static_image_mode=self.static_mode,  
            max_num_hands=self.max_hands,  
            model_complexity=self.model_complexity,  
            min_detection_confidence=self.detection_confidence,  
            min_tracking_confidence=self.tracking_confidence  
        )  
        
        self.fps_start_time = 0  
        self.fps = 0  
    
    def find_hands(self, frame, draw=True):  
        if time.time() - self.fps_start_time > 1:  
            self.fps_start_time = time.time()  
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
        results = self.hands.process(rgb_frame)  
        
        if draw and results.multi_hand_landmarks:  
            for hand_landmarks in results.multi_hand_landmarks:  
                self.mp_drawing.draw_landmarks(  
                    frame,  
                    hand_landmarks,  
                    self.mp_hands.HAND_CONNECTIONS,  
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),  
                    self.mp_drawing_styles.get_default_hand_connections_style()  
                )  
                
        return frame, results  
    
    def get_landmark_position(self, hand_landmarks, width, height, landmark_idx):  
        landmark = hand_landmarks.landmark[landmark_idx]  
        x = int(landmark.x * width)  
        y = int(landmark.y * height)  
        return (x, y)  
    
    def is_drawing_mode(self, hand_landmarks):  
        return (self._is_finger_up(hand_landmarks, self.mp_hands.HandLandmark.INDEX_FINGER_TIP, self.mp_hands.HandLandmark.INDEX_FINGER_PIP) and  
                not self._is_finger_up(hand_landmarks, self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP, self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP) and  
                not self._is_finger_up(hand_landmarks, self.mp_hands.HandLandmark.RING_FINGER_TIP, self.mp_hands.HandLandmark.RING_FINGER_PIP) and  
                not self._is_finger_up(hand_landmarks, self.mp_hands.HandLandmark.PINKY_TIP, self.mp_hands.HandLandmark.PINKY_PIP))  
    
    def is_text_mode(self, hand_landmarks, width, height):  
        thumb_tip = self.get_landmark_position(hand_landmarks, width, height, self.mp_hands.HandLandmark.THUMB_TIP)  
        index_tip = self.get_landmark_position(hand_landmarks, width, height, self.mp_hands.HandLandmark.INDEX_FINGER_TIP)  
        
        distance = np.sqrt((thumb_tip[0] - index_tip[0])**2 + (thumb_tip[1] - index_tip[1])**2)  
        
        other_fingers_up = (  
            self._is_finger_up(hand_landmarks, self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP, self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP) and  
            self._is_finger_up(hand_landmarks, self.mp_hands.HandLandmark.RING_FINGER_TIP, self.mp_hands.HandLandmark.RING_FINGER_PIP) and  
            self._is_finger_up(hand_landmarks, self.mp_hands.HandLandmark.PINKY_TIP, self.mp_hands.HandLandmark.PINKY_PIP)  
        )  
        
        return distance < 50 and other_fingers_up  
    
    def is_gesture_mode(self, hand_landmarks):  
        return (self._is_finger_up(hand_landmarks, self.mp_hands.HandLandmark.THUMB_TIP, self.mp_hands.HandLandmark.THUMB_IP) and  
                self._is_finger_up(hand_landmarks, self.mp_hands.HandLandmark.INDEX_FINGER_TIP, self.mp_hands.HandLandmark.INDEX_FINGER_PIP) and  
                self._is_finger_up(hand_landmarks, self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP, self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP) and  
                self._is_finger_up(hand_landmarks, self.mp_hands.HandLandmark.RING_FINGER_TIP, self.mp_hands.HandLandmark.RING_FINGER_PIP) and  
                self._is_finger_up(hand_landmarks, self.mp_hands.HandLandmark.PINKY_TIP, self.mp_hands.HandLandmark.PINKY_PIP))  
    
    def is_selection_mode(self, hand_landmarks):  
        return (self._is_finger_up(hand_landmarks, self.mp_hands.HandLandmark.INDEX_FINGER_TIP, self.mp_hands.HandLandmark.INDEX_FINGER_PIP) and  
                self._is_finger_up(hand_landmarks, self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP, self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP) and  
                self._is_finger_up(hand_landmarks, self.mp_hands.HandLandmark.RING_FINGER_TIP, self.mp_hands.HandLandmark.RING_FINGER_PIP) and  
                not self._is_finger_up(hand_landmarks, self.mp_hands.HandLandmark.PINKY_TIP, self.mp_hands.HandLandmark.PINKY_PIP))  
    
    def _is_finger_up(self, hand_landmarks, tip_idx, pip_idx):  
        return hand_landmarks.landmark[tip_idx].y < hand_landmarks.landmark[pip_idx].y  

"""  
Burdaki sınıf, MediaPipe kütüphanesini kullanarak el hareketlerini tespit eder.  
Temel işlevleri:  
- El ve parmak pozisyonlarını algılama  
- Farklı modlar için el hareketlerini tanıma (çizim, yazı, hareket vb.)  
- Gerçek zamanlı performans optimizasyonu  

Kullanımı basit: find_hands() metoduyla görüntü işlenir, diğer metodlarla özel hareketler kontrol edilir.  
"""  
