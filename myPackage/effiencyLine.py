import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Investar import Analyzer

mk = Analyzer.MarketDB()
stocks=['삼성전자', 'NAVER', '현대자동차', 'SK하이닉스']
df = pd.DataFrame()
for s in stocks:
    df[s] = mk.get_daily_price(s, '2016-01-04', '2018-04-27')['close']

# 수익률 및 리스크
daily_ret = df.pct_change()
annual_ret = daily_ret.mean() * 252
daily_cov = daily_ret.cov()
annual_cov = daily_cov*252

print(daily_ret)
print(annual_ret)
print(daily_cov)
print(annual_cov)

# 포트폴리오 담을 틀
port_ret = []
port_risk = []
port_weights = []
sharpe_ratio = []

for _ in range(20000):
    # 1. 포트폴리오 구성비 추출
    weights = np.random.random(len(stocks))
    weights = weights / np.sum(weights)

    # 2. 내적을 통한 포트폴리오 연간 수익률 추출
    returns = np.dot(weights, annual_ret)

    # 3. 포트폴리오의 연간 리스크 추출
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))

    port_ret.append(returns)
    port_risk.append(risk)
    port_weights.append(weights)
    sharpe_ratio.append(returns/risk) # 샤프지수

portfolio = {'Returns': port_ret, 'Risk':port_risk, 'Sharpe':sharpe_ratio}
# Returns Risk '삼성전자', 'NAVER', '현대자동차', 'SK하이닉스' 이렇게 만들고 싶다.
for i, s in enumerate(stocks):
    portfolio[s] = [weight[i] for weight in port_weights]
df = pd.DataFrame(portfolio)

print(df)

max_sharpe = df.loc[df['Sharpe']==df['Sharpe'].max()]
print(max_sharpe)
min_risk = df.loc[df['Risk']==df['Risk'].min()]
print(min_risk)

# 몬테카를로 시뮬레이션
df.plot.scatter(x='Risk', y='Returns', c='Sharpe', cmap='viridis', edgecolors='k', figsize=(10,7), grid=True)
plt.scatter(x=max_sharpe['Risk'], y=max_sharpe['Returns'], c='r', marker='*', s=300)
plt.scatter(x=min_risk['Risk'], y=min_risk['Returns'], c='r', marker='X', s=200)
plt.title('Efficienct Frontier')
plt.xlabel('Risk')
plt.ylabel('Expected Returns')
plt.show()

