# Youtube Video Uploader noAPI - Python Script
# Vladimir Popovic - Astrov
# Kovin, 18-Jan-2021

import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyautogui
import glob
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

user_name = open("user_google.txt", "r").readline()
password = open("pass_google.txt", "r").readline()

visibility = 1 ### 1 = PUBLIC
               ### 2 = UNLISTED
               ### 3 or anything else = PRIVATE

driver = webdriver.Chrome(service_log_path='C:/Junk/geckodriver.log')
driver.get('https://www.youtube.com')

driver.implicitly_wait(60)
driver.find_element_by_xpath("/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-button-renderer/a/paper-button").click()

driver.implicitly_wait(60)
driver.find_element_by_id('identifierId').send_keys(user_name)
time.sleep(2)
driver.find_element_by_id('identifierNext').click()
time.sleep(2)
driver.implicitly_wait(60)
driver.find_element_by_name('password').send_keys(password)
time.sleep(2)
driver.find_element_by_id('passwordNext').click()

time.sleep(5)
driver.get('https://studio.youtube.com')

#dirloc = r"C:\396\Atmosfera"

for file in sorted(glob.glob("videos\\*.mp4"), key=numericalSort):

    if not file:
        break

    print("")
    print(file)

    ### CREATE/UPLOAD, WAIT FOR PAGE TO APPEAR
    driver.implicitly_wait(60)
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/ytcp-app/ytcp-entity-page/div/ytcp-header/header/div/ytcp-button").click()
    time.sleep(1)
    driver.implicitly_wait(60)
    driver.find_element_by_xpath("/html/body/ytcp-app/ytcp-entity-page/div/ytcp-header/header/div/ytcp-text-menu/paper-dialog/paper-listbox/paper-item[1]/ytcp-ve/div/div/yt-formatted-string").click()
    time.sleep(1)

    ### SELECT FILES
    driver.implicitly_wait(60)
    driver.find_element_by_xpath("/html/body/ytcp-uploads-dialog/paper-dialog/div/ytcp-uploads-file-picker/div/ytcp-button/div").click()

    ### INPUT FILE PATH
    time.sleep(1.5)
    pyautogui.write(file)
    time.sleep(1)
    pyautogui.press('enter')

    ### TITTLE
    driver.implicitly_wait(60)
    video_title = file.replace("videos\\", "")
    video_title = video_title.replace(".mp4", "")
    #video_title = video_title[5:] # optional rebove x number of letters: [x:] at the begining, [:x] at the end
    input_title = driver.find_element_by_id('textbox')
    input_title.click()
    time.sleep(0.5)
    input_title.clear()
    input_title.send_keys(video_title)
    print('Video title: ' + video_title)
    time.sleep(1)

    ### KIDS?
    driver.implicitly_wait(60)
    driver.find_element_by_xpath('/html/body/ytcp-uploads-dialog/paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-details/div/ytcp-uploads-basics/ytcp-form-audience/ytcp-audience-picker/div[4]/paper-radio-group/paper-radio-button[2]/div[2]').click()
    time.sleep(1)

    ### NEXT BUTTON X2
    driver.implicitly_wait(60)
    driver.find_element_by_id('next-button').click()
    time.sleep(1)
    driver.implicitly_wait(60)
    driver.find_element_by_id('next-button').click()
    time.sleep(1)

    if visibility == 1: ### PUBLIC BUTTON
        driver.implicitly_wait(60)
        driver.find_element_by_xpath('/html/body/ytcp-uploads-dialog/paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[1]/paper-radio-group/paper-radio-button[3]/div[2]').click()
        time.sleep(1)
    elif visibility == 2: ### UNLISTED BUTTON
        driver.implicitly_wait(60)
        driver.find_element_by_xpath('/html/body/ytcp-uploads-dialog/paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[1]/paper-radio-group/paper-radio-button[2]/div[2]').click()
        time.sleep(1)
    else: ### PRIVATE BUTTON
        driver.implicitly_wait(60)
        driver.find_element_by_xpath('/html/body/ytcp-uploads-dialog/paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[1]/paper-radio-group/paper-radio-button[1]/div[2]').click()
        time.sleep(1)

    ### SAVE BUTTON
    driver.implicitly_wait(60)
    driver.find_element_by_id('done-button').click()


    ### IF VIDEO PROCESSIND DIALOG APPEARS
    try:
        element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/ytcp-uploads-still-processing-dialog/ytcp-dialog/paper-dialog/div[3]/ytcp-button/div"))
        )
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/ytcp-uploads-still-processing-dialog/ytcp-dialog/paper-dialog/div[3]/ytcp-button/div").click()
    except:
        time.sleep(2)
        driver.get('https://studio.youtube.com')

    print('done')
