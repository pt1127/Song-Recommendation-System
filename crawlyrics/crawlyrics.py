from selenium.webdriver.common.keys import Keys
import pause
import json
import jsonlines
import os
import time
import pandas as pd
import numpy as np
from queue import Queue
from threading import Thread
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import csv

def login_spotify(driver):
    url = "https://open.spotify.com/"
    driver.implicitly_wait(10)
    driver.get(url)

    # Login spotify with email and password
    
    driver.find_element(By.CSS_SELECTOR, '#main > div > div.Root__top-container > div.Root__top-bar > header > div.LKFFk88SIRC9QKKUWR5u > button.Button-sc-qlcn5g-0.jsmWVV').click()
    driver.find_element(By.CSS_SELECTOR, '#root > div > div.sc-giYglK.ggrwSq > div > div > button.Button-y0gtbx-0.hpTULc.sc-fFeiMQ.kiLgbd').click()
    ## username
    driver.find_element(By.ID, 'email').send_keys('0329928130')
    ## password
    driver.find_element(By.ID, 'pass').send_keys('bc$2514666')
    driver.find_element(By.ID, 'loginbutton').click()
    time.sleep(5)

def get_link_track(id_track):
    return "https://open.spotify.com/" + "track/" + id_track

def save_file(PATH, data):
    with open(PATH, 'a+', encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)

def crawldata(id_track, driver):
    try:
        url = get_link_track(id_track)
        driver.get(url)
        time.sleep(4)
        # print(driver.page_source)
        # lyrics = driver.find_elements(By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[4]/div[1]/div/div[1]/div//p[contains(@class, "Type__TypeElement-goli3j-0 ipKmGr uzdLGhPskgWtE64HOVL8")]')
        lyrics = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[4]/div[1]/div/div[1]/div')
        return lyrics.text[7:].replace("\n", ". ")
    except NoSuchElementException as e:
        with open('dataset/error.txt', 'a+') as f:
            f.write(url + '\n')
        return ""

PATH = 'output_lyrics.csv'    
driver = webdriver.Edge('msedgedriver.exe')
login_spotify(driver)
data = pd.read_csv('dataset/tracks_.csv')
df = data.iloc[3663:5600].copy()
for idx, row in tqdm(df.iterrows(), total=df.shape[0]):
    row['lyrics'] = crawldata(row['id_track'], driver)
    if row['lyrics'] == "":
        continue
    else:
        value = row.values
        save_file(PATH, value)

# tqdm.pandas(desc='My bar!')
# df['lyrics'] = df.progress_apply(lambda x: crawldata(x['id_track'], driver), axis=1)
# df.to_csv('output_lyrics.csv', mode='a', index=False, header=False)