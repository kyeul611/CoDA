from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import chromedriver_autoinstaller

import re
import time
import pandas as pd
import itertools

chromedriver_autoinstaller.install()
options = Options()
# options.add_argument('--headless')
options.add_argument('--disable-usb-devices')

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

class Crawler:
    def __init__(self):
        self.driver = webdriver.Chrome(options=options)

    def scroll_dwon(self, iter=max):
        '''
        동적 웹 페이지의 모든 컨텐츠를 로드하기 위해 스크롤을 내리는 메서드
        iter: 내리는 횟수
        '''

        if iter == max:
            last_position = 0
            while True:
                self.driver.execute_script("window.scrollBy(0, window.innerHeight);")
                current_position = self.driver.execute_script("return window.pageYOffset;")

                if current_position == last_position:
                    break
                else:
                    last_position = current_position
                
                time.sleep(1)

        else:
            for _ in range(iter):
                self.driver.execute_script("window.scrollBy(0, window.innerHeight);")
                time.sleep(1)


    def getProdUrls(self, query, max_pages):
        '''
        상품 상세 페이지로 진입하기 위해 url을 수집하는 메서드
        '''
        product_urls = []

        for page_num in itertools.count(1, 1):
            
            # 네이버 쇼핑 검색 결과 페이지 URL을 생성합니다.
            url = f"https://search.shopping.naver.com/search/all?frm=NVSHCHK&origQuery={query}&pagingIndex={page_num}&pagingSize=20&productSet=checkout&query={query}&sort=review&timestamp=&viewType=list"
            self.driver.get(url)
            self.scroll_down()

            # 현재 페이지의 HTML 소스를 가져와 BeutifulSoup 객체를 생성함
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')
            item_list = soup.find_all('div', class_='product_item__MDtDF')
            
            # print(item_list)
            # 상품 리스트에서 정보를 추출하자.
            for item in item_list:
                m_url = item.find('a').get('href')
                
                if 'naver.com' in m_url: # 네이버 스토어 제품이라면
                    product_urls.append(m_url)
                    
            if page_num >= max_pages:
                return product_urls


    def getProdInfo(self):
        '''
        상품 정보를 수집하는 메서드
        '''
        pass

    def getProdReview(self):
        '''
        상품의 리뷰 데이터를 수집하는 메서드
        '''
        pass