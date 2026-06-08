import pandas as pd
import FinanceDataReader as fdr

# 삼성전자 주가 데이터 가져오기
df = fdr.DataReader('005930', '2024-01-01', '2024-12-31')
print(df.head())