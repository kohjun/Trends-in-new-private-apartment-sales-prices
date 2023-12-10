import csv
import pandas as pd
import matplotlib.pyplot as plt

# RegionData 클래스는 파일을 불러 키,값으로 구성된 딕셔너리 형태로 '지역명', '연도', '월', '분양가격'으로 이루어짐
class RegionData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data_list = self._load_data()

    def _load_data(self):
        result_list = []

        with open(self.file_path, newline='', encoding='utf-8-sig') as csvfile:
            csv_reader = csv.reader(csvfile)
            
            # 첫 번째 행을 키로 사용
            keys = next(csv_reader)
            
            for row in csv_reader:
                if row[1]=='모든면적' :
                    # 각 행의 값을 키와 묶어 딕셔너리로 변환
                    row_dict = dict(zip(keys, row))
                    
                    # 규모구분 열을 제외하고 데이터 추가
                    row_dict.pop('규모구분', None)
                    
                    result_list.append(row_dict)

        return result_list
    

    # get_data_by_region 함수는 지역을 매개변수로 주어서 해당 지역의 데이터만을 추출함.
    def get_data_by_region(self, region):
        return [data for data in self.data_list if data.get('지역명') == region]

    def plot_graph(selected_region):
        # 모든 지역의 데이터를 저장
        regionData = RegionData('신규 민간아파트 분양가격.csv')
        # 선택된 지역만의 데이터를 저장
        selected_region_data = regionData.get_data_by_region(selected_region)
        x_values=[]
        y_values=[]

        # 데이터프레임으로 변환
        df = pd.DataFrame(selected_region_data)

        # 분양가격(제곱미터) 컬럼을 숫자로 변환
        df['분양가격(제곱미터)'] = pd.to_numeric(df['분양가격(제곱미터)'], errors='coerce')

        # 연도별 평균 분양가격 계산
        df_grouped = df.groupby('연도')['분양가격(제곱미터)'].mean().reset_index()

        # 시각화
        plt.figure(figsize=(10, 6))
        plt.plot(df_grouped['연도'], df_grouped['분양가격(제곱미터)'], marker='o', linestyle='-', label='Selected Region')
        plt.title('Trends in new private apartment sales prices')
        plt.xlabel('Date')
        plt.ylabel('Price ')
        plt.legend()
        plt.grid(True)
        plt.show()
