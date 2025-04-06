
"""  
-------------  
Batuhan Korkmaz  
Full Stack Developer & EdTech Girişimcisi  
https://www.linkedin.com/in/batuhanfy/  
--------------  
"""  

import cv2  
import numpy as np  
import os  
from datetime import datetime  
from config import settings  

def add_status_text(frame, text, color):  
    cv2.putText(  
        frame,  
        text,  
        settings.STATUS_POSITION,  
        cv2.FONT_HERSHEY_SIMPLEX,  
        settings.STATUS_FONT_SCALE,  
        color,  
        settings.STATUS_FONT_THICKNESS  
    )  
    return frame  

def add_color_indicator(frame, color, thickness):  
    h, w = frame.shape[:2]  
    
    cv2.rectangle(frame, (w-60, 10), (w-10, 40), color, -1)  
    cv2.rectangle(frame, (w-60, 10), (w-10, 40), (255, 255, 255), 1)  
    
    cv2.putText(  
        frame,  
        f"Kalinlik: {thickness}",  
        (w-150, 70),  
        cv2.FONT_HERSHEY_SIMPLEX,  
        0.5,  
        (255, 255, 255),  
        1  
    )  
    
    return frame  

def add_help_text(frame, show_extended=False):  
    h, w = frame.shape[:2]  
    
    cv2.putText(  
        frame,  
        "q: Cikis | c: Temizle | m: Renk Degistir | t: Yazi Modu",  
        (10, h-20),  
        cv2.FONT_HERSHEY_SIMPLEX,  
        0.5,  
        (255, 255, 255),  
        1  
    )  
    
    if show_extended:  
        help_texts = [  
            "+/-: Kalin./Incel.",  
            "Enter: Yazi Kaydet",  
            "ESC: Yazi Iptal",  
            "s: Ekrani Kaydet"  
        ]  
        
        for i, text in enumerate(help_texts):  
            cv2.putText(  
                frame,  
                text,  
                (10, h-(20*(i+2))),  
                cv2.FONT_HERSHEY_SIMPLEX,  
                0.5,  
                (200, 200, 200),  
                1  
            )  
    
    return frame  

def save_frame(frame, dirname="saved_frames"):  
    try:  
        if not os.path.exists(dirname):  
            os.makedirs(dirname)  
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  
        filename = f"{dirname}/frame_{timestamp}.png"  
        
        cv2.imwrite(filename, frame)  
        return filename  
    except Exception as e:  
        print(f"Kare kaydedilemedi: {e}")  
        return None  

def add_fps_counter(frame, fps):  
    h, w = frame.shape[:2]  
    
    cv2.putText(  
        frame,  
        f"FPS: {fps:.1f}",  
        (w-100, h-20),  
        cv2.FONT_HERSHEY_SIMPLEX,  
        0.5,  
        (0, 255, 0),  
        1  
    )  
    
    return frame  

def create_debug_view(frame, canvas, hand_landmarks, detector):  
    h, w = frame.shape[:2]  
    
    debug_frame = np.zeros((h, w*3, 3), dtype=np.uint8)  
    
    debug_frame[:, :w] = frame  
    debug_frame[:, w:w*2] = canvas  
    debug_frame[:, w*2:] = cv2.addWeighted(frame, 0.8, canvas, 1.0, 0)  
    
    cv2.putText(debug_frame, "Kamera", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)  
    cv2.putText(debug_frame, "Canvas", (w+10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)  
    cv2.putText(debug_frame, "Sonuc", (w*2+10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)  
    
    return debug_frame  

"""  
Bu dosyada neler var:  
- Görüntü işleme için yardımcı fonksiyonlar  
- Ekrana metin ekleme, renk göstergesi, yardım metni gibi UI öğeleri  
- Frame kaydetme ve FPS gösterme fonksiyonları  
- Debug görünümü oluşturma fonksiyonu  

Kısacası, uygulamanın görsel arayüzünü yöneten fonksiyonlar burada.  
Daha temiz ve modüler bir yapı için bu şekilde ayırdım.  
"""  
