"""
SentimentAgent - 市场情绪分析 Agent

分析市场恐惧/贪婪指数、社交媒体情绪
"""

import json
from typing import Dict, Any

class SentimentAgent:
    """市场情绪分析 Agent"""
    
    def __init__(self):
        self.name = "SentimentAgent"
        self.weight = 0.2
    
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """分析市场情绪"""
        question = context.get("question", "")
        
        # 检测情绪关键词
        fear_keywords = ["恐慌", "暴跌", "崩盘", "危机", "制裁", "次贷", "股灾"]
        greed_keywords = ["暴涨", "牛市", "繁荣", "机会", "狂热", "泡沫", "疯涨"]
        systemic_risk_keywords = ["系统性", "流动性枯竭", "央行", "违约"]
        
        fear_count = sum(1 for kw in fear_keywords if kw in question)
        greed_count = sum(1 for kw in greed_keywords if kw in question)
        has_systemic_risk = any(kw in question for kw in systemic_risk_keywords)
        
        # 优先使用搜索到的数据，否则根据关键词估算
        fear_index = context.get("fear_index")
        if fear_index is None:
            if fear_count > 0:
                fear_index = max(10, 30 - fear_count * 5)  # 映射到恐惧区间
            elif greed_count > 0:
                fear_index = min(90, 70 + greed_count * 5)  # 映射到贪婪区间
            else:
                fear_index = 50  # 默认中性
            data_source = "关键词推断"
        else:
            data_source = "实时搜索"
        
        # 情绪信号判断（统一阈值：20/40/60/80）
        if fear_index < 20:
            # 极度恐惧 - 检查系统性风险
            if has_systemic_risk:
                signal = "neutral"
                description = "极度恐惧但存在系统性风险，暂不逆向"
            else:
                signal = "bullish"
                description = "极度恐惧，市场可能见底"
        elif fear_index < 40:
            signal = "bullish"
            description = "恐惧情绪，存在反转机会"
        elif fear_index > 80:
            signal = "bearish"
            description = "极度贪婪，市场可能见顶"
        elif fear_index > 60:
            signal = "bearish"
            description = "贪婪情绪，需谨慎"
        else:
            signal = "neutral"
            description = "情绪中性"
        
        # 置信度计算（区分数据源）
        base_confidence = abs(fear_index - 50) / 50
        if data_source == "关键词推断":
            confidence = min(0.5, base_confidence)  # 关键词推断上限 0.5
        else:
            confidence = min(0.9, base_confidence)  # 实时数据上限 0.9
        
        return {
            "agent": self.name,
            "weight": self.weight,  # 固定权重，不动态调整
            "analysis": {
                "fear_index": fear_index,
                "sentiment": self._get_sentiment_label(fear_index),
                "data_source": data_source,
                "has_systemic_risk": has_systemic_risk
            },
            "signal": signal,
            "confidence": confidence,
            "reasoning": description
        }
    
    def _get_sentiment_label(self, fear_index: int) -> str:
        if fear_index < 20:
            return "极度恐惧"
        elif fear_index < 40:
            return "恐惧"
        elif fear_index < 60:
            return "中性"
        elif fear_index < 80:
            return "贪婪"
        else:
            return "极度贪婪"


if __name__ == "__main__":
    agent = SentimentAgent()
    result = agent.analyze({"fear_index": 30})
    print(json.dumps(result, indent=2, ensure_ascii=False))