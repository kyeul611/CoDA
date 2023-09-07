'''
aws s3에 
'''

import boto3
import os

# AWS S3 버킷 이름과 파일 이름 설정
bucket_name = 'sorrykim-s3'

# 로컬 디렉토리 경로 설정
file_blog = './blog'
file_DA = './DA'
file_itemData = './itemData'


# Boto3 클라이언트 생성
s3 = boto3.client('s3')


def uploadFile(file_name):
    # 로컬 디렉토리 내의 모든 파일 및 폴더 업로드
    for root, dirs, files in os.walk(file_name):
        for file in files:
            file_path = os.path.join(root, file)
            s3_key = os.path.relpath(file_path, file_name).replace('\\', '/')
            # 파일을 S3 버킷에 업로드
            s3.upload_file(file_path, bucket_name, s3_key)

            print(f'{file_path}가 {bucket_name} 버킷에 성공적으로 업로드되었습니다.')


uploadFile(file_blog)
uploadFile(file_DA)
uploadFile(file_itemData)
