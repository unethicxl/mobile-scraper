import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

modelsRegex = re.compile(r'\/specs\/samsung\/[a-z0-9-]+\/sm-[0-9a-z]+-[0-9]+gb\/')

class Model:
    def __init__(self):
        self.Path = ""
        self.Model = ""
        self.Manufacturer = "samsung"
        self.Device = "z3q"
        self.Width = 0
        self.Height = 0
        self.GPS = False
        self.Gyro = False
        self.Accelerometer = False
        self.Ethernet = False
        self.TouchScreen = False
        self.NFC = False
        self.WiFi = False
        self.AndroidVersion = 0

    def scrape_models(page):
        out = {}
        url = f"https://www.phonemore.com/specs/?brand=5&device=1&network=5&z={page}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        content = response.content
        models = modelsRegex.findall(content.decode("utf-8"))
        
        if not models:
            raise ValueError("No models in result")
        
        for m in models:
            parts = m.split("/")
            model_parsed = "-".join(parts[-2].split("-")[:-1])
            if model_parsed not in out:
                model = Model()
                model.Path = m
                model.Model = model_parsed
                out[model_parsed] = model
        
        return out

    
    def fill_data(model):
        widthHeightRegex = re.compile(r'Display resolution</td><td>[0-9]+x[0-9]+')
        androidVersionRegex = re.compile(r'System version</td><td><a href="/systems/android/[0-9]+/">Android [0-9]+')

        url = "https://www.phonemore.com" + model.Path
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        content = response.content.decode("utf-8")
        
        x = widthHeightRegex.search(content)
        if not x:
            raise ValueError("Unable to get resolution")
        
        resolution = x.group()[27:]
        width, height = map(int, resolution.split("x"))
        model.Width = width
        model.Height = height
        android_ver = androidVersionRegex.search(content)
        if not android_ver:
            raise ValueError("Unable to get android version")
        
        version = int(android_ver.group().split('Android ')[1])
        model.AndroidVersion = version
        
        model.TouchScreen = "Capacitive Multitouch" in content
        model.GPS = "A-GPS" in content
        model.Gyro = "Gyroscope" in content
        model.Accelerometer = "Accelerometer" in content
        model.NFC = '<tr><td>NFC</td><td><span class=item_check></span>Supported</td></tr>' in content
        model.WiFi = '<tr><td>WiFi</td><td><span class=item_check>' in content
