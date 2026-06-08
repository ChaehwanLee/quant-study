import pandas as pd
import FinanceDataReader as fdr

df = fdr.DataReader('000660', '2026-01-01', '2026-06-09')
print(df)