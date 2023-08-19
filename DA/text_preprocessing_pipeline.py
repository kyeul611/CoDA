#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/Tiabet/Project_Market/blob/master/text_preprocessing_pipeline.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>


#사용법 : python text_preprocessing_pipeline.py input.tsv
#결과가 input 파일 이름_preprocessed.tsv 형식으로 저장됩니다.
#설치 필요 패키지 : Hanspell (네이버 맞춤법 검사기) , Scikit-learn (싸이킷런)

import unicodedata
import pandas as pd
from hanspell import spell_checker
import re
import os
import sys
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

def normalize_unicode(text):
    return unicodedata.normalize('NFKC', text)

def correct_spelling(text):
    spelled_sent = spell_checker.check(text)
    return spelled_sent.checked

def apply_regex(text): 
    text = re.sub(r'[^ 가-힣a-zA-Z\(\):]','',text)
    text = re.sub(r'[a-zA-Z]{1,2}', '', text)
    text = re.sub(r':\s?[)D]|:\s?\[', '', text)
    return text

class NormalizeUnicodeTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.apply(normalize_unicode)

class CorrectSpellingTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.apply(correct_spelling)

class ApplyRegexTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.apply(apply_regex)

def preprocess_file(input_filename, output_filename):
    df = pd.read_csv(input_filename, sep='\t')
    
    preprocessing_pipeline = Pipeline([
        ('normalize_unicode', NormalizeUnicodeTransformer()),
        ('correct_spelling', CorrectSpellingTransformer()),
        ('apply_regex', ApplyRegexTransformer()),
        ('correct_spelling_2', CorrectSpellingTransformer())
    ])

    df_preprocessed = preprocessing_pipeline.fit_transform(df['review'])
    df['review'] = df_preprocessed
    df.to_csv(output_filename, sep='\t', index=False)  

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python preprocessing_script.py input.tsv")
    else:
        input_filename = sys.argv[1]
        base_filename, extension = os.path.splitext(input_filename)
        output_filename = base_filename + '_preprocessed' + extension
        preprocess_file(input_filename, output_filename)
