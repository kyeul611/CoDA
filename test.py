from crawler_blog import CrawlingBlogItem

import pandas as pd
import os
import argparse

#CrawlingBlogItem.getBlogUrls("커피", 10)

url = "https://blog.naver.com/ko4791917/223188365892"


CrawlingBlogItem.getBlogReviews(url, "")