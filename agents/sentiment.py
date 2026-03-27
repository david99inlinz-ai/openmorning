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
        fear_index = context.get("fear_index", 50)  # 0-100, <25极度恐惧, >75极度贪婪
        
        # 情绪信号判断
        if fear_index < 25:
            signal = "bullish"  # 极度恐惧可能是买入机会
            description = "极度恐惧，市场可能见底"
        elif fear_index < 45:
            signal = "bullish"
            description = "恐惧情绪，存在反转机会"
        elif fear_index > 75:
            signal = "bearish"  # 极度贪婪可能见顶
            description = "极度贪婪，市场可能见顶"
        elif fear_index > 55:
            signal = "bearish"
            description = "贪婪情绪，需谨慎"
        else:
            signal = "neutral"
            description = "情绪中性"
        
        return {
            "agent": self.name,
            "weight": self.weight,
            "analysis": {
                "fear_index": fear_index,
                "sentiment": self._get_sentiment_label(fear_index)
            },
            "signal": signal,
            "confidence": abs(fear_index - 50) / 50,  # 偏离中性的程度
            "description": description
        }
    
    def _get_sentiment_label(self, fear_index: int) -> str:
        if fear_index < 25:
            return "极度恐惧"
        elif fear_index < 45:
            return "恐惧"
        elif fear_index < 55:
            return "中性"
        elif fear_index < 75:
            return "贪婪"
        else:
            return "极度贪婪"


if __name__ == "__main__":
    agent = SentimentAgent()
    result = agent.analyze({"fear_index": 30})
    print(json.dumps(result, indent=2, ensure_ascii=False))