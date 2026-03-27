# 🌅 OpenMorning - Open Source Prediction Engine

**Making predictions scientific, not guesswork.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

---

## Core Philosophy

> History often rhymes. Predictions need verification. Verification brings learning.

OpenMorning is an open-source prediction engine combining:
- **Economic Cycles** (Kondratieff/Juglar/Kitchin)
- **Real-time News**
- **Market Sentiment**
- **Metaphysics Analysis** (optional)

Continuously learning through user verification feedback.

---

## Quick Start

### Use in OpenClaw

```
/openmorning Will A-shares rise in 2026?
/openmorning Can Bitcoin reach $150K in 2026?
/openmorning AI industry trends in 2026
```

### Verify Predictions

```
/openmorning verify pred_20260327_001 result: up 12%
```

---

## Key Features

### 1. Full Analysis (No Filtering)

All agents analyze in parallel, never miss any possibility.

### 2. Multi-Scenario Predictions

Generate bullish/neutral/bearish scenarios with probabilities.

### 3. Historical Case Matching

Automatically match similar historical cases for reference.

### 4. Verification Feedback Loop

```
Predict → Record → Wait → Verify → Learn → Evolve
```

### 5. Continuous Learning

Update agent weights after each verification. Gets smarter with use.

---

## Architecture

```
User Request
    ↓
【Analysis Layer】Full Analysis
    ├─ EconomicCycleAgent
    ├─ SentimentAgent
    └─ MetaphysicsAgent
    ↓
【Prediction Layer】Multi-Scenario Generation
    ├─ Bullish Scenario
    ├─ Neutral Scenario
    └─ Bearish Scenario
    ↓
【Record Layer】Save Prediction
    data/predictions.json
    ↓
【Verification Layer】User Feedback
    └─ Analyze why right/wrong
    ↓
【Learning Layer】Update Weights
    cases.json + Agent weight adjustment
```

---

## Cycle Theory Reference

### Kondratieff Cycle (50-60 years)

| Phase | Characteristics | Current Status |
|-------|----------------|----------------|
| Prosperity | Tech revolution | - |
| Recession | Growth slowdown | - |
| Depression | Economic downturn | 2015-2025 |
| Recovery | New cycle start | **2026-** |

### Juglar Cycle (7-11 years)

Equipment investment cycle, affects medium-term economic trends.

### Kitchin Cycle (3-4 years)

Inventory cycle, affects short-term market volatility.

---

## Data Collection Notice

This is an open-source project. User prediction questions and verification results are collected for model optimization.

**Data Collected**:
- Prediction questions
- Analysis process
- Prediction results
- Verification results
- Lessons learned

**Not Collected**: Personal privacy information

Data used for:
- Improving prediction accuracy
- Building historical case library
- Academic research

---

## Disclaimer

1. For research and entertainment purposes only
2. Predictions do not constitute investment advice
3. Past performance does not indicate future results
4. Investment involves risk, decisions should be cautious

---

## Contributing

Contributions welcome:
- New analysis agents
- Historical case data
- Prediction logic improvements
- Verification analysis methods

### Development Setup

```bash
git clone https://github.com/david99inlinz-ai/openmorning.git
cd openmorning
pip install -r requirements.txt
```

### Testing

```bash
python openmorning.py
```

---

## License

MIT License - See [LICENSE](LICENSE)

---

## Contact

- GitHub: https://github.com/david99inlinz-ai/openmorning
- Issues: https://github.com/david99inlinz-ai/openmorning/issues

---

# 🌅 OpenMorning - 开源预测引擎

**让预测成为科学，不再是瞎猜。**

---

## 核心理念

> 历史总是惊人的相似，预测需要验证，验证带来学习。

OpenMorning 是一个开源的预测引擎，结合：
- **经济学周期**（康波/朱格拉/基钦）
- **实时新闻**
- **市场情绪**
- **玄学分析**（可选）

通过用户验证反馈持续学习进化。

---

## 快速开始

### 在 OpenClaw 中使用

```
/openmorning 2026 年 A 股会涨吗？
/openmorning 比特币 2026 年能到 15 万美元吗？
```

### 验证预测

```
/openmorning verify pred_20260327_001 结果：上涨 12%
```

---

## 核心特性

- 全量分析，不漏掉任何可能
- 多方案预测，概率 + 关键因素
- 历史案例匹配
- 验证反馈闭环
- 持续学习进化

---

## 免责声明

1. 仅供研究和娱乐用途
2. 预测不构成投资建议
3. 投资有风险，决策需谨慎

---

**🌅 让每一次预测都成为学习的机会。**