# -----------------------------------------------------------------  
# Batuhan Korkmaz  
# Full Stack Developer & EdTech Girişimcisi  
# https://www.linkedin.com/in/batuhanfy/  
# -----------------------------------------------------------------  

import logging  
import os  
from datetime import datetime  

def get_logger(name):  
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")  
    
    if not os.path.exists(log_dir):  
        os.makedirs(log_dir)  
    
    timestamp = datetime.now().strftime("%Y%m%d")  
    log_file = os.path.join(log_dir, f"airdraw_{timestamp}.log")  
    
    logger = logging.getLogger(name)  
    
    if logger.handlers:  
        return logger  
    
    logger.setLevel(logging.DEBUG)  
    
    file_handler = logging.FileHandler(log_file)  
    file_handler.setLevel(logging.DEBUG)  
    
    console_handler = logging.StreamHandler()  
    console_handler.setLevel(logging.INFO)  
    
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'  
    formatter = logging.Formatter(log_format)  
    
    file_handler.setFormatter(formatter)  
    console_handler.setFormatter(formatter)  
    
    logger.addHandler(file_handler)  
    logger.addHandler(console_handler)  
    
    return logger  

# -----------------------------------------------------------------  
# Bu dosya, uygulama için loglama işlemlerini yönetir.  
# Hata ayıklama ve bilgilendirme mesajlarını hem dosyaya hem de konsola yazar.  
# Kullanımı basit: get_logger("modul_adi") şeklinde çağırıp log atabilirsin.  
# -----------------------------------------------------------------  
