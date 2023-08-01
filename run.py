from crawler import CrawlingItem

import pandas as pd

if __name__=='__main__':

    query = '애견 장난감'
    max_pages = 1

    query = query.replace(' ', '%20') # 띄어쓰기 문자열 치환

    cItem = CrawlingItem
    # product_urls = cItem.getProdUrls(query, max_pages)


    product_urls = ['https://smartstore.naver.com/petagon/products/2199261531?NaPm=ct%3Dlkrxplfs%7Cci%3D3bca062be38fa862a52a85df98d504c072d49d19%7Ctr%3Dslsl%7Csn%3D441903%7Chk%3De1bf006b15c1e12b4a3dcc47e6ecd9a827862622']

    df = pd.DataFrame()
    for url in product_urls:
        df = pd.concat([df, cItem.getProdInfo(url)], ignore_index=True)
        cItem.getProdReview(df['상품번호'])
        print(df)
