# -----------------------------------------------------------------------------  
# Batuhan Korkmaz  
# Full Stack Developer & EdTech Girişimcisi  
# https://www.linkedin.com/in/batuhanfy/  
# -----------------------------------------------------------------------------  

import os  

CAMERA_WIDTH = 1280  
CAMERA_HEIGHT = 720  
CAMERA_DEVICE = 1  

DEFAULT_PEN_COLOR = (0, 0, 255)  
DEFAULT_PEN_THICKNESS = 5  
MIN_PEN_THICKNESS = 1  
MAX_PEN_THICKNESS = 40  

DEFAULT_FONT_SCALE = 1.5  
DEFAULT_FONT_THICKNESS = 2  
MIN_FONT_SCALE = 0.5  
MAX_FONT_SCALE = 3.0  

MAX_HANDS = 2  
DETECTION_CONFIDENCE = 0.5  
TRACKING_CONFIDENCE = 0.5  

CANVAS_OPACITY = 0.5  
CANVAS_COLOR = (255, 255, 255)  

FPS_LIMIT = 30  
DEBUG_MODE = True  

DEFAULT_ERASER_SIZE = 40  

KEY_CLEAR_CANVAS = ord('c')  
KEY_SAVE_DRAWING = ord('s')  
KEY_UNDO = ord('z')  
KEY_REDO = ord('y')  
KEY_NEXT_MODE = ord('m')  
KEY_PREV_MODE = ord('n')  
KEY_COLOR_CYCLE = ord('p')  
KEY_THICKNESS_INCREASE = ord('+')  
KEY_THICKNESS_DECREASE = ord('-')  
KEY_ERASER_SIZE_INCREASE = ord('=')  
KEY_ERASER_SIZE_DECREASE = ord('-')  

SAVE_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), "saved_drawings")  

STATUS_TEXT = "İşaret parmağıyla çizim yap"  
STATUS_NO_HAND = "El tespit edilemedi"  
STATUS_ERASER = "Silgi Modu: İşaret ve orta parmak ile sil"  
STATUS_ERASER_OFF = "Silgi: Silmek için yüzük parmağını kapat"  
STATUS_GESTURE = "Hareket Modu: El hareketleri ile kontrol et"  

# -----------------------------------------------------------------------------  
# Bu dosya, bir el hareketiyle çizim yapmayı sağlayan uygulamanın ayarlarını içerir.  
# Kamera, çizim, yazı, el tespiti, tuş kontrolleri ve dosya kaydetme gibi tüm  
# temel ayarlar burada tanımlanmıştır. Kodun yapısını bozmadan sadeleştirdim.  
# -----------------------------------------------------------------------------  
