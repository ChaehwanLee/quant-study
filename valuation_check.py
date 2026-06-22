"""
메모리 반도체 밸류에이션 체크
- 현재 PER(후행/선행), PBR 스냅샷
- 5년 주가 밴드 내 현재 위치(백분위) → '역사적으로 어디쯤'인지 직관
- (옵션) 분기 자본총계로 PBR 추세 근사

* yfinance .info는 가끔 값이 비거나 지연될 수 있음 → 비면 네이버금융/FnGuide로 교차 확인.
* '진짜' PBR 밴드(과거~현재)는 BPS 시계열이 필요해서 yfinance만으론 한계가 있음.
  아래 옵션 블록은 분기 자본총계 기반 근사치 — 정밀치는 FnGuide(comp.fnguide.com) 권장.
"""

import yfinance as yf
import pandas as pd

TICKERS = {"삼성전자": "005930.KS", "SK하이닉스": "000660.KS"}


def snapshot(name: str, ticker: str) -> None:
    t = yf.Ticker(ticker)
    info = t.info

    price   = info.get("currentPrice") or info.get("regularMarketPrice")
    per     = info.get("trailingPE")
    fwd_per = info.get("forwardPE")
    pbr     = info.get("priceToBook")

    print(f"\n=== {name} ({ticker}) ===")
    print(f"현재가      : {price:,}" if price else "현재가      : N/A")
    print(f"PER (후행)  : {per:.2f}"     if per     else "PER (후행)  : N/A")
    print(f"PER (선행)  : {fwd_per:.2f}" if fwd_per else "PER (선행)  : N/A")
    print(f"PBR         : {pbr:.2f}"     if pbr     else "PBR         : N/A")

    # 5년 주가 밴드 내 위치 → 절대값보다 '역사적 위치'가 핵심
    hist = t.history(period="5y")["Close"].dropna()
    if len(hist):
        cur = hist.iloc[-1]
        pct = (hist < cur).mean() * 100  # 0=5년 최저권, 100=5년 최고권
        print(f"5년 주가 밴드 위치 : {pct:.0f} 백분위  "
              f"(최저 {hist.min():,.0f} / 현재 {cur:,.0f} / 최고 {hist.max():,.0f})")
        if pct >= 80:
            print("  → 역사적 상단권. '싸다'고 볼 근거 약함.")
        elif pct <= 20:
            print("  → 역사적 하단권.")
        else:
            print("  → 중간 구간.")


def pbr_trend_approx(name: str, ticker: str) -> None:
    """분기 자본총계(지배주주지분) / 시총 → PBR 추세 근사. 정밀치는 FnGuide 확인."""
    t = yf.Ticker(ticker)
    try:
        bs = t.quarterly_balance_sheet
        equity = bs.loc["Stockholders Equity"].dropna()
        shares = t.info.get("sharesOutstanding")
        price = t.info.get("currentPrice") or t.info.get("regularMarketPrice")
        if shares and price and len(equity):
            bps_latest = equity.iloc[0] / shares
            print(f"[{name}] 최근 분기 BPS 근사: {bps_latest:,.0f}  "
                  f"→ 근사 PBR {price / bps_latest:.2f}")
    except Exception as e:
        print(f"[{name}] PBR 근사 실패({e}) — FnGuide로 확인 권장")


if __name__ == "__main__":
    for name, tk in TICKERS.items():
        snapshot(name, tk)
    print("\n--- PBR 추세 근사 (참고용) ---")
    for name, tk in TICKERS.items():
        pbr_trend_approx(name, tk)

    print("\n[해석 가이드]")
    print("1) 메모리는 PER 낮다고 싸다 X — 이익(EPS) 정점이면 PER은 원래 낮게 찍힌다.")
    print("2) PBR이 과거 5~10년 밴드 '상단 돌파' 상태면 전통 기준 역사적 고평가.")
    print("3) 그 돌파의 정당성 = HBM 장기계약·공급부족이 구조적이냐에 달림")
    print("   → 네 셀 트리거(NVDA 가이던스 / 빅테크 Capex)가 그대로 판단 기준.")