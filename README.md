민간 아파트 서비스 플랫폼 
## '토아'
### 토아는 Trend Of Apartment의 약자 TOA로 공공데이터를 기반으로 한 민간 아파트 서비스 플랫폼입니다.

### 지역 가격 추이 그래프 시각화
- 국가 공공 신규 민간 아파트 데이터를 활용하여 지역의 민간 아파트 가격 추이를 그래프화

![image](https://github.com/kohjun/Trends-in-new-private-apartment-sales-prices/assets/82298792/f18d1b86-f499-4589-83c9-10ec9bc1dc0d)

### 지역 가격 예측 산정
- 해당 지역의 특정 연도와 통화량 증가율, GDP(경제성장률)을 통해 민간 아파트 분양가격을 예측
![image](https://github.com/kohjun/Trends-in-new-private-apartment-sales-prices/assets/82298792/b98d860a-77d4-48ff-8c80-15eb383a7f9a)

### 지역 가격 비교
- 두 지역의 지역을 비교하고 평균가격을 표시
![image](https://github.com/kohjun/Trends-in-new-private-apartment-sales-prices/assets/82298792/1601d2e8-c35b-4d49-bf40-2f3c4e3bf9a9)

<hr>

- 파이썬 Tkinter를 활용하여 만든  **객체 지향적 **  프로그램
- Main GUI를 동작하여 사용
- DataLoad.py를 통해 csv파일을 읽어 pandas를 통해 데이터를 정리
- RegionButton.py에는 선택된 지역의 데이터를 읽어 matplotlib를 통해 데이터를 시각화
- MachingLearning.py와 Calulate.py는 선택된 지역의 예측 연도 통화량 증가율, 경제성장률을 입력하여 랜덤포레스트 분류기를 통한 머신러닝 훈련과 예측된 분양가격(제곱미터)으로 아파트 가격을 예상


데이터 출처 : 통계청(https://kostat.go.kr/ansk/) , 공공 데이터 포털(https://www.data.go.kr/)


### 음원 크레딧
이 영상은 뮤팟에서 제공한 음원 소스를 사용했습니다.
Today's eating show- Download: mewc.at/songs/10026

🎫 추천인 코드: mewc.at/ref/4ktz
위의 URL을 통해 구독하시면 2개월 추가 혜택!
저와 함께 뮤팟 혜택을 받아요~🎁
