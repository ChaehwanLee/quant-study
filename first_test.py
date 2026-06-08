import pandas as pd
import FinanceDataReader as fdr
import matplotlib.pyplot as plt

df = fdr.DataReader('000660', '2026-01-01', '2026-06-09')

# 이동평균선
df['MA5'] = df['Close'].rolling(5).mean()
df['MA20'] = df['Close'].rolling(20).mean()

# 차트
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Close'], label='종가')
plt.plot(df.index, df['MA5'], label='5일 이동평균')
plt.plot(df.index, df['MA20'], label='20일 이동평균')
plt.title('SK하이닉스 주가')
plt.legend()
plt.show()