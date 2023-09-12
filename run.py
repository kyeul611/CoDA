'''
리눅스에서 테스트를 진행해야함.
리뷰 데이터의 경우 1000페이지 이후 데이터가 없음.
'''
from crawler import CrawlingItem
from crawler_blog import CrawlingBlogItem
import multiprocessing
import pandas as pd
import os
import argparse
import json
import time
import multiprocessing


def crawling(query, max_pages):

    cItem = CrawlingItem
    product_urls = cItem.getProdUrls(query, max_pages)

    # query에 해당하는 데이터가 있으면 불러온다.
    if os.path.exists(f'itemData/{query}.csv'):
        df = pd.read_csv(f'itemData/{query}.csv')
        # 여기에 중복 url을 피하도록 product_url 리스트를 수정하자
        exists_items = df['상품번호'].to_list()
    else:
        df = pd.DataFrame()
        exists_items = []

    # 리뷰 데이터가 있으면 목록을 가져온다.
    if os.path.exists(f'reviews/{query}'):
        exists_review = [int(file.split('.')[0])
                         for file in os.listdir(f'reviews/{query}')]

    # 정보와 리뷰 수집
    for i, url in enumerate(product_urls):
        print(f"[{i+1}/{len(product_urls)}] ", end="")

        # 아이템 정보 수집
        item_info = cItem.getProdInfo(url, query)
        try:
            pNum = int(item_info.iloc[-1]['상품번호'])
        except AttributeError:
            continue

        if pNum not in exists_items:
            # 수집한 데이터를 저장함.
            # 아이템 정보를 수집 후 기존 정보와 병합
            df = pd.concat([df, item_info], ignore_index=True)
            df.fillna(method='ffill', inplace=True)
            df.drop_duplicates(inplace=True)
            # 데이터를 덮어씀. 지속적으로 IO가 일어나기 때문에 성능에 영향을 끼칠 수 있지만, column이 통일되지 않은 상황에서 데이터를 지속적으로 저장하기 위한 차선책.
            df.to_csv(f'itemData/{query}.csv', encoding='utf-8', mode='w')

        # 이미 수집한 리뷰라면 건너 뛴다.
        if pNum not in exists_review:
            # 리뷰 데이터 수집
            nReview = int(df.iloc[-1]['nReview'])
            cItem.getProdReview(pNum, query, nReview, url)  # 리뷰 수집
        else:
            print("    >> 이미 있는 데이터이므로 다음으로 넘어갑니다. ")

    print("수집 완료!")


def crawling_blog(query, max_pages):

    bItem = CrawlingBlogItem
    blog_urls = bItem.getBlogUrls(query, max_pages)

    # 정보와 리뷰 수집
    for i, url in enumerate(blog_urls):
        print(f"[{i+1}/{len(blog_urls)}] ", end="")

        # 아이템 정보 수집
        item_info = bItem.getBlogReviews(url)

        with open(f'blog/{query}_blog_review_{i}.json', 'w', encoding='utf-8') as f:
            json.dump(item_info, f, indent='\t', ensure_ascii=False)

    print("수집 완료!")


if __name__ == '__main__':
    # arguement를 받음
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', required=True,
                        help='수집을 원하는 키워드를 입력. 띄어쓰기 사이에는 \\를 넣어줘야함. ex) 패션\\ 안경')
    parser.add_argument('--max_pages', default=1, type=int,
                        help='네이버 쇼핑에서 몇 페이지를 수집할 지 결정. 기본값은 1. 첫페이지만 수집함.')
    args = parser.parse_args()

    query = args.query
    max_pages = args.max_pages

    # 필요한 폴더 생성
    if not os.path.exists(f'reviews'):
        os.mkdir('reviews')
    if not os.path.exists(f'reviews/{query}'):
        os.mkdir(f'reviews/{query}')
    if not os.path.exists('itemData'):
        os.mkdir('itemData')
    if not os.path.exists('logs'):
        os.mkdir('logs')
    if not os.path.exists('blog'):
        os.mkdir('blog')

    query_url = query.replace('_', '%20')  # url용 띄어쓰기 문자열 치환

    # 멀티프로세스 구현
    process1 = multiprocessing.Process(target=crawling, args=(query, max_pages))
    process2 = multiprocessing.Process(target=crawling_blog, args=(query,max_pages))

    # 프로세스 시작
    process1.start()
    process2.start()
    
    # 프로세스 종료 대기
    process1.join()
    process2.join()