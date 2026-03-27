"""
OpenMorning 专业报告生成器
营销号风格 + 危机感 + 中英双语
结构：危机→解读→方案
"""

from datetime import datetime
from typing import Dict

def detect_question_type(question: str) -> str:
    """检测问题类型"""
    q = question.lower()
    if any(kw in q for kw in ['关系', '紧张', '战争', '冲突', '国际', '外交']):
        return 'international'
    if any(kw in q for kw in ['选举', '连任', '总统', '特朗普', '政治']):
        return 'political'
    if any(kw in q for kw in ['比特币', 'btc', '加密货币', '币圈']):
        return 'crypto'
    if any(kw in q for kw in ['趋势', '发展', '行业', '前景']):
        return 'industry'
    return 'stock'

def generate_report(prediction_data: dict) -> tuple:
    """生成中英双语报告"""
    question = prediction_data.get("question", "")
    predictions = prediction_data.get("predictions", [])
    prediction_id = prediction_data.get("id", "")
    
    question_type = detect_question_type(question)
    main_pred = predictions[0] if predictions else {}
    result = main_pred.get("result", "")
    probability = main_pred.get("probability", 0)
    
    if question_type == 'international':
        return _generate_international_report_v2(question, result, probability, prediction_id)
    elif question_type == 'crypto':
        return _generate_crypto_report_v2(question, result, probability, prediction_id)
    elif question_type == 'political':
        return _generate_political_report_v2(question, result, probability, prediction_id)
    else:
        return _generate_stock_report_v2(question, result, probability, prediction_id)

def _generate_stock_report_v2(question: str, result: str, probability: float, prediction_id: str) -> tuple:
    """A 股/股票报告 - 营销号风格"""
    
    cn = f"""
# 🌅 OpenMorning 深度报告

---

## ⚠️ 你正在错过一代人的财富机遇

**问题**：{question}

这不是危言耸听。

历史数据告诉我们：**90% 的投资者在周期起点选择观望，然后在周期顶点冲进市场。**

他们不是输给了市场，而是输给了自己的犹豫。

---

## 🔴 悲观者正在错过什么？

有人说："经济不好，股市要崩。"

有人说："现在是熊市，等明确了再进场。"

**这些人 2008 年错过了抄底，2020 年错过了科技股，现在又要错过什么？**

康波周期理论创始人尼古拉·康德拉季耶夫用 60 年的数据证明：

> **每一次经济最低迷的时候，都是财富转移的起点。**

1982 年，美国走出滞胀，道指开启 18 年牛市
2009 年，金融危机见底，美股开启 10 年长牛
**2026 年，历史正在重演。**

---

## 🔍 深度解读：为什么是现在？

### 1. 康波周期：60 年一遇的转折点

我们正处于第五轮康波周期的**回升起点**。

| 周期阶段 | 时间 | 特征 | 投资者行为 |
|---------|------|------|-----------|
| 繁荣期 | 1991-2000 | 技术革命 | 疯狂追涨 |
| 衰退期 | 2000-2008 | 泡沫破裂 | 恐慌出逃 |
| 萧条期 | 2008-2025 | 存量博弈 | 躺平放弃 |
| **回升期** | **2026-** | **新周期起点** | **？？？** |

**90% 的人会在回升期结束时才反应过来。**

### 2. 流动性拐点：央行已经行动

全球主要央行进入降息通道。

**这不是预测，这是正在发生的事实。**

历史规律：降息启动后 12-24 个月，风险资产平均涨幅超过 50%。

### 3. 技术革命：AI 正在重塑一切

这不是概念炒作。

AI、新能源、高端制造的技术突破正在加速商业化。

**每一次技术革命，都会诞生新的财富巨头。**

上一次是互联网，这一次是什么？

---

## 💡 解决方案：如何抓住这次机遇？

### 核心策略

| 步骤 | 行动 | 时间 |
|------|------|------|
| **1** | 建立认知 | 现在 |
| **2** | 分批建仓 | Q1-Q2 |
| **3** | 动态调整 | Q3-Q4 |
| **4** | 止盈离场 | 周期顶点 |

### 配置建议

- **40%** 科技创新 — 技术革命核心受益者
- **25%** 新能源 — 能源转型不可逆转
- **20%** 高端制造 — 国产替代 + 产业升级
- **15%** 现金 — 应对不确定性

### 风险控制

> **永远不要孤注一掷。**
> 
> 分批建仓，动态止盈，保留现金。

---

## 📊 核心结论

**方向**：看涨  
**区间**：{result}  
**置信度**：{int(probability * 100)}%

---

## ⏰ 最后的话

**历史不会等人。**

1982 年抓住机会的人，财富翻了 10 倍
2009 年抓住机会的人，财富翻了 5 倍
**2026 年，你会是哪一个？**

---

**报告编号**：`{prediction_id}`  
**生成时间**：{datetime.now().strftime('%Y年%m月%d日')}  
**验证日期**：2026年12月31日

---

*OpenMorning — 让预测成为科学*
"""

    en = f"""
# 🌅 OpenMorning Investment Strategy Report

---

## ⚠️ You're Missing a Once-in-a-Generation Wealth Opportunity

**Question**: {question}

This is not fear-mongering.

Historical data shows: **90% of investors choose to wait at cycle bottoms, then rush in at cycle tops.**

They didn't lose to the market. They lost to their own hesitation.

---

## 🔴 What Are Pessimists Missing?

"The economy is bad. The market will crash."

"Wait for clarity before entering."

**These people missed the 2008 bottom, missed the 2020 tech rally. What will they miss now?**

Kondratieff Wave theory proves with 60 years of data:

> **Every economic low point is the starting point of wealth transfer.**

1982: US exits stagflation, Dow begins 18-year bull market
2009: Financial crisis bottom, US stocks begin 10-year bull run
**2026: History is repeating.**

---

## 🔍 Deep Analysis: Why Now?

### 1. Kondratieff Cycle: 60-Year Turning Point

We're at the **recovery starting point** of the 5th Kondratieff Wave.

| Phase | Time | Characteristics | Investor Behavior |
|-------|------|----------------|-------------------|
| Prosperity | 1991-2000 | Tech Revolution | FOMO buying |
| Recession | 2000-2008 | Bubble Burst | Panic selling |
| Depression | 2008-2025 | Zero-sum Game | Giving up |
| **Recovery** | **2026-** | **New Cycle Start** | **???** |

**90% will only realize it at the end of recovery phase.**

### 2. Liquidity Inflection: Central Banks Are Acting

Global central banks are entering rate cut cycles.

**This is not a prediction. This is happening.**

Historical pattern: 12-24 months after rate cuts begin, risk assets average 50%+ gains.

### 3. Tech Revolution: AI is Reshaping Everything

This is not hype.

AI, new energy, advanced manufacturing breakthroughs are accelerating commercialization.

**Every tech revolution creates new wealth giants.**

Last time: Internet. This time: What?

---

## 💡 Solution: How to Seize This Opportunity?

### Core Strategy

| Step | Action | Timing |
|------|--------|--------|
| **1** | Build Awareness | Now |
| **2** | Scale In | Q1-Q2 |
| **3** | Dynamic Adjust | Q3-Q4 |
| **4** | Take Profits | Cycle Top |

### Allocation Recommendation

- **40%** Tech Innovation — Core beneficiaries
- **25%** New Energy — Irreversible transition
- **20%** Advanced Manufacturing — Domestic substitution
- **15%** Cash — Uncertainty buffer

### Risk Control

> **Never go all-in.**
> 
> Scale in, dynamic exits, keep cash reserve.

---

## 📊 Core Conclusion

**Direction**: Bullish  
**Range**: {result}  
**Confidence**: {int(probability * 100)}%

---

## ⏰ Final Words

**History waits for no one.**

Those who seized 1982: 10x wealth
Those who seized 2009: 5x wealth
**2026: Which one will you be?**

---

**Report ID**: `{prediction_id}`  
**Generated**: {datetime.now().strftime('%Y-%m-%d')}  
**Verify**: 2026-12-31

---

*OpenMorning — Making Prediction Scientific*
"""

    return cn.strip(), en.strip()

def _generate_crypto_report_v2(question: str, result: str, probability: float, prediction_id: str) -> tuple:
    """加密货币报告 - 营销号风格"""
    
    cn = f"""
# 🚀 OpenMorning 数字资产深度报告

---

## ⚠️ 大多数人正在错过数字资产时代

**问题**：{question}

这不是危言耸听。

**2010 年，比特币 0.1 美元，99% 的人说"这是骗局"**
**2015 年，比特币 300 美元，90% 的人说"太晚了"**
**2020 年，比特币 1 万美元，80% 的人说"太高了"**

**现在，他们在说什么？**

---

## 🔴 悲观者错过了什么？

"加密货币是泡沫。"

"监管会扼杀一切。"

**说这些话的人：**
- 2010 年错过了 10000 倍
- 2015 年错过了 100 倍
- 2020 年错过了 10 倍

**他们不是谨慎，他们是无知。**

---

## 🔍 深度解读：为什么是现在？

### 1. 机构资金已经入场

贝莱德、富达、高盛...

这些曾经最看不起加密货币的机构，现在都在做什么？

**他们在建仓。**

当最保守的资金都在入场时，你还在犹豫什么？

### 2. 监管框架正在成型

这不是利空，这是利好。

监管 = 合法性 = 更多资金入场

**每一次监管落地，都是价格上涨的催化剂。**

### 3. 康波周期：技术革命的起点

2026 年是康波周期回升起点。

历史证明：每一次技术革命，都会诞生新的资产类别。

1990 年代：互联网股票
2020 年代：**数字资产**

---

## 💡 解决方案：如何参与？

### 核心策略

| 步骤 | 行动 | 关键 |
|------|------|------|
| **1** | 认知升级 | 理解数字资产价值 |
| **2** | 仓位配置 | 不超过 10% |
| **3** | 定投策略 | 平摊成本 |
| **4** | 长期持有 | 穿越周期 |

### 风险控制

> **不要用救命钱投资加密货币。**
> 
> 只用你能承受损失的资金。

---

## 📊 核心结论

**方向**：看涨  
**区间**：{result}  
**置信度**：{int(probability * 100)}%

---

## ⏰ 最后的话

**数字资产时代已经到来。**

你可以选择继续质疑，也可以选择参与。

**历史不会重复，但总是押着相似的韵脚。**

---

**报告编号**：`{prediction_id}`  
**生成时间**：{datetime.now().strftime('%Y年%m月%d日')}

---

*OpenMorning — 让预测成为科学*
"""

    en = f"""
# 🚀 OpenMorning Digital Asset Report

---

## ⚠️ Most People Are Missing the Digital Asset Era

**Question**: {question}

This is not fear-mongering.

**2010: Bitcoin at $0.10, 99% said "scam"**
**2015: Bitcoin at $300, 90% said "too late"**
**2020: Bitcoin at $10K, 80% said "too high"**

**What are they saying now?**

---

## 🔴 What Are Pessimists Missing?

"Crypto is a bubble."

"Regulation will kill it."

**These people:**
- Missed 10000x in 2010
- Missed 100x in 2015
- Missed 10x in 2020

**They're not cautious. They're ignorant.**

---

## 🔍 Deep Analysis: Why Now?

### 1. Institutions Are Already In

BlackRock, Fidelity, Goldman Sachs...

The institutions that once dismissed crypto, what are they doing now?

**They're accumulating.**

When the most conservative capital is entering, what are you waiting for?

### 2. Regulatory Framework Is Forming

This is not bearish. This is bullish.

Regulation = Legitimacy = More Capital

**Every regulatory milestone is a catalyst for price appreciation.**

### 3. Kondratieff Cycle: Tech Revolution Starting Point

2026 is the recovery starting point.

History proves: Every tech revolution creates new asset classes.

1990s: Internet stocks
2020s: **Digital Assets**

---

## 💡 Solution: How to Participate?

### Core Strategy

| Step | Action | Key |
|------|--------|-----|
| **1** | Cognitive Upgrade | Understand digital asset value |
| **2** | Position Sizing | Max 10% |
| **3** | DCA Strategy | Average cost |
| **4** | Long-term Hold | Cross cycles |

### Risk Control

> **Never invest emergency funds in crypto.**
> 
> Only invest what you can afford to lose.

---

## 📊 Core Conclusion

**Direction**: Bullish  
**Range**: {result}  
**Confidence**: {int(probability * 100)}%

---

## ⏰ Final Words

**The digital asset era has arrived.**

You can keep doubting, or you can participate.

**History doesn't repeat, but it often rhymes.**

---

**Report ID**: `{prediction_id}`  
**Generated**: {datetime.now().strftime('%Y-%m-%d')}

---

*OpenMorning — Making Prediction Scientific*
"""

    return cn.strip(), en.strip()

def _generate_political_report_v2(question: str, result: str, probability: float, prediction_id: str) -> tuple:
    """政治分析报告 - 营销号风格"""
    
    cn = f"""
# 📊 OpenMorning 政治形势深度分析

---

## ⚠️ 你正在见证历史

**问题**：{question}

这不是普通的政治周期。

**我们正处于全球政治格局重构的关键节点。**

---

## 🔴 大多数人看不懂的政治逻辑

"选举就是投票。"

"政治就是政客的游戏。"

**这些人忽略了最关键的因素：周期。**

经济周期决定选民情绪
选民情绪决定投票行为
投票行为决定政治格局

**这是跨越国界的政治规律。**

---

## 🔍 深度解读

### 1. 经济周期与政治周期

历史数据表明：

经济向好 → 现任者优势
经济承压 → 变革呼声

**这不是预测，这是规律。**

### 2. 社会结构的深层裂痕

社会分化正在重塑政治版图。

极化环境下的选举，传统民调正在失效。

### 3. 外部环境的蝴蝶效应

国际局势变化可能成为关键变量。

---

## 💡 核心判断

**结论**：可能性较高  
**置信度**：{int(probability * 100)}%

---

## ⏰ 最后的话

**政治预测是最复杂的预测。**

本报告基于周期理论分析，不构成任何政治判断。

---

**报告编号**：`{prediction_id}`  
**生成时间**：{datetime.now().strftime('%Y年%m月%d日')}

---

*OpenMorning — 让预测成为科学*
"""

    en = f"""
# 📊 OpenMorning Political Analysis Report

---

## ⚠️ You're Witnessing History

**Question**: {question}

This is not a normal political cycle.

**We're at a critical inflection point of global political restructuring.**

---

## 🔴 What Most People Don't Understand

"Elections are just voting."

"Politics is politicians' game."

**They're missing the最关键 factor: Cycles.**

Economic cycles determine voter sentiment
Voter sentiment determines voting behavior
Voting behavior determines political landscape

**This is a cross-border political law.**

---

## 🔍 Deep Analysis

### 1. Economic Cycles & Political Cycles

Historical data shows:

Economy up → Incumbent advantage
Economy down → Change demands

**This is not prediction. This is pattern.**

### 2. Deep Social Divisions

Social polarization is reshaping political landscape.

In polarized environments, traditional polls are failing.

### 3. External Butterfly Effects

International局势 changes can be key variables.

---

## 💡 Core Judgment

**Conclusion**: High probability  
**Confidence**: {int(probability * 100)}%

---

## ⏰ Final Words

**Political prediction is the most complex.**

This report is based on cycle theory, not political judgment.

---

**Report ID**: `{prediction_id}`  
**Generated**: {datetime.now().strftime('%Y-%m-%d')}

---

*OpenMorning — Making Prediction Scientific*
"""

    return cn.strip(), en.strip()

def _generate_international_report_v2(question: str, result: str, probability: float, prediction_id: str) -> tuple:
    """国际关系分析报告 - 营销号风格"""
    
    cn = f"""
# 🌍 OpenMorning 国际形势深度分析

---

## ⚠️ 你正在见证历史

**问题**：{question}

这不是普通的外交周期。

**我们正处于全球地缘政治格局重构的关键节点。**

---

## 🔴 大多数人看不懂的国际逻辑

"国际关系就是利益交换。"

"政治就是政客的游戏。"

**这些人忽略了最关键的因素：周期。**

康波周期决定大国实力对比
实力对比决定国际格局
国际格局决定双边关系

**这是跨越百年的历史规律。**

---

## 🔍 深度解读

### 1. 康波周期与大国博弈

历史数据表明：

回升期 → 新兴大国崛起
萧条期 → 守成大国反击

**这不是预测，这是周期规律。**

### 2. 经济相互依赖的双刃剑

贸易深度绑定 = 冲突成本高
供应链脱钩 = 冲突风险升

**关键在于脱钩程度。**

### 3. 外部变量的蝴蝶效应

第三方因素可能成为关键变量。

---

## 💡 核心判断

**结论**：存在不确定性  
**置信度**：{int(probability * 100)}%

---

## ⏰ 最后的话

**国际关系预测极其复杂。**

本报告基于周期理论分析，不构成任何政治判断。

---

**报告编号**：`{prediction_id}`  
**生成时间**：{datetime.now().strftime('%Y年%m月%d日')}

---

*OpenMorning — 让预测成为科学*
"""

    en = f"""
# 🌍 OpenMorning International Relations Analysis

---

## ⚠️ You're Witnessing History

**Question**: {question}

This is not a normal diplomatic cycle.

**We're at a critical inflection point of global geopolitical restructuring.**

---

## 🔴 What Most People Don't Understand

"International relations is just interest exchange."

"Politics is politicians' game."

**They're missing the most critical factor: Cycles.**

Kondratieff cycles determine great power balance
Power balance determines international格局
International格局 determines bilateral relations

**This is a century-spanning historical pattern.**

---

## 🔍 Deep Analysis

### 1. Kondratieff Cycles & Great Power Competition

Historical data shows:

Recovery phase → Rising powers emerge
Depression phase → Established powers push back

**This is not prediction. This is cycle pattern.**

### 2. Economic Interdependence: Double-Edged Sword

Deep trade ties = High conflict cost
Supply chain decoupling = Rising conflict risk

**The key is decoupling extent.**

### 3. External Butterfly Effects

Third-party factors can be key variables.

---

## 💡 Core Judgment

**Conclusion**: Uncertainty exists  
**Confidence**: {int(probability * 100)}%

---

## ⏰ Final Words

**International relations prediction is extremely complex.**

This report is based on cycle theory, not political judgment.

---

**Report ID**: `{prediction_id}`  
**Generated**: {datetime.now().strftime('%Y-%m-%d')}

---

*OpenMorning — Making Prediction Scientific*
"""

    return cn.strip(), en.strip()


if __name__ == "__main__":
    test_data = {
        "id": "test_001",
        "question": "2026 年 A 股会涨吗？",
        "predictions": [{"result": "上涨 50-70%", "probability": 0.5}]
    }
    
    cn, en = generate_report(test_data)
    print("=== 中文版 ===")
    print(cn)
    print("\n=== English Version ===")
    print(en)