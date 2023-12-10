import pandas as pd
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import DataLoad

class MachineLearn:
    def __init__(self):
        self.model = RandomForestRegressor(random_state=42)

    def train_model(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, future_data):
        return self.model.predict(future_data)

    def evaluate_model(self, X_test, y_test):
        y_pred = self.model.predict(X_test)
        return r2_score(y_test, y_pred)

class Input_MachineLearning:
    
    # ip1 = '지역, ip2 = '예측 연도' , ip3 = '통화량 증가율', ip4 = '경제성장률'
    def __init__(self,ip1,ip2,ip3,ip4):
            
        # 본원통화 데이터 
        exchange_df = pd.read_csv('본원통화(2015~2023).csv')

        # '기간' 열을 분리하여 '연도'와 '월'로 나누기
        exchange_df[['연도', '월']] = exchange_df['기간'].str.split('-', expand=True)

        # '연도'와 '월'을 정수형으로 변환
        exchange_df['연도'] = exchange_df['연도'].astype(int)
        exchange_df['월'] = exchange_df['월'].astype(int)

        # 기존 '기간' 열 제거
        exchange_df = exchange_df.drop(columns=['기간'])

        # 신규 민간 아파트 분양가격 데이터
        dt_load = DataLoad.RegionData('신규 민간아파트 분양가격.csv')


        # gdp 연도별 딕셔너리 형태
        gdp_data = [
            {'year': 2015, '국내총생산(명목GDP)': 1658020, '경제성장률(실질GDP성장률)': 2.8},
            {'year': 2016, '국내총생산(명목GDP)': 1740779, '경제성장률(실질GDP성장률)': 2.9},
            {'year': 2017, '국내총생산(명목GDP)': 1835698, '경제성장률(실질GDP성장률)': 3.2},
            {'year': 2018, '국내총생산(명목GDP)': 1898192, '경제성장률(실질GDP성장률)': 2.9},
            {'year': 2019, '국내총생산(명목GDP)': 1924498, '경제성장률(실질GDP성장률)': 2.2},
            {'year': 2020, '국내총생산(명목GDP)': 1940726, '경제성장률(실질GDP성장률)': -0.7},
            {'year': 2021, '국내총생산(명목GDP)': 2071658, '경제성장률(실질GDP성장률)': 4.1},
            {'year': 2022, '국내총생산(명목GDP)': 2150575, '경제성장률(실질GDP성장률)': 2.6}
        ]
        # gdp 데이터프레임으로 변환
        gdp_df = pd.DataFrame(gdp_data)

        # 특정 지역 분양가격 데이터
        region_dt_load = dt_load.get_data_by_region(ip1)

        # 특정 지역의 데이터프레임으로 변환
        region_apartment_df = pd.DataFrame(region_dt_load)
        region_apartment_df['분양가격(제곱미터)'] = pd.to_numeric(region_apartment_df['분양가격(제곱미터)'], errors='coerce')
        region_apartment_df['연도'] = region_apartment_df['연도'].astype(int)
        region_apartment_df['월'] = region_apartment_df['월'].astype(int)  # Ensure '월' is int
        region_apartment_df = region_apartment_df.dropna(subset=['분양가격(제곱미터)'])

        # 본원통화 데이터와 지역 아파트 데이터 병합
        merged_df = pd.merge(region_apartment_df, exchange_df, on=['연도', '월'])
        merged_df = pd.merge(merged_df, gdp_df, left_on='연도', right_on='year')  # gdp_df를 merged_df에 추가

        # 모델에 사용할 특성 선택
        X = merged_df[['연도','증가율', '경제성장률(실질GDP성장률)']]

        # 타겟 선택
        y = merged_df['분양가격(제곱미터)']

        # 데이터를 훈련 세트와 테스트 세트로 분리
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        

        # 랜덤 포레스트 모델 초기화
        self.ml_model = MachineLearn()

        # 모델 훈련
        self.ml_model.train_model(X_train, y_train)

        self.ip2 = ip2
        self.ip3, self.ip4 = ip3, ip4
        self.X_test = X_test
        self.y_test = y_test


    def get_prediction(self):
        # 예측에 사용할 입력 데이터 준비
        future_data = pd.DataFrame({
            '연도': [self.ip2],
            '증가율': [self.ip3],
            '경제성장률(실질GDP성장률)': [self.ip4]
        })

        # 입력 연도의 지역 아파트 분양가격 예측
        predicted_price = self.ml_model.predict(future_data)

        return round(predicted_price[0])
    

    def get_evaluation(self):
        # 테스트 세트로 성능 평가
        y_pred = self.ml_model.predict(self.X_test)
        return r2_score(self.y_test, y_pred)


