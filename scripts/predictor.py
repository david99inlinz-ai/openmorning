#!/usr/bin/env python3
"""
OpenMorning - 开源预测引擎
核心预测逻辑
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
PREDICTIONS_FILE = DATA_DIR / "predictions.json"
CASES_FILE = DATA_DIR / "cases.json"


def load_predictions():
    """加载预测记录"""
    if PREDICTIONS_FILE.exists():
        with open(PREDICTIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"predictions": [], "metadata": {"version": "1.0.0"}}


def save_predictions(data):
    """保存预测记录"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(PREDICTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_cases():
    """加载历史案例"""
    if CASES_FILE.exists():
        with open(CASES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"cases": [], "metadata": {"version": "1.0.0"}}


def save_cases(data):
    """保存历史案例"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(CASES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def analyze_question(question):
    """
    分析问题，识别类型和关键信息
    """
    # 简单关键词匹配（后续可扩展为 NLP）
    question_lower = question.lower()
    
    analysis = {
        "type": "general",
        "time_horizon": "medium",
        "domain": "general"
    }
    
    # 识别领域
    if any(kw in question_lower for kw in ["a 股", "股市", "股票", "大盘"]):
        analysis["domain"] = "stock"
    elif any(kw in question_lower for kw in ["比特币", "crypto", "btc", "eth"]):
        analysis["domain"] = "crypto"
    elif any(kw in question_lower for kw in ["经济", "gdp", "衰退", "繁荣"]):
        analysis["domain"] = "economy"
    elif any(kw in question_lower for kw in ["ai", "人工智能", "科技", "行业"]):
        analysis["domain"] = "industry"
    elif any(kw in question_lower for kw in ["运势", "事业", "财运", "个人"]):
        analysis["domain"] = "personal"
    
    # 识别时间维度
    if any(kw in question_lower for kw in ["2026", "明年", "今年"]):
        analysis["time_horizon"] = "short"
    elif any(kw in question_lower for kw in ["2027", "2028", "未来几年"]):
        analysis["time_horizon"] = "medium"
    elif any(kw in question_lower for kw in ["2030", "未来十年"]):
        analysis["time_horizon"] = "long"
    
    return analysis


def get_kondratieff_analysis(year=2026):
    """
    康波周期分析
    基于周金涛研究：2025-2026 年是第五轮康波萧条末期与第六轮康波回升期起点
    """
    # 2026 年处于康波回升期起点
    return {
        "phase": "回升期",
        "signal": "bullish",
        "confidence": 0.8,
        "description": "2026 年是第六轮康波周期正式启动的标志性时间点",
        "reference": "周金涛研究"
    }


def get_juglar_analysis(year=2026):
    """
    朱格拉周期分析（7-11 年设备投资周期）
    """
    # 简化逻辑，实际应基于设备投资数据
    return {
        "phase": "扩张期",
        "signal": "bullish",
        "confidence": 0.7,
        "description": "设备投资周期处于扩张阶段"
    }


def get_rate_cycle_analysis(year=2026):
    """
    货币周期分析（降息/加息）
    """
    # 2026 年全球处于降息周期
    return {
        "phase": "降息",
        "signal": "bullish",
        "confidence": 0.75,
        "description": "全球流动性迎来拐点，降息周期打开估值弹性"
    }


def get_sentiment_analysis():
    """
    市场情绪分析
    """
    # 简化版本，实际应接入实时数据
    return {
        "fear_index": 30,
        "signal": "reversal_possible",
        "confidence": 0.6,
        "description": "恐慌指数处于低位，可能出现反转"
    }


def find_similar_cases(context):
    """
    查找相似历史案例
    """
    cases_data = load_cases()
    similar = []
    
    for case in cases_data.get("cases", []):
        similarity = 0
        
        # 康波阶段匹配
        if case.get("context", {}).get("kondratieff") == context.get("kondratieff"):
            similarity += 0.4
        
        # 利率周期匹配
        if case.get("context", {}).get("rate_cycle") == context.get("rate_cycle"):
            similarity += 0.3
        
        # 情绪匹配
        if case.get("context", {}).get("sentiment") == context.get("sentiment"):
            similarity += 0.3
        
        if similarity >= 0.3:
            similar.append({
                "year": case.get("time"),
                "context": case.get("context"),
                "result": case.get("result"),
                "similarity": similarity
            })
    
    # 按相似度排序
    similar.sort(key=lambda x: x["similarity"], reverse=True)
    return similar[:3]  # 返回最相似的 3 个


def generate_predictions(analysis):
    """
    生成多方案预测
    """
    # 基于周期分析生成预测
    kondratieff = get_kondratieff_analysis()
    juglar = get_juglar_analysis()
    rate = get_rate_cycle_analysis()
    sentiment = get_sentiment_analysis()
    
    # 计算综合信号
    bullish_signals = sum([
        1 if kondratieff["signal"] == "bullish" else 0,
        1 if juglar["signal"] == "bullish" else 0,
        1 if rate["signal"] == "bullish" else 0,
    ])
    
    # 生成多方案
    predictions = []
    
    if bullish_signals >= 2:
        # 多数看涨
        predictions = [
            {
                "scenario": "乐观",
                "result": "上涨50-70%",
                "probability": 0.5,
                "key_factors": ["康波回升期", "降息周期", "设备投资扩张"]
            },
            {
                "scenario": "中性",
                "result": "上涨20-40%",
                "probability": 0.3,
                "key_factors": ["震荡上行"]
            },
            {
                "scenario": "悲观",
                "result": "下跌10-20%",
                "probability": 0.2,
                "key_factors": ["黑天鹅事件"]
            }
        ]
    elif bullish_signals == 1:
        # 中性
        predictions = [
            {
                "scenario": "乐观",
                "result": "上涨10-20%",
                "probability": 0.3,
                "key_factors": ["结构性机会"]
            },
            {
                "scenario": "中性",
                "result": "持平±5%",
                "probability": 0.4,
                "key_factors": ["震荡市"]
            },
            {
                "scenario": "悲观",
                "result": "下跌10-20%",
                "probability": 0.3,
                "key_factors": ["下行压力"]
            }
        ]
    else:
        # 多数看跌
        predictions = [
            {
                "scenario": "乐观",
                "result": "上涨10-20%",
                "probability": 0.2,
                "key_factors": ["超跌反弹"]
            },
            {
                "scenario": "中性",
                "result": "下跌10-20%",
                "probability": 0.4,
                "key_factors": ["震荡下行"]
            },
            {
                "scenario": "悲观",
                "result": "下跌30-50%",
                "probability": 0.4,
                "key_factors": ["周期共振下跌"]
            }
        ]
    
    return predictions, {
        "kondratieff_cycle": kondratieff,
        "juglar_cycle": juglar,
        "rate_cycle": rate,
        "sentiment": sentiment
    }


def create_prediction(question):
    """
    创建新的预测记录
    """
    data = load_predictions()
    
    # 分析问题
    analysis = analyze_question(question)
    
    # 生成预测
    predictions, factors = generate_predictions(analysis)
    
    # 查找相似历史案例
    context = {
        "kondratieff": factors["kondratieff_cycle"]["phase"],
        "juglar": factors["juglar_cycle"]["phase"],
        "rate_cycle": factors["rate_cycle"]["phase"],
        "sentiment": factors["sentiment"]["signal"]
    }
    similar_cases = find_similar_cases(context)
    
    # 生成预测 ID
    prediction_id = f"pred_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # 创建预测记录
    prediction = {
        "prediction_id": prediction_id,
        "question": question,
        "created_at": datetime.now().isoformat(),
        "verify_date": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
        "analysis": factors,
        "predictions": predictions,
        "similar_cases": similar_cases,
        "status": "pending",
        "verification": None,
        "lessons": None
    }
    
    # 保存
    data["predictions"].append(prediction)
    save_predictions(data)
    
    return prediction


def verify_prediction(prediction_id, actual_result, user_analysis=None):
    """
    验证预测结果
    """
    data = load_predictions()
    
    # 查找预测记录
    prediction = None
    for p in data["predictions"]:
        if p["prediction_id"] == prediction_id:
            prediction = p
            break
    
    if not prediction:
        return {"error": "预测记录不存在"}
    
    # 分析预测准确性
    verification = {
        "verified_at": datetime.now().isoformat(),
        "actual_result": actual_result,
        "user_analysis": user_analysis,
        "accuracy": {}
    }
    
    # 方向判断
    predicted_direction = "上涨" if "上涨" in str(prediction["predictions"][0]["result"]) else "下跌"
    actual_direction = "上涨" if "上涨" in str(actual_result) else "下跌"
    
    verification["accuracy"]["direction"] = predicted_direction == actual_direction
    verification["accuracy"]["direction_text"] = "✓ 方向正确" if verification["accuracy"]["direction"] else "✗ 方向错误"
    
    # 更新记录
    prediction["verification"] = verification
    prediction["status"] = "verified"
    
    save_predictions(data)
    
    # 添加到历史案例库
    add_to_cases(prediction, verification)
    
    return verification


def add_to_cases(prediction, verification):
    """
    将验证后的预测添加到历史案例库
    """
    cases_data = load_cases()
    
    case = {
        "id": prediction["prediction_id"],
        "time": datetime.now().strftime("%Y"),
        "question": prediction["question"],
        "context": {
            "kondratieff": prediction["analysis"]["kondratieff_cycle"]["phase"],
            "juglar": prediction["analysis"]["juglar_cycle"]["phase"],
            "rate_cycle": prediction["analysis"]["rate_cycle"]["phase"],
            "sentiment": prediction["analysis"]["sentiment"]["signal"]
        },
        "prediction": prediction["predictions"][0]["result"],
        "result": verification["actual_result"],
        "analysis": verification.get("user_analysis", ""),
        "lessons": ""
    }
    
    cases_data["cases"].append(case)
    save_cases(cases_data)


# 主函数：供 Skill 调用
def predict(question):
    """
    主预测函数
    """
    result = create_prediction(question)
    
    # 格式化输出
    output = f"""
# 🌅 OpenMorning 预测报告

**预测 ID**: `{result['prediction_id']}`
**问题**: {result['question']}
**验证日期**: {result['verify_date']}

---

## 📊 周期分析

| 周期类型 | 阶段 | 信号 | 置信度 |
|---------|------|------|--------|
| 康波周期 | {result['analysis']['kondratieff_cycle']['phase']} | {result['analysis']['kondratieff_cycle']['signal']} | {result['analysis']['kondratieff_cycle']['confidence']:.0%} |
| 朱格拉周期 | {result['analysis']['juglar_cycle']['phase']} | {result['analysis']['juglar_cycle']['signal']} | {result['analysis']['juglar_cycle']['confidence']:.0%} |
| 货币周期 | {result['analysis']['rate_cycle']['phase']} | {result['analysis']['rate_cycle']['signal']} | {result['analysis']['rate_cycle']['confidence']:.0%} |
| 市场情绪 | 恐慌指数{result['analysis']['sentiment']['fear_index']} | {result['analysis']['sentiment']['signal']} | {result['analysis']['sentiment']['confidence']:.0%} |

---

## 🔮 多方案预测

| 方案 | 结果 | 概率 | 关键因素 |
|------|------|------|---------|
"""
    
    for pred in result["predictions"]:
        factors = "、".join(pred["key_factors"])
        output += f"| {pred['scenario']} | {pred['result']} | {pred['probability']:.0%} | {factors} |\n"
    
    output += "\n---\n\n## 📚 相似历史案例\n\n"
    
    if result["similar_cases"]:
        for case in result["similar_cases"]:
            output += f"- **{case['year']}年**: {case['context'].get('kondratieff', '')} → {case['result']}（相似度{case['similarity']:.0%}）\n"
    else:
        output += "暂无相似案例\n"
    
    output += f"""
---

## 📝 验证说明

请在 **{result['verify_date']}** 后使用以下命令验证：

```
/openmorning verify {result['prediction_id']} 实际结果
```

例如：
```
/openmorning verify {result['prediction_id']} 上涨12%
```

---

⚠️ **免责声明**: 本预测仅供参考，不构成投资建议。投资有风险，决策需谨慎。

📊 **数据收集**: 本预测将匿名收录到 OpenMorning 历史案例库，用于模型优化。
"""
    
    return output


def verify_cmd(prediction_id, actual_result):
    """
    验证命令
    """
    result = verify_prediction(prediction_id, actual_result)
    
    if "error" in result:
        return f"❌ 错误：{result['error']}"
    
    output = f"""
# ✅ 验证报告

**预测 ID**: `{prediction_id}`
**实际结果**: {actual_result}
**验证时间**: {result['verified_at']}

---

## 📊 准确性分析

- **方向判断**: {result['accuracy']['direction_text']}

---

## 📝 分析建议

请补充详细分析（为什么对/为什么错）：
```
/openmorning analyze {prediction_id} 详细分析内容
```

---

🎯 感谢验证！您的反馈将帮助 OpenMorning 变得更准确。
"""
    
    return output


if __name__ == "__main__":
    # 测试
    import sys
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        print(predict(question))