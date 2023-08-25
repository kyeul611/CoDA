#사용법 : python combine_data.py 폴더명
#결과가 폴더명_combined 안에 저장됩니다.

import os
import pandas as pd
import argparse

def combine(folder_path,output_folder):
    print("{} 폴더의 파일들을 병합합니다.".format(folder_path))
    tsv_files = [file for file in os.listdir(folder_path) if file.endswith('.tsv')]
    combined_data = pd.concat([pd.read_csv(os.path.join(folder_path, file), sep='\t') for file in tsv_files], ignore_index=True)
    combined_data.to_csv(os.path.join(output_folder, folder_path+'.tsv'), sep='\t', index=False)
    print("저장이 완료되었습니다.")

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="데이터가 들어있는 파일들을 하나로 병합")
    parser.add_argument("input_folder", help="병합할 파일들이 있는 폴더명을 입력하세요.")
    
    args = parser.parse_args()
    
    folder_name = args.input_folder
    output_folder = folder_name+"_combined"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    combine(folder_name,output_folder)

