# -----------------------------------------------------------------  
# Batuhan Korkmaz  
# Full Stack Developer & EdTech Girişimcisi  
# https://www.linkedin.com/in/batuhanfy/  
# -----------------------------------------------------------------  

import time  

class FPSCounter:  
    def __init__(self, avg_frames=10):  
        self.prev_time = time.time()  
        self.fps_list = []  
        self.avg_frames = avg_frames  
    
    def update(self):  
        current_time = time.time()  
        fps = 1 / (current_time - self.prev_time)  
        self.prev_time = current_time  
        
        self.fps_list.append(fps)  
        if len(self.fps_list) > self.avg_frames:  
            self.fps_list.pop(0)  
        
        avg_fps = sum(self.fps_list) / len(self.fps_list)  
        return avg_fps  

# -----------------------------------------------------------------  
# Bu dosya, uygulamanın performansını ölçmek için FPS (saniyedeki kare sayısı)   
# hesaplama işlevlerini içerir. FPSCounter sınıfı:  
# - Gerçek zamanlı FPS ölçümü yapar  
# - Belirli bir kare sayısı üzerinden ortalama hesaplar  
# - Performans optimizasyonu için kullanılır  
# -----------------------------------------------------------------  