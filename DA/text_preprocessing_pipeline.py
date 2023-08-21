#사용법 : python text_preprocessing_pipeline.py input.tsv
#결과가 input 파일 이름_preprocessed.tsv 형식으로 저장됩니다.

import unicodedata
import xml.etree.ElementTree as ET
import pandas as pd
from hanspell import spell_checker
import re
import os
import sys
import argparse
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

def normalize_unicode(text):
    return unicodedata.normalize('NFKC', text)

def correct_spelling(text):
    try:
        spelled_sent = spell_checker.check(text)
        return spelled_sent.checked
    except Exception  as e:
        print("text", text)
        print("Error:", e)
        return text

def apply_regex(text): 
    text = re.sub(r'[^ 가-힣a-zA-Z\(\):]','',text)
    text = re.sub(r'[a-zA-Z]{1,2}', '', text)
    text = re.sub(r':\s?[\)D]|:\s?\(', '', text)
    return text

class NormalizeUnicodeTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        print("Normalizing Unicode")
        return X.apply(normalize_unicode)

class CorrectSpellingTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        print("Correcting Spelling")
        return X.apply(correct_spelling)

class ApplyRegexTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        print("Applying Regex")
        return X.apply(apply_regex)

def preprocess_file(input_filename, output_filename):
    df = pd.read_csv(input_filename, sep='\t')
    print("{}의 리뷰를 전처리 중입니다...".format(input_filename))
    print("리뷰 개수 : {}".format(len(df['review'])))
    
    preprocessing_pipeline = Pipeline([
        ('normalize_unicode', NormalizeUnicodeTransformer()),
        ('apply_regex', ApplyRegexTransformer()),
        ('correct_spelling', CorrectSpellingTransformer())
    ])

    df_preprocessed = preprocessing_pipeline.fit_transform(df['review'])
    df['review'] = df_preprocessed
    df.to_csv(output_filename, sep='\t', index=False)
    print("저장이 완료되었습니다.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="텍스트 데이터 전처리(띄어쓰기, 불필요언어 제거 등)")
    parser.add_argument("input_file", help="전처리할 파일명을 입력하세요.")
    
    args = parser.parse_args()
    
    input_filename = args.input_file
    base_filename, extension = os.path.splitext(input_filename)
    output_filename = base_filename + '_preprocessed' + extension
    
    preprocess_file(input_filename, output_filename)