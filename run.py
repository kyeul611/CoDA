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
    if not os.path.exists('logs'):
        os.mkdir('logs')

    query = '애견 장난감'
    max_pages = 1

    query_t = query.replace(' ', '_') # 파일 저장용 문자열 치환
    query = query.replace(' ', '%20') # 띄어쓰기 문자열 치환

    cItem = CrawlingItem
    product_urls = cItem.getProdUrls(query, max_pages)

    df = pd.DataFrame()
    for url in product_urls:
        print(f"now=>   {url}\n")
        df = pd.concat([df, cItem.getProdInfo(url, query_t)], ignore_index=True)
        print("nReview", df.iloc[-1]['nReview'])
        # cItem.getProdReview(df.iloc[-1, 4])
    df.fillna(None, inplace=True)
    df.to_csv(f'itemData/{query_t}.csv', encoding='utf-8')
    print("수집 완료!")
