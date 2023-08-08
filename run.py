'''
리눅스에서 테스트를 진행해야함.
itemInfo 데이터가 수집될 때마다 일단 저장되도록 변경할 것
이전에 진행한 페이지는 건너뛰는 방법을 고민해보자.
'''

from crawler import CrawlingItem

import pandas as pd
import os
import argparse

if __name__=='__main__':

    # 필요한 폴더 생성
    if not os.path.exists('reviews'):
        os.mkdir('reviews')
    if not os.path.exists('itemData'):
        os.mkdir('itemData')
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # arguement를 받음
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', required=True, help='수집을 원하는 키워드를 입력. 띄어쓰기 사이에는 \\를 넣어줘야함. ex) 패션\\ 안경')
    parser.add_argument('--max_pages', default=1, type=int, help='네이버 쇼핑에서 몇 페이지를 수집할 지 결정. 기본값은 1. 첫페이지만 수집함.')
    args = parser.parse_args()

    query = args.query
    max_pages = args.max_pages

    # query = query.replace(' ', '_') # 파일 저장용 문자열 치환
    query_url = query.replace('_', '%20') # url용 띄어쓰기 문자열 치환

    cItem = CrawlingItem
    product_urls = cItem.getProdUrls(query_url, max_pages)
    
    # query에 해당하는 데이터가 있으면 불러온다.
    if os.path.exists(f'itemData/{query}.csv'):
        df = pd.read_csv(f'itemData/{query}.csv')
        # 여기에 중복 url을 피하도록 product_url 리스트를 수정하자
        exists_items = df['상품번호'].to_list()
    else:
        df = pd.DataFrame()
        exists_items = []

    # 정보와 리뷰 수집
    for url in product_urls:
        item_info = cItem.getProdInfo(url, query)
        if int(item_info.iloc[-1]['상품번호']) in exists_items:
            continue
        
        df = pd.concat([df, item_info], ignore_index=True) # 아이템 정보를 수집 후 기존 정보와 병합
        df.fillna(method='ffill', inplace=True) 
        df.to_csv(f'itemData/{query}.csv', encoding='utf-8', mode='w')
        
        pNum = df.iloc[-1]['상품번호']
        nReview = int(df.iloc[-1]['nReview'])
        cItem.getProdReview(pNum, query, nReview) # 리뷰 수집

    
    
    print("수집 완료!")
