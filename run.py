from crawler import CrawlingItem

import pandas as pd

if __name__=='__main__':

    query = '애견 장난감'
    max_pages = 1

    query = query.replace(' ', '%20') # 띄어쓰기 문자열 치환

    cItem = CrawlingItem
    # product_urls = cItem.getProdUrls(query, max_pages)


    product_urls = ['https://cr.shopping.naver.com/adcr.nhn?x=jn6s0jvCj5%2F71pAKK9duxv%2F%2F%2Fw%3D%3DsLAfTDUyBM4fRj7nV%2BabDocOD1cSkXBUU%2FdjBE52T4zvGuCxdcFRAgmqqBnSnKr1XSaQnUOMVdtOE4MAr4wfgRxoi55GgTPXEY3oQoumRpoTb3Ss7%2Fx%2F8BZZzWDOhBTTK7uPXG6vCTAeQsyqShz30n%2FCrzVtOxK%2BDNFfhXp70O%2BvG66W39bYVR7J8ygpm2%2FKtN2BD0qbQ%2Bjh7a9pYVcBYqC528eEoKXB%2FWiwLXsd8mw9JT%2FywKUM2GIochP90NJw4pOr9sPYwajBkeE07IGGkJ5SCPsmGKllbt0kl8XIxCXSlzxG%2FA5xt5I86VWTPweBoxfp6gdOZQqP%2FA352xIvPOsAFBQNh3Vn2Iq3SHPUkG5bZ29buHDI5yUoBiYxyFJyXpseS0vbdJmdBrO74r7h%2F5uRYl70AGRMfxZlBEFjeSPYpf6Kmi4mLdsx6FuwiQy%2FleUplI6dWYYKEgxYcnygui3KAQEeTDHJZBjhT0BC3gzUGsU34sl6BdQ7HZQ6AKkvZm3qcFokC5kwWu3lMecFSgaJDoq7rFjgmjoUPz9pX5ctxxlLPUS54NpKB%2F5mOehLRwL20E1XMgQf78TXa11dnpnG3edWmELTGG4Xmj7DoZ5nuhanrDapWV%2FfJWEJUGFG3V3OdHgSE8LoEjTx9zpNPbFaRsOtQUnaEEbxBoHxZXOc%3D&nvMid=80009113836&catId=50006674']

    df = pd.DataFrame()
    for url in product_urls:
    #    df = pd.concat(df, cItem.getProdInfo(url))
    #    print(df)

        cItem.getProdInfo(url)