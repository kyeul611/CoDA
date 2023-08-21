'''
작성자: SorryKim
'''

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

import re
import time
import pandas as pd
import itertools
import traceback

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-usb-devices')
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

# 크롤링 url, 키워드
url = 'https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=ALL&orderBy=sim&keyword='
keyword = ''

try: # 이미 설치된 크롬드라이버가 있으면 
    driver = webdriver.Chrome(options=options)
except: # 없으면 설치
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 5)

def scroll_down(iter=max):
        '''
        동적 웹 페이지의 모든 컨텐츠를 로드하기 위해 스크롤을 내리는 메서드
        iter: 내리는 횟수
        '''
        if iter == max:
            last_position = 0
            while True:
                driver.execute_script("window.scrollBy(0, window.innerHeight);")
                current_position = driver.execute_script("return window.pageYOffset;")

                if current_position == last_position:
                    break
                else:
                    last_position = current_position
                
                time.sleep(0.75)

        else:
            for _ in range(iter):
                driver.execute_script("window.scrollBy(0, window.innerHeight);")
                time.sleep(0.75)


class CrawlingItem:
    
    def getProdUrls(query, max_pages):
        '''
        상품 상세 페이지로 진입하기 위해 url을 수집하는 메서드
        '''

        print("상품 URL을 수집중입니다. 수집한 URL의 개수 : ", end='')
        product_urls = []

        for page_num in itertools.count(1, 1):

            # 블로그 검색 url
            url = f"https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=ALL&orderBy=sim&keyword={query}"
            driver.get(url)
            scroll_down() # 모든 컨텐츠가 로드될 때까지 페이지 다운

            # 현재 페이지의 HTML 소스를 가져와 BeutifulSoup 객체를 생성함
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')
            url_list = soup.find_all('a', {'class': 'desc_inner'}) # 블로그의 url 정보를 가져옴
            
            if len(url_list) == 0:
                #write_log('getProdUrls', query, url, page_source)
                print("페이지 로드 안됨")
                exit() # 프로그램 종료
            
            # print(item_list)
            # 상품 리스트에서 정보를 추출하자.
            for url in url_list:
                item_url = url.get('href')  
                product_urls.append(item_url)

            # 범위 초과했을 경우
            if page_num >= max_pages:
                print(len(product_urls))
                return product_urls

        



