'''
headless 모드에서도 진행상황을 파악할 수 있도록 적절한 출력을 작성하자.
어디가 진행중인지,
완료된 사항에 대해서는 몇가지 데이터가 수집되었는지 등등

getProdInfo: price와 title 정보 추가되도록해야함
'''

from crawler import CrawlingItem

import pandas as pd
import os

if __name__=='__main__':

    if not os.path.exists('reviews'):
        os.mkdir('reviews')
    if not os.path.exists('itemData'):
        os.mkdir('itemData')

    query = '애견 장난감'
    max_pages = 1

    title = query.replace(' ', '_') # 파일 저장용 문자열 치환
    query = query.replace(' ', '%20') # 띄어쓰기 문자열 치환

    cItem = CrawlingItem
    product_urls = cItem.getProdUrls(query, max_pages)


    # product_urls = ['https://smartstore.naver.com/petagon/products/2199261531?NaPm=ct%3Dlkrxplfs%7Cci%3D3bca062be38fa862a52a85df98d504c072d49d19%7Ctr%3Dslsl%7Csn%3D441903%7Chk%3De1bf006b15c1e12b4a3dcc47e6ecd9a827862622']

    df = pd.DataFrame()
    for url in product_urls:
        print(f"now=>   {url}")
        df = pd.concat([df, cItem.getProdInfo(url)], ignore_index=True)
        cItem.getProdReview(df.iloc[-1, 0])
    
    
    df.to_csv(f'itemData/{title}.csv', encoding='utf-8')
