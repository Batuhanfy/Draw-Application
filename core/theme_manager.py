 # ------------------------------------------------------------------------------  
# Batuhan Korkmaz  
# Full Stack Developer & EdTech Girişimcisi  
# https://www.linkedin.com/in/batuhanfy/  
# ------------------------------------------------------------------------------  


import json  
import os  
from config import settings  


class ThemeManager:  
   
    
    def __init__(self):  
  
        self.themes = self._load_themes()  
        self.current_theme = "default"  
        
    def _load_themes(self):  
       
        default_themes = {  
            "default": {  
                "background_color": (0, 0, 0),  
                "ui_text_color": (255, 255, 255),  
                "status_text_color": (0, 255, 0),  
                "pen_colors": [  
                    (0, 0, 255),   # Kırmızı  
                    (0, 255, 0),   # Yeşil  
                    (255, 0, 0),   # Mavi  
                    (0, 255, 255), # Sarı  
                    (255, 0, 255), # Mor  
                    (255, 255, 0), # Turkuaz  
                    (255, 255, 255) # Beyaz  
                ],  
                "ui_elements_color": (0, 140, 255)  
            },  
            "light": {  
                "background_color": (255, 255, 255),  
                "ui_text_color": (0, 0, 0),  
                "status_text_color": (0, 100, 0),  
                "pen_colors": [  
                    (0, 0, 200),   # Koyu Kırmızı  
                    (0, 150, 0),   # Koyu Yeşil  
                    (200, 0, 0),   # Koyu Mavi  
                    (0, 150, 150), # Koyu Sarı  
                    (150, 0, 150), # Koyu Mor  
                    (150, 150, 0), # Koyu Turkuaz  
                    (100, 100, 100) # Gri  
                ],  
                "ui_elements_color": (0, 100, 200)  
            },  
            "dark": {  
                "background_color": (40, 40, 40),  
                "ui_text_color": (200, 200, 200),  
                "status_text_color": (0, 255, 0),  
                "pen_colors": [  
                    (0, 0, 255),   # Kırmızı  
                    (0, 255, 100), # Parlak Yeşil  
                    (255, 100, 0), # Turuncu  
                    (0, 255, 255), # Sarı  
                    (255, 0, 255), # Mor  
                    (255, 255, 0), # Turkuaz  
                    (255, 255, 255) # Beyaz  
                ],  
                "ui_elements_color": (60, 140, 255)  
            },  
            "colorful": {  
                "background_color": (40, 10, 40),  
                "ui_text_color": (200, 200, 50),  
                "status_text_color": (50, 255, 150),  
                "pen_colors": [  
                    (0, 0, 255),    # Kırmızı  
                    (0, 255, 0),    # Yeşil  
                    (255, 0, 0),    # Mavi  
                    (0, 255, 255),  # Sarı  
                    (255, 0, 255),  # Mor  
                    (255, 255, 0),  # Turkuaz  
                    (255, 255, 255), # Beyaz  
                    (0, 165, 255),   # Turuncu  
                    (128, 0, 128),   # Mor  
                    (255, 192, 203)  # Pembe  
                ],  
                "ui_elements_color": (0, 200, 255)  
            },  
            "minimal": {  
                "background_color": (0, 0, 0),  
                "ui_text_color": (255, 255, 255),  
                "status_text_color": (200, 200, 200),  
                "pen_colors": [  
                    (255, 255, 255), # Beyaz  
                    (180, 180, 180), # Açık Gri  
                    (120, 120, 120), # Orta Gri  
                    (60, 60, 60)     # Koyu Gri  
                ],  
                "ui_elements_color": (150, 150, 150)  
            }  
        }  
        
        try:  
            file_path = os.path.join('data', 'themes.json')  
            if os.path.exists(file_path):  
                with open(file_path, 'r') as f:  
                    loaded_themes = json.load(f)  
                    combined_themes = {**default_themes, **loaded_themes}  
                    return combined_themes  
            return default_themes  
        except Exception as e:  
            print(f"Temalar yüklenemedi: {e}")  
            return default_themes  
    
    def get_theme(self, theme_name=None):  
      
        theme_to_get = theme_name if theme_name else self.current_theme  
        return self.themes.get(theme_to_get, self.themes.get("default"))  
    
    def set_theme(self, theme_name):  
       
        if theme_name in self.themes:  
            self.current_theme = theme_name  
            return True  
        return False  
    
    def get_pen_colors(self):  
       
        theme = self.get_theme()  
        return theme.get("pen_colors", settings.DEFAULT_PEN_COLOR)  
    
    def get_ui_text_color(self):  
       
        theme = self.get_theme()  
        return theme.get("ui_text_color", (255, 255, 255))  
    
    def get_status_text_color(self):  
    
        theme = self.get_theme()  
        return theme.get("status_text_color", (0, 255, 0))  
    
    def get_ui_elements_color(self):  
       
        theme = self.get_theme()  
        return theme.get("ui_elements_color", (0, 140, 255))  
    
    def save_themes(self):  
      
        try:  
            data_dir = "data"  
            if not os.path.exists(data_dir):  
                os.makedirs(data_dir)  
                
            file_path = os.path.join(data_dir, 'themes.json')  
            
            with open(file_path, 'w') as f:  
                json.dump(self.themes, f, indent=4)  
            return True  
        except Exception as e:  
            print(f"Temalar kaydedilemedi: {e}")  
            return False  

# ------------------------------------------------------------------------------  
# Bu sınıf, uygulamanın tema yönetimini sağlar. Temalar arasında geçiş yapabilir,  
# yeni temalar ekleyebilir ve mevcut temaları kaydedebilirsiniz.  
# ------------------------------------------------------------------------------  
