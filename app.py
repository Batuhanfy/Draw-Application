# -----------------------------------------------------------------  
# Batuhan Korkmaz  
# Full Stack Developer & EdTech Girişimcisi  
# https://www.linkedin.com/in/batuhanfy/  
# -----------------------------------------------------------------  


import cv2  
import time  
import numpy as np  
from config import settings  
from modules.hand_detector import HandDetector  
from modules.canvas import Canvas  
from modes.drawing_mode import DrawingMode  
from modes.eraser_mode import EraserMode  
from modes.text_mode import TextMode  
from modes.gesture_mode import GestureMode  

class AirDrawApp:  
    def __init__(self):  
        self.cap = cv2.VideoCapture(0)  
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, settings.CAMERA_WIDTH)  
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, settings.CAMERA_HEIGHT)  
        
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))  
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  
        
        self.hand_detector = HandDetector(  
            static_mode=False,  
            max_hands=1,  
            detection_confidence=0.7,  
            tracking_confidence=0.7  
        )  
        
        self.canvas = Canvas(width=self.width, height=self.height)  
        
        self.current_time = 0  
        self.prev_time = 0  
        self.fps = 0  
        
        self.modes = [  
            DrawingMode(self),  
            EraserMode(self),  
            TextMode(self),  
            GestureMode(self)  
        ]  
        self.current_mode_idx = 0  
        self.current_mode = self.modes[self.current_mode_idx]  
        
        print("Uygulama başlatıldı!")  
        
    def run(self):  
        while True:  
            success, frame = self.cap.read()  
            if not success:  
                print("Kamera hatası!")  
                break  
            
            frame = cv2.flip(frame, 1)  
            
            frame, results = self.hand_detector.find_hands(frame, draw=True)  
            
            overlay = frame.copy()  
            alpha = 0.5  
            cv2.addWeighted(self.canvas, alpha, overlay, 1 - alpha, 0, overlay)  
            frame = overlay  
            
            status_text = settings.STATUS_NO_HAND  
            status_color = (0, 0, 255)  
            active_mode = None  
            
            if results.multi_hand_landmarks:  
                for hand_landmarks in results.multi_hand_landmarks:  
                    for mode in self.modes:  
                        if mode.check_activation(hand_landmarks, self.width, self.height):  
                            active_mode = mode  
                            frame, status_text, status_color = mode.process(  
                                frame,   
                                hand_landmarks,   
                                self.width,   
                                self.height  
                            )  
                            break  
            
            if active_mode and active_mode != self.current_mode:  
                self.current_mode.reset()  
                self.current_mode = active_mode  
                self.current_mode_idx = self.modes.index(active_mode)  
            
            self.current_time = time.time()  
            self.fps = 1 / (self.current_time - self.prev_time) if self.current_time != self.prev_time else 0  
            self.prev_time = self.current_time  
            
            cv2.putText(  
                frame,   
                f"FPS: {int(self.fps)}",   
                (10, 30),   
                cv2.FONT_HERSHEY_PLAIN,   
                2,   
                (255, 0, 255),   
                2  
            )  
            
            cv2.putText(  
                frame,   
                status_text,   
                (10, self.height - 20),   
                cv2.FONT_HERSHEY_PLAIN,   
                2,   
                status_color,   
                2  
            )  
            
            mode_text = f"Mod: {self.current_mode.name}"  
            cv2.putText(  
                frame,   
                mode_text,   
                (10, 70),   
                cv2.FONT_HERSHEY_PLAIN,   
                2,   
                self.current_mode.status_color,   
                2  
            )  
            
            cv2.imshow("AirDraw", frame)  
            
            key = cv2.waitKey(1)  
            if key == 27:  
                print("Kapatılıyor...")  
                break  
            elif key == ord('c'):  
                self.canvas.clear()  
                print("Temizlendi")  
            elif key == ord('s'):  
                file_path = self.canvas.save_drawing()  
                if file_path:  
                    print(f"Kaydedildi: {file_path}")  
            elif key == ord('z'):  
                if self.canvas.undo():  
                    print("Geri alındı")  
            elif key == ord('y'):  
                if self.canvas.redo():  
                    print("Yeniden yapıldı")  
            elif key == ord('m'):  
                self.next_mode()  
            elif key == ord('n'):  
                self.prev_mode()  
            else:  
                self.current_mode.handle_key_press(key)  
                
        self.cap.release()  
        cv2.destroyAllWindows()  
    
    def next_mode(self):  
        self.current_mode.reset()  
        self.current_mode_idx = (self.current_mode_idx + 1) % len(self.modes)  
        self.current_mode = self.modes[self.current_mode_idx]  
        print(f"Yeni mod: {self.current_mode.name}")  
    
    def prev_mode(self):  
        self.current_mode.reset()  
        self.current_mode_idx = (self.current_mode_idx - 1) % len(self.modes)  
        self.current_mode = self.modes[self.current_mode_idx]  
        print(f"Yeni mod: {self.current_mode.name}")  

if __name__ == "__main__":  
    app = AirDrawApp()  
    app.run()  

# -----------------------------------------------------------------  
# Bu kod, el hareketleriyle çizim yapmayı sağlayan bir uygulamanın ana sınıfıdır.  
# Kameradan görüntü alır, el hareketlerini tespit eder ve çeşitli modlarda çizim yapar.  
# Modlar arasında geçiş yapılabilir, çizimler kaydedilebilir ve geri alınabilir.  
# Basit ve kullanıcı dostu bir arayüz sunar.  
# -----------------------------------------------------------------  
