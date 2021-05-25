from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver_path = '/home/nur/Downloads/chromedriver_linux64/chromedriver'

class Youtube:

    def getBrowser(self):
        self.browser = webdriver.Chrome(driver_path)
        self.browser.get('https://www.youtube.com/channel/UCPJJbWeR2r1Rs_FWQhsPaFw')
        self.browser.maximize_window()

    def getData(self):

        videoList = []

        # kanal logosu
        with open('SeleniumYoutube/Logo.png', 'wb') as file:
            img = self.browser.find_element(By.XPATH, '//img[@id="img"]')
            file.write(img.screenshot_as_png)
        
        videosButton = self.browser.find_element(By.XPATH, '//div[@id="tabsContent"]/tp-yt-paper-tab[2]/div[1]')
        videosButton.click()
        time.sleep(2)

        # kanal adi
        channelName = self.browser.find_element(By.CLASS_NAME, 'ytd-channel-name').text
        # kanal abone sayisi
        subscribers = self.browser.find_element(By.ID, 'subscriber-count').text

        videosCount = len(self.browser.find_elements(By.CSS_SELECTOR,'ytd-grid-video-renderer'))

        while True:
            
            last_height = self.browser.execute_script('return document.documentElement.scrollHeight')

            self.browser.execute_script('window.scrollTo(0,document.documentElement.scrollHeight)')
            time.sleep(2)
            new_height = self.browser.execute_script('return document.documentElement.scrollHeight')
            if(last_height == new_height):
                break
            last_height = new_height

            newCount = len(self.browser.find_elements(By.CSS_SELECTOR,'ytd-grid-video-renderer'))
            if videosCount != newCount:
                videosCount = newCount
                #print(f'second count : {newCount}')
                time.sleep(1)
            else:
                break

        videoTitles = self.browser.find_elements(By.ID, 'video-title')
        views = self.browser.find_elements(By.CSS_SELECTOR, '#metadata-line > span:nth-child(1)')

        for title, view in zip(videoTitles, views):  
            videoList.append(f'Video Adı : {title.text} - Görüntüleme Sayısı : {view.text}')
        
        with open('SeleniumYoutube/videos.txt','w') as file:
            file.write(f'Kanal Adı : {channelName} - Abone Sayısı : {subscribers}\n')
            index = 1
            for item in videoList:
                file.write(str(index)+'.'+item +'\n')
                index += 1
        self.closeBrowser()
    
    def closeBrowser(self):
        
        self.browser.close()


youtube = Youtube()
youtube.getBrowser()
youtube.getData()