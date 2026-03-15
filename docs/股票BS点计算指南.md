# 股票BS点（买卖点）计算指南

## 什么是BS点？

**B点** (Buy) - 买入点  
**S点** (Sell) - 卖出点

BS点是技术分析中用于判断股票买卖时机的关键指标。

---

## 一、基础技术指标

### 1. 移动平均线 (MA)

**计算公式：**
```
MA(n) = (P1 + P2 + ... + Pn) / n
```
- P: 收盘价
- n: 周期（5日、10日、20日、60日）

**BS点判断：**
- **金叉**（短期MA上穿长期MA）→ B点
- **死叉**（短期MA下穿长期MA）→ S点

**示例：**
```
5日均线上穿20日均线 = 买入信号
5日均线下穿20日均线 = 卖出信号
```

---

### 2. MACD指标

**计算公式：**
```
EMA(12) = 前一日EMA(12) × 11/13 + 今日收盘价 × 2/13
EMA(26) = 前一日EMA(26) × 25/27 + 今日收盘价 × 2/27
DIF = EMA(12) - EMA(26)
DEA = 前一日DEA × 8/10 + 今日DIF × 2/10
MACD = (DIF - DEA) × 2
```

**BS点判断：**
- **DIF上穿DEA**（金叉）+ MACD柱状图由负转正 → B点
- **DIF下穿DEA**（死叉）+ MACD柱状图由正转负 → S点

---

### 3. RSI相对强弱指标

**计算公式：**
```
RSI = 100 - (100 / (1 + RS))
RS = n日内上涨平均值 / n日内下跌平均值
```

**BS点判断：**
- **RSI < 30**（超卖）→ B点（买入机会）
- **RSI > 70**（超买）→ S点（卖出机会）
- **RSI从30以下向上突破** → B点
- **RSI从70以上向下突破** → S点

---

### 4. KDJ随机指标

**计算公式：**
```
RSV = (收盘价 - n日内最低价) / (n日内最高价 - n日内最低价) × 100
K = 2/3 × 前一日K + 1/3 × 当日RSV
D = 2/3 × 前一日D + 1/3 × 当日K
J = 3K - 2D
```

**BS点判断：**
- **K上穿D**（金叉）+ J < 20 → B点
- **K下穿D**（死叉）+ J > 80 → S点

---

## 二、进阶BS点计算

### 1. 布林带 (Bollinger Bands)

**计算公式：**
```
中轨 = MA(20)
上轨 = MA(20) + 2 × 标准差(20)
下轨 = MA(20) - 2 × 标准差(20)
```

**BS点判断：**
- 股价触及**下轨**且反弹 → B点
- 股价触及**上轨**且回落 → S点
- 股价**突破上轨** → 强势B点
- 股价**跌破下轨** → 弱势S点

---

### 2. 成交量配合

**量价关系BS点：**

| 情况 | 信号 |
|------|------|
| 价格上涨 + 成交量放大 | 确认B点 |
| 价格上涨 + 成交量萎缩 | 假突破，警惕S点 |
| 价格下跌 + 成交量放大 | 确认S点 |
| 价格下跌 + 成交量萎缩 | 可能是洗盘，观察B点 |

---

### 3. 支撑阻力位

**计算方法：**
```
支撑位 = 近期低点 / 前期低点
阻力位 = 近期高点 / 前期高点
```

**BS点判断：**
- 股价**回调至支撑位**且企稳 → B点
- 股价**反弹至阻力位**且受阻 → S点
- **突破阻力位** → 追涨B点
- **跌破支撑位** → 止损S点

---

## 三、综合BS点评分系统

### 多指标共振评分

| 指标 | 买入信号 | 卖出信号 | 权重 |
|------|----------|----------|------|
| MA金叉/死叉 | +20 | -20 | 20% |
| MACD金叉/死叉 | +20 | -20 | 20% |
| RSI超卖/超买 | +15 | -15 | 15% |
| KDJ金叉/死叉 | +15 | -15 | 15% |
| 布林带位置 | +15 | -15 | 15% |
| 成交量配合 | +15 | -15 | 15% |

**评分标准：**
- **+60分以上** → 强烈B点（买入）
- **+30~60分** → 一般B点（轻仓买入）
- **-30~+30分** → 观望
- **-30~-60分** → 一般S点（减仓）
- **-60分以下** → 强烈S点（卖出）

---

## 四、实战示例

### 示例：计算某股票的BS点

**假设数据：**
- 当前价：25.80
- 5日均线：25.50
- 20日均线：26.00
- MACD DIF：-0.15
- MACD DEA：-0.20
- RSI：35
- 成交量：较昨日放大30%

**分析：**
1. MA：5日 < 20日，无金叉 → 0分
2. MACD：DIF > DEA，金叉 → +20分
3. RSI：35，接近超卖区 → +10分
4. 成交量：放大，配合上涨 → +15分

**总分：45分** → 一般B点，可轻仓关注

---

## 五、注意事项

### ⚠️ 风险控制
1. **止损位**：买入价下方5-8%
2. **仓位管理**：单只股票不超过总资金20%
3. **分批建仓**：不要一次性满仓

### 📊 适用场景
- **趋势行情**：MA、MACD效果好
- **震荡行情**：RSI、KDJ、布林带效果好
- **突破行情**：成交量+阻力位突破

### 🚫 不适用情况
- 个股突发重大利空/利好
- 市场整体暴跌/暴涨
- 流动性极差的股票

---

## 六、Python计算示例

```python
import pandas as pd
import numpy as np

def calculate_ma(prices, n):
    """计算移动平均线"""
    return prices.rolling(window=n).mean()

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """计算MACD"""
    ema_fast = prices.ewm(span=fast).mean()
    ema_slow = prices.ewm(span=slow).mean()
    dif = ema_fast - ema_slow
    dea = dif.ewm(span=signal).mean()
    macd = (dif - dea) * 2
    return dif, dea, macd

def calculate_rsi(prices, n=14):
    """计算RSI"""
    deltas = prices.diff()
    gain = deltas.where(deltas > 0, 0).rolling(window=n).mean()
    loss = (-deltas.where(deltas < 0, 0)).rolling(window=n).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_bollinger(prices, n=20, k=2):
    """计算布林带"""
    ma = prices.rolling(window=n).mean()
    std = prices.rolling(window=n).std()
    upper = ma + k * std
    lower = ma - k * std
    return upper, ma, lower

# 综合BS点判断
def get_bs_signal(df):
    """
    df需要包含: close, volume
    返回: 'B'买入, 'S'卖出, 'H'持有
    """
    score = 0
    
    # MA金叉
    if df['MA5'].iloc[-1] > df['MA20'].iloc[-1] and \
       df['MA5'].iloc[-2] <= df['MA20'].iloc[-2]:
        score += 20
    
    # MACD金叉
    if df['DIF'].iloc[-1] > df['DEA'].iloc[-1] and \
       df['DIF'].iloc[-2] <= df['DEA'].iloc[-2]:
        score += 20
    
    # RSI超卖反弹
    if df['RSI'].iloc[-1] > 30 and df['RSI'].iloc[-2] <= 30:
        score += 15
    
    # 成交量放大
    if df['volume'].iloc[-1] > df['volume'].iloc[-2] * 1.2:
        score += 15
    
    if score >= 60:
        return 'B', score
    elif score <= -60:
        return 'S', score
    else:
        return 'H', score
```

---

## 七、推荐学习资源

1. **《日本蜡烛图技术》** - 史蒂夫·尼森
2. **《技术分析》** - 马丁·普林格
3. **TradingView** - 在线图表分析工具
4. **同花顺/东方财富** - 国内技术指标平台

---

*此文档由 AnalyzeMaster 创建*
*最后更新: 2026-03-15*
