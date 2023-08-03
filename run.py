'''
리눅스에서 테스트를 진행해야함.
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

    query_t = query.replace(' ', '_') # 파일 저장용 문자열 치환
    query = query.replace(' ', '%20') # url용 띄어쓰기 문자열 치환

    cItem = CrawlingItem
    product_urls = cItem.getProdUrls(query, max_pages)

    df = pd.DataFrame()
    for url in product_urls:
        df = pd.concat([df, cItem.getProdInfo(url, query_t)], ignore_index=True) # 아이템 정보를 수집 후 기존 정보와 병합
        
        pNum = df.iloc[-1]['상품번호']
        nReview = int(df.iloc[-1]['nReview'])
        cItem.getProdReview(pNum, nReview)
    df.fillna(method='ffill', inplace=True)
    df.to_csv(f'itemData/{query_t}.csv', encoding='utf-8')
    print("수집 완료!")
