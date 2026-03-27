# 🌅 OpenMorning - 开源预测引擎

**让预测不再是瞎猜，而是有据可依、持续进化的科学。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

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
/openmorning 2026 年 AI 行业发展趋势
```

### 验证预测

```
/openmorning verify pred_20260327_001
结果：上涨 12%
```

---

## 核心特性

### 1. 全量分析（不筛选）

所有 Agent 并行分析，不漏掉任何可能：
- EconomicCycleAgent - 康波/朱格拉/基钦周期
- SentimentAgent - 市场情绪分析
- MetaphysicsAgent - 玄学分析（可选）

### 2. 多方案预测

生成乐观/中性/悲观三个方案，每个方案有概率和关键因素。

### 3. 历史案例匹配

自动匹配相似历史案例，参考历史结果。

### 4. 验证反馈闭环

```
预测 → 记录 → 等待 → 验证 → 学习 → 进化
```

### 5. 持续学习

每次验证后更新 Agent 权重，越用越准。

---

## 架构设计

```
用户请求
    ↓
【分析层】全量分析（不筛选）
    ├─ EconomicCycleAgent
    ├─ SentimentAgent
    └─ MetaphysicsAgent
    ↓
【预测层】多方案生成
    ├─ 方案 A（乐观）
    ├─ 方案 B（中性）
    └─ 方案 C（悲观）
    ↓
【记录层】保存预测
    data/predictions.json
    ↓
【验证层】用户反馈验证
    └─ 分析为什么对/错
    ↓
【学习层】更新权重
    data/cases.json + Agent 权重调整
```

---

## 输出示例

```json
{
  "prediction_id": "pred_20260327_001",
  "question": "2026 年 A 股会涨吗？",
  "analysis": {
    "economic_cycle": {
      "kondratieff": {"phase": "回升期", "signal": "bullish"},
      "juglar": {"phase": "扩张期", "signal": "bullish"},
      "rate_cycle": {"phase": "降息", "signal": "bullish"}
    },
    "sentiment": {"fear_index": 30, "signal": "reversal_possible"},
    "metaphysics": {"period": "九紫离火运", "signal": "bullish"}
  },
  "predictions": [
    {"scenario": "乐观", "result": "上涨 50-70%", "probability": 0.5},
    {"scenario": "中性", "result": "上涨 20-40%", "probability": 0.3},
    {"scenario": "悲观", "result": "下跌 10-20%", "probability": 0.2}
  ],
  "similar_cases": [
    {"year": 1982, "context": "康波回升期", "result": "上涨 45%"},
    {"year": 2019, "context": "降息周期", "result": "上涨 25%"}
  ]
}
```

---

## 数据收集声明

本 Skill 为开源项目，会收集用户的预测问题和验证结果用于模型优化。

**收集的数据**：
- 预测问题
- 分析过程
- 预测结果
- 验证结果
- 经验教训

**不会收集**：个人隐私信息

数据将用于：
- 改进预测准确率
- 建立历史案例库
- 学术研究

---

## 贡献指南

欢迎贡献：
1. 新的分析 Agent
2. 历史案例数据
3. 预测逻辑优化
4. 验证分析方法

### 开发环境

```bash
git clone https://github.com/openclaw/openmorning.git
cd openmorning
pip install -r requirements.txt
```

### 测试

```bash
python openmorning.py
```

---

## 周期理论参考

### 康波周期（50-60 年）

| 阶段 | 特征 | 当前状态 |
|------|------|---------|
| 繁荣期 | 技术革命爆发 | - |
| 衰退期 | 增长放缓 | - |
| 萧条期 | 经济低迷 | 2015-2025 |
| 回升期 | 新周期起点 | **2026-** |

### 朱格拉周期（7-11 年）

设备投资周期，影响中期经济走势。

### 基钦周期（3-4 年）

库存周期，影响短期市场波动。

---

## 玄学分析（可选）

基于易经、五行等传统文化进行分析。

**注意**：玄学分析仅供参考，不构成决策依据。

---

## 免责声明

1. 本 Skill 仅供研究和娱乐用途
2. 预测结果不构成投资建议
3. 历史表现不代表未来结果
4. 投资有风险，决策需谨慎

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 联系方式

- GitHub: https://github.com/openclaw/openmorning
- 问题反馈：https://github.com/openclaw/openmorning/issues

---

**🌅 让每一次预测都成为学习的机会。**