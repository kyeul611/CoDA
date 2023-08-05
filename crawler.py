from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager



import re
import time
import pandas as pd
import itertools
# import json
import traceback

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-usb-devices')
options.add_argument('--blink-settings=imagesEnabled=false') # 이미지 로딩 안함
options.add_experimental_option('excludeSwitches', ['enable-logging']) # selenium 로그 숨김

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

# 정보에 접근하는 class 값 모음. 
# 크롤링이 정상적으로 작동하지 않는다면 아래 정보가 변경되지 않았는지 살펴보라.
global elementNames 
elementNames= {
    'getProdUrls':{
        'item_list':'product_item__MDtDF',
        'shop_list':'product_mall__hPiEH'
    },
    'getProdInfo':{
        'title':'_22kNQuEXmb',
        'price':'_1LY7DqCnwR',
        'delivery_fee':'bd_ChMMo',
        # table은 스토어에서 제공하는 테이블 정보에 접근하는 값이다.
        'table_1':{
            'table':'_1_UiXWHt__',
            'ths':'_1iuv6pLHMD',
            'tds':'ABROiEshTD'

        },
        'table_2':{
            'table':'TH_yvPweZa',
            'ths':'_15qeGNn6Dt',
            'tds':'jvlKiI0U_y'
        },
        'nReview':'_2pgHN-ntx6'
    },
    'getProdReview':{

    }
}

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
                
                time.sleep(0.5)

        else:
            for _ in range(iter):
                driver.execute_script("window.scrollBy(0, window.innerHeight);")
                time.sleep(0.5)

def write_log(method, query, url, err_msg):
    with open(f'logs/{method}_{query}.txt', 'a') as f:
        f.write(url+'\n')
        f.write(err_msg)
        f.write("================== line ==================\n\n")
    
class CrawlingItem:
    def getProdUrls(query, max_pages):
        '''
        상품 상세 페이지로 진입하기 위해 url을 수집하는 메서드
        '''
        product_urls = []

        for page_num in itertools.count(1, 1):
            
            # 네이버 쇼핑 검색 결과 페이지 URL을 생성합니다.
            url = f"https://search.shopping.naver.com/search/all?frm=NVSHCHK&origQuery={query}&pagingIndex={page_num}&pagingSize=20&productSet=checkout&query={query}&sort=review&timestamp=&viewType=list"
            driver.get(url)
            scroll_down() # 모든 컨텐츠가 로드될 때까지 페이지 다운

            # 현재 페이지의 HTML 소스를 가져와 BeutifulSoup 객체를 생성함
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')
            item_list = soup.find_all('div', {'class':elementNames['getProdUrls']['item_list']}) # item list를 모두 가져옴
            shop_list = soup.find_all('a', {'class':elementNames['getProdUrls']['shop_list']}) # 공식 shop의 url 정보를 가져옴
            # print(item_list)
            # 상품 리스트에서 정보를 추출하자.
            for item, shop in zip(item_list, shop_list):
                item_url = item.find('a').get('href')
                shop_url = shop.get('href')
                
                if 'naver.com' in shop_url: # 네이버 스토어 제품이라면
                    product_urls.append(item_url)

            if page_num >= max_pages:
                return product_urls


    def getProdInfo(url, query_t):
        '''
        상품 정보를 수집하는 메서드
        url: 상품 url
        title: log 저장용
        '''
        try:
            print("Now Item title : \"", end="")
            driver.get(url)
            scroll_down(14)
            soup = BeautifulSoup(driver.page_source, 'lxml')

            # 정보
            title = soup.find('h3', {'class':elementNames['getProdInfo']['title']}).text
            price = soup.find_all('span', class_=elementNames['getProdInfo']['price'])[-1].text.replace(',', '') # 가격
            print(title+"\"")

            # 배송비
            delivery_fee = soup.find_all('span', attrs={'class':elementNames['getProdInfo']['delivery_fee']})
            
            delivery_fee = delivery_fee[-1].text

            price_pattern = r'\d{1,3}(,\d{3})*'
            try:
                delivery_fee = re.search(price_pattern, delivery_fee).group()
                delivery_fee =  int(delivery_fee.replace(',', ''))
            except AttributeError:
                delivery_fee = 0

            

            # f-string에 dictionary 중첩문을 적용할 수 없어서 예외적으로 변수로 만들어서 사용함.
            table_1 = elementNames['getProdInfo']['table_1']['table']
            table_2 = elementNames['getProdInfo']['table_2']['table']

            element = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[contains(@class, "{}") or contains(@class, "{}")]'.format(table_1, table_2))
                ))
            e_class = element.get_attribute("class")
            
            ths, tds = [], []
            if e_class == table_1:
                table_soup = soup.find_all('table', {'class':table_1})
                for i in range(2):
                    ths.append(table_soup[i].find_all('th', {'class':elementNames['getProdInfo']['table_1']['ths']}))
                    tds.append(table_soup[i].find_all('td', {'class':elementNames['getProdInfo']['table_1']['tds']}))

            elif e_class == table_2:
                table_soup = soup.find_all('table', {'class':table_2})
                for i in range(2):
                    ths.append(table_soup[i].find_all('th', {'class':elementNames['getProdInfo']['table_2']['ths']}))
                    tds.append(table_soup[i].find_all('td', {'class':elementNames['getProdInfo']['table_2']['tds']}))
            else:
                # 로그로 남길 수 있게 바꾸기
                with open('e_class.txt', 'a') as f:
                    f.write(url+'\t'+e_class+'\n')
            
            columns = ['title', 'price', 'delivery_fee']
            rows = [title, price, delivery_fee]
            # th는 columns, td는 데이터다.
            for th, td in zip(ths, tds):
                for i in range(len(th)):
                    columns.append(th[i].text)
                    rows.append(td[i].text)
            
            # 리뷰수 구하기
            try:
                element = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="REVIEW"]/div/div[3]/div[1]/div[1]/strong/span[@class="{}"]'.format(elementNames['getProdInfo']['nReview']))
                ))
            except TimeoutException or ElementNotInteractableException:
                time.sleep(1)

            nReview = soup.find('strong', {'class':elementNames['getProdInfo']['nReview']})
            nReview = nReview.text.replace(',', '')
            
            columns.append('nReview')
            rows.append(nReview)

            # df로 데이터 저장
            data = {col: [value] for col, value in zip(columns, rows)}
            df = pd.DataFrame(data=data)
            
            return df
        
        except Exception as e:
            # print("error", e)
            # print("type", type(e))
            err_msg = traceback.format_exc()
            write_log('getProdInfo', query_t, url, err_msg )
            return
            

    def getProdReview(pNum, query, nReview):
        '''
        상품의 리뷰 데이터를 수집하는 메서드
        '''
        total_pages = (nReview//20) + 1

        
        # df_review = pd.DataFrame(columns=['p_num', 'user_id', 'score', 'date', 'review', 'is_month', 'is_repurch'])
        
        df_review = pd.DataFrame(columns=['user_id', 'score', 'date', 'review', 'is_month', 'is_repurch'])
        try:
            print(f"리뷰 수집 시작")
            next_btn = driver.find_element(By.XPATH, '//*[@id="REVIEW"]/div/div[3]/div[2]/div/div/a[@class="fAUKm1ewwo _2Ar8-aEUTq"]')
            
            for i in itertools.count(1, 1):
                print(f"현재 리뷰 페이지: {i}/{total_pages}(총 리뷰: {nReview})", end='\r', flush=True)
                
                soup = BeautifulSoup(driver.page_source,'lxml')
                review_ul = soup.find('ul', {'class':'TsOLil1PRz'})
                if review_ul == None:
                    # 리뷰가 없다면 종료
                    break

                scores = review_ul.find_all('em', {'class':'_15NU42F3kT'})
                user_id = review_ul.find_all('strong', {'class':'_3QDEeS6NLn'})
                date_soup = review_ul.find_all('span', {'class':'_3QDEeS6NLn'})
                date = []
                for i in range(0, len(date_soup), 2):
                    date.append(date_soup[i])
                
                review_div = review_ul.find_all('div', {'class':'YEtwtZFLDz'})
                
                reviews, is_month, is_repurch = [], [], []

                # 리뷰를 저장하고 '재구매', '한달사용기' 정보를 판단함
                for div in review_div:
                    review = div.find('span', {'class':'_3QDEeS6NLn'}).text
                    reviews.append(review)
                    re_month = div.find_all('span',{'class':'_1eidska71d'})
                    
                    if len(re_month) >= 2:
                        is_month.append(True)
                        is_repurch.append(True)
                    elif len(re_month) == 0:
                        is_month.append(False)
                        is_repurch.append(False)
                    else:
                        if re_month[0].text == '한달사용기':
                            is_month.append(True)
                            is_repurch.append(False)
                        elif re_month[0].text == '재구매':
                            is_repurch.append(True)
                            is_month.append(False)

                scores = [x.text for x in scores]
                user_id = [x.text for x in user_id]
                date = [x.text for x in date]

                rows = [user_id, scores, date, reviews, is_month, is_repurch]
                for row in zip(*rows):
                    df_review.loc[len(df_review)] = row

                try:
                    next_btn.click()
                    time.sleep(0.5)
                except ElementNotInteractableException:
                    # err_msg = traceback.format_exc()
                    # write_log('getProdReview', pNum, err_msg)
                    break

            
            df_review.drop_duplicates(inplace=True)
            df_review.to_csv(f'reviews/{pNum}.tsv', sep='\t', encoding='utf-8', index=False)
            print("\n")

        except Exception as e:
            err_msg = traceback.format_exc()
            url = driver.current_url
            write_log('getProdReview', query, url, err_msg)
            return

class CrawlingBlog:
    pass