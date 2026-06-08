import pandas as pd
import FinanceDataReader as fdr
import matplotlib.pyplot as plt

df = fdr.DataReader('000660', '2026-01-01', '2026-06-09')

df['MA5'] = df['Close'].rolling(5).mean()
df['MA20'] = df['Close'].rolling(20).mean()

# 매수/매도 신호
df['Signal'] = 0
df.loc[df['MA5'] > df['MA20'], 'Signal'] = 1   # 매수
df.loc[df['MA5'] < df['MA20'], 'Signal'] = -1  # 매도

# 신호 변화 시점
df['Position'] = df['Signal'].diff()

# 차트
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Close'], label='종가', alpha=0.7)
plt.plot(df.index, df['MA5'], label='5일선')
plt.plot(df.index, df['MA20'], label='20일선')

# 매수 시점 표시
plt.scatter(df[df['Position'] == 2].index, 
            df[df['Position'] == 2]['Close'], 
            marker='^', color='red', s=100, label='매수')

# 매도 시점 표시
plt.scatter(df[df['Position'] == -2].index, 
            df[df['Position'] == -2]['Close'], 
            marker='v', color='blue', s=100, label='매도')

plt.title('SK하이닉스 골든크로스 전략')
plt.legend()
plt.show()