# ---------------  
# Batuhan Korkmaz  
# Full Stack Developer & EdTech Girişimcisi  
# https://www.linkedin.com/in/batuhanfy/  
# ---------------  

import os  
from config.settings import *  

DEBUG_MODE = True  

CAMERA_DEVICE = 0  
MAX_HANDS = 2  
DETECTION_CONFIDENCE = 0.7  
TRACKING_CONFIDENCE = 0.7  

CANVAS_OPACITY = 0.5  

AUTO_SAVE = True  
AUTO_SAVE_INTERVAL = 300  

DATA_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")  

# Bu dosya, uygulamanın genişletilmiş ayarlarını içerir.   
# Kamera ve kanvas ayarları, otomatik kaydetme özellikleri ve veri dizini yapılandırması burada tanımlanmıştır.   
# Debug modu aktif edilerek geliştirme sürecinde hata ayıklama kolaylaştırılmıştır.  
