"""
OpenMorning 精炼报告生成器
结论前置、3段结构、1500字以内
"""

import json
from datetime import datetime
from typing import Dict, List, Tuple


def generate_report(prediction_data: dict) -> Tuple[str, str]:
    """生成精炼投资报告（中英双语）"""
    
    question = prediction_data.get("question", "")
    predictions = prediction_data.get("predictions", [])
    analysis = prediction_data.get("analysis", {})
    prediction_id = prediction_data.get("id", "")
    
    # 生成精炼中文报告
    cn_report = _generate_concise_cn_report(
        question, predictions, analysis, prediction_id
    )
    
    # 生成英文摘要
    en_report = _generate_en_summary(question, predictions, prediction_id)
    
    return cn_report, en_report


def _generate_concise_cn_report(
    question: str,
    predictions: List[Dict],
    analysis: Dict,
    prediction_id: str
) -> str:
    """生成精炼中文报告（结论前置、3段结构）"""
    
    # 找出最佳预测
    best = max(predictions, key=lambda x: x.get("probability", 0))
    result = best.get("result", "")
    probability = best.get("probability", 0)
    
    # 判断方向和评级
    if "上涨" in result and "下跌" not in result:
        direction = "看涨"
        rating = "买入"
        emoji = "📈"
    elif "下跌" in result:
        direction = "看跌"
        rating = "卖出"
        emoji = "📉"
    else:
        direction = "中性"
        rating = "持有"
        emoji = "➡️"
    
    # 提取关键洞察（top 3）
    insights = _extract_key_insights(analysis)
    
    # 提取核心理由（一句话）
    core_reason = _build_core_reason(insights, direction)
    
    # 构建报告（3段结构）
    report = f"""# {emoji} OpenMorning 投资报告

**{question}**

---

## 📊 核心结论

**投资评级**: {rating} | **预测方向**: {direction} | **置信度**: {probability:.0%}

**核心理由**: {core_reason}

---

## 🔍 关键证据

{_build_key_evidence(insights[:3])}

---

## 💡 操作建议

{_build_dynamic_advice(direction, predictions, analysis)}

---

**预测ID**: `{prediction_id}` | **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

验证命令: `/openmorning verify {prediction_id} result: 实际结果`

*本报告由 OpenMorning 自动生成，仅供参考，不构成投资建议*
"""
    
    return report


def _extract_key_insights(analysis: Dict) -> List[Dict]:
    """提取关键洞察（按置信度排序）"""
    insights = []
    
    for name, res in analysis.items():
        if "error" in res:
            continue
        
        signal = res.get("signal", "neutral")
        confidence = res.get("confidence", 0)
        reasoning = res.get("reasoning", "")
        
        if confidence >= 0.4:  # 降低阈值，确保有足够信号
            insights.append({
                "dimension": name,
                "signal": signal,
                "confidence": confidence,
                "reasoning": reasoning
            })
    
    return sorted(insights, key=lambda x: x["confidence"], reverse=True)


def _build_core_reason(insights: List[Dict], direction: str) -> str:
    """构建核心理由（一句话）"""
    if not insights:
        return "多维度信号不明确，建议观望"
    
    top = insights[0]
    dim_name = _get_dimension_name(top["dimension"])
    
    if direction == "看涨":
        return f"{dim_name}支持上涨，{top['reasoning']}"
    elif direction == "看跌":
        return f"{dim_name}指向下跌，{top['reasoning']}"
    else:
        return f"{dim_name}显示中性，多空力量均衡"


def _build_key_evidence(insights: List[Dict]) -> str:
    """构建关键证据（top 3）"""
    if not insights:
        return "暂无明确信号"
    
    text = ""
    for i, insight in enumerate(insights, 1):
        dim_name = _get_dimension_name(insight["dimension"])
        signal_text = {"bullish": "看涨", "bearish": "看跌", "neutral": "中性"}.get(insight["signal"], "未知")
        
        text += f"**{i}. {dim_name}** ({signal_text}, 置信度 {insight['confidence']:.0%})\n\n"
        text += f"{insight['reasoning']}\n\n"
    
    return text


def _build_dynamic_advice(direction: str, predictions: List[Dict], analysis: Dict) -> str:
    """动态生成操作建议"""
    # 提取预测幅度
    best = max(predictions, key=lambda x: x.get("probability", 0))
    result = best.get("result", "")
    
    # 提取数字范围
    import re
    numbers = re.findall(r'(\d+)', result)
    
    if direction == "看涨":
        advice = "**建议操作**: 逐步建仓，分批买入\n\n"
        advice += "**仓位配置**: 激进 60-70% | 稳健 40-50% | 保守 20-30%\n\n"
        
        if numbers and len(numbers) >= 2:
            low, high = int(numbers[0]), int(numbers[1])
            advice += f"**目标收益**: {low}-{high}%\n\n"
        
        advice += "**风险控制**: 设置止损位，单次亏损不超过 5%"
        
    elif direction == "看跌":
        advice = "**建议操作**: 减仓观望，保留现金\n\n"
        advice += "**仓位配置**: 降至 30% 以下，持有防御性资产\n\n"
        advice += "**风险控制**: 严格止损，避免深套"
        
    else:
        advice = "**建议操作**: 观望为主，等待明确信号\n\n"
        advice += "**仓位配置**: 维持现有仓位，不追涨杀跌\n\n"
        advice += "**风险控制**: 保持灵活，随时调整"
    
    return advice


def _get_dimension_name(dimension: str) -> str:
    """获取维度中文名"""
    name_map = {
        "economic_cycle": "经济周期",
        "policy": "政策环境",
        "sentiment": "市场情绪",
        "metaphysics": "周期玄学",
        "tech": "技术革命",
        "international": "国际环境",
        "capital_flow": "资金流向",
        "valuation": "估值水平",
        "risk": "风险评估"
    }
    return name_map.get(dimension, dimension)


def _generate_en_summary(question: str, predictions: List[Dict], prediction_id: str) -> str:
    """生成英文摘要"""
    best = max(predictions, key=lambda x: x.get("probability", 0))
    result = best.get("result", "")
    probability = best.get("probability", 0)
    
    return f"""# OpenMorning Investment Report

**Question**: {question}

**Prediction**: {result} (Confidence: {probability:.0%})

**Prediction ID**: `{prediction_id}`

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

*This report is for reference only and does not constitute investment advice.*
"""
