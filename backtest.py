import pandas as pd
import FinanceDataReader as fdr

df = fdr.DataReader('000660', '2026-01-01', '2026-06-09')

df['MA5'] = df['Close'].rolling(5).mean()
df['MA20'] = df['Close'].rolling(20).mean()

df['Signal'] = 0
df.loc[df['MA5'] > df['MA20'], 'Signal'] = 1
df.loc[df['MA5'] < df['MA20'], 'Signal'] = -1
df['Position'] = df['Signal'].diff()

# 초기 자본 1000만원
capital = 10000000
shares = 0
portfolio = []

for i, row in df.iterrows():
    if row['Position'] == 2:  # 매수
        shares = capital // row['Close']
        capital -= shares * row['Close']
    elif row['Position'] == -2:  # 매도
        capital += shares * row['Close']
        shares = 0
    
    total = capital + shares * row['Close']
    portfolio.append(total)

df['Portfolio'] = portfolio

print(f"시작 자본: 10,000,000원")
print(f"최종 자산: {int(df['Portfolio'].iloc[-1]):,}원")
print(f"수익률: {(df['Portfolio'].iloc[-1] / 10000000 - 1) * 100:.1f}%")

# Buy & Hold 비교
buy_hold_shares = 10000000 // df['Close'].iloc[0]
buy_hold_final = buy_hold_shares * df['Close'].iloc[-1]
buy_hold_return = (buy_hold_final / 10000000 - 1) * 100

print(f"\n=== Buy & Hold 비교 ===")
print(f"Buy & Hold 최종 자산: {int(buy_hold_final):,}원")
print(f"Buy & Hold 수익률: {buy_hold_return:.1f}%")
print(f"\n골든크로스 전략이 Buy & Hold보다 {(df['Portfolio'].iloc[-1] - buy_hold_final) / 10000000 * 100:.1f}% 차이")