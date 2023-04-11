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

PATH = 'output_lyrics.csv'  
data = pd.read_csv(r'D:\Users\Documents\Hocki1nam4\DS300_N11\DoAn\crawlyrics\output_lyrics.csv', sep = ',', encoding='utf-8')
tracks = pd.read_csv('dataset/tracks_.csv')
data = data.loc[~data['lyrics'].str.contains("to see lyrics and listen to the full track")]
data = data.drop_duplicates(subset="id_track").reset_index(drop=True)
data['lyrics_split'] = data['lyrics'].str.split()
data['length'] = data['lyrics_split'].str.len()
data.sort_values('length', inplace=True)
# print(str(data.loc[data['id_track'] == '6nrHpOgcdE0KcfnTcWdaZs', 'lyrics']))
data = data.iloc[13931:].drop(columns=['length', 'lyrics_split'])
data.to_csv('output_lyrics_final.csv', encoding='utf-8', index=False)
