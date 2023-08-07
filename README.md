# 네이버 스토어에서 아이템 정보와 리뷰를 수집하는 크롤링 프로그램

### 주의사항
실행 환경의 인터넷 속도에 영향을 받는다. 
selenium 코드가 실행되고 페이지 로드까지 정해진 시간을 대기하는데, 인터넷 속도가 느린 곳이라면 기다리는 시간보다 로딩 시간이 오래 걸릴 수 있다. 
이런 상황에서는 해당 페이지의 데이터를 정상적으로 수집 하지 못할 가능성이 있다. 


## 설치
```
> pip install -r requirements.txt
```

## 실행
```
> python run.py --query [str] --max_pages [int]
```

### 예시
네이버 쇼핑몰에서 '애견 간식' 키워드로 검색하여 나오는 첫번째 페이지의 데이터를 수집하고 싶다면 아래 명령어를 입력하면 된다. 띄어쓰기는 "언더바(_)"로 표기하자. 검색시엔 space로 바뀌어서 적용된다.
```
> python run.py --query 애견_간식 --max_pages 1
```


## Author

{  
&emsp;Infra:  
&emsp;[  
&emsp;&emsp;"kyul611":"gyul611@gmail.com",  
&emsp;&emsp;"":"",  
&emsp;],  
&emsp;Data_Analysis :  
&emsp;[  
&emsp;&emsp;"":"",  
&emsp;&emsp;"":""  
&emsp;]  
}