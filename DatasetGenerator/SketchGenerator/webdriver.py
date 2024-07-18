import os
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
class WebDriver:
    def __init__(self, w=1200, h=1200):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new") 
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(w, h)
        
    def saveScreenshot(self, filePath, fileName, savePath):
        self.driver.get(("file:///" + os.path.abspath(filePath+"/" + fileName)).replace("\\","/"))
        # time.sleep(3)
        self.driver.save_screenshot(savePath+"/" + fileName.split('.')[0] + '.png')
        # self.driver.get_screenshot_as_file(savePath+"/" + fileName.split('.')[0] + '.png')
        
    def setWindowSize(self, width, height):
        self.driver.set_window_size(width, height)
    def quit(self):
        self.driver.quit()