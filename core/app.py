"""
-------------
Batuhan Korkmaz
Full Stack Developer & EdTech Girişimcisi
https://www.linkedin.com/in/batuhanfy/
--------------
"""

import cv2
import time
import numpy as np
from config import settings
from utils.logger import get_logger
from utils.fps_counter import FPSCounter
from core.hand_detector import HandDetector
from core.canvas import Canvas
from modes.drawing_mode import DrawingMode
from modes.eraser_mode import EraserMode
from modes.text_mode import TextMode
from modes.gesture_mode import GestureMode
from modes.selection_mode import SelectionMode

logger = get_logger(__name__)

class AirDrawApp:
    def __init__(self):
        logger.info("AirDraw uygulaması başlatılıyor...")
        
        self.cap = cv2.VideoCapture(settings.CAMERA_DEVICE)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, settings.CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, settings.CAMERA_HEIGHT)
        
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        logger.info(f"Kamera boyutları: {self.width}x{self.height}")
        
        self.hand_detector = HandDetector(
            static_mode=False,
            max_hands=settings.MAX_HANDS,
            detection_confidence=settings.DETECTION_CONFIDENCE,
            tracking_confidence=settings.TRACKING_CONFIDENCE
        )
        
        self.canvas = Canvas(width=self.width, height=self.height)
        self.fps_counter = FPSCounter()
        
        self.modes = [
            DrawingMode(self),
            EraserMode(self),
            TextMode(self),
            SelectionMode(self),
            GestureMode(self)
        ]
        self.current_mode_idx = 0
        self.current_mode = self.modes[self.current_mode_idx]
        
        self.running = False
        self.show_help = False
        self.show_debug = settings.DEBUG_MODE
        
        logger.info("AirDraw uygulaması başlatıldı!")
        
    def run(self):
        self.running = True
        logger.info("Uygulama çalışmaya başladı")
        
        while self.running:
            success, frame = self.cap.read()
            if not success:
                logger.error("Kameradan görüntü alınamadı!")
                break
            
            frame = cv2.flip(frame, 1)
            frame, results = self.hand_detector.find_hands(frame, draw=True)
            
            overlay = frame.copy()
            alpha = settings.CANVAS_OPACITY
            cv2.addWeighted(self.canvas.canvas, alpha, overlay, 1 - alpha, 0, overlay)
            frame = overlay
            
            status_text = settings.STATUS_NO_HAND
            status_color = (0, 0, 255)
            active_mode = None
            
            if results.multi_hand_landmarks:
                for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    if hand_idx >= settings.MAX_HANDS:
                        break
                    
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
                logger.debug(f"Mod değiştirildi: {self.current_mode.name}")
            
            fps = self.fps_counter.update()
            
            if self.show_debug:
                cv2.putText(
                    frame,
                    f"FPS: {int(fps)}",
                    (10, 30),
                    cv2.FONT_HERSHEY_PLAIN,
                    2,
                    (255, 0, 255),
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
            
            cv2.putText(
                frame,
                status_text,
                (10, self.height - 20),
                cv2.FONT_HERSHEY_PLAIN,
                2,
                status_color,
                2
            )
            
            if self.show_help:
                self._draw_help_screen(frame)
            
            cv2.imshow("AirDraw", frame)
            key = cv2.waitKey(1)
            self._handle_key_press(key)
                
        self.cap.release()
        cv2.destroyAllWindows()
        logger.info("Uygulama sonlandırıldı")
    
    def _handle_key_press(self, key):
        if key == -1:
            return
            
        if key == 27:
            logger.info("Uygulama sonlandırılıyor...")
            self.running = False
        elif key == ord('h'):
            self.show_help = not self.show_help
        elif key == ord('d'):
            self.show_debug = not self.show_debug
        elif key == ord('c'):
            self.canvas.clear()
            logger.info("Kanvas temizlendi")
        elif key == ord('s'):
            file_path = self.canvas.save_drawing()
            if file_path:
                logger.info(f"Çizim kaydedildi: {file_path}")
        elif key == ord('z'):
            if self.canvas.undo():
                logger.info("Son işlem geri alındı")
        elif key == ord('y'):
            if self.canvas.redo():
                logger.info("İşlem yeniden yapıldı")
        elif key == ord('m'):
            self.next_mode()
        elif key == ord('n'):
            self.prev_mode()
        else:
            self.current_mode.handle_key_press(key)
    
    def _draw_help_screen(self, frame):
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (self.width, self.height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        cv2.putText(
            frame,
            "AirDraw - Yardım",
            (self.width//2 - 150, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )
        
        help_texts = [
            "ESC: Çıkış",
            "H: Yardım ekranı",
            "D: Debug modu",
            "C: Kanvası temizle",
            "S: Çizimi kaydet",
            "Z: Geri al",
            "Y: Yeniden yap",
            "M: Sonraki mod",
            "N: Önceki mod",
            "P: Renk değiştir",
            "+/-: Kalem/Silgi boyutu",
            "",
            "Modlar:",
            "- İşaret parmağı: Çizim modu",
            "- İşaret + Orta parmak: Silgi modu",
            "- Başparmak + İşaret parmağı kıskaç: Yazı modu",
            "- İşaret + Orta + Yüzük parmak: Seçim modu",
            "- Tüm parmaklar açık: Hareket modu"
        ]
        
        for i, text in enumerate(help_texts):
            cv2.putText(
                frame,
                text,
                (50, 100 + i * 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                1
            )
    
    def next_mode(self):
        self.current_mode.reset()
        self.current_mode_idx = (self.current_mode_idx + 1) % len(self.modes)
        self.current_mode = self.modes[self.current_mode_idx]
        logger.info(f"Mod değiştirildi: {self.current_mode.name}")
    
    def prev_mode(self):
        self.current_mode.reset()
        self.current_mode_idx = (self.current_mode_idx - 1) % len(self.modes)
        self.current_mode = self.modes[self.current_mode_idx]
        logger.info(f"Mod değiştirildi: {self.current_mode.name}")

"""
Bu kod, el hareketleriyle çizim yapmayı sağlayan bir uygulamanın ana sınıfıdır. 
Kamera üzerinden el tespiti yapar, çeşitli çizim modlarını destekler ve kullanıcı 
etkileşimlerini işler. Benim için önemli bir proje çünkü hem eğitim teknolojilerine 
hem de kullanıcı deneyimine dokunuyor. Eğer bir sorunla karşılaşırsanız, 
LinkedIn üzerinden bana ulaşabilirsiniz.
"""
