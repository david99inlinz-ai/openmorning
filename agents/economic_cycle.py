"""
EconomicCycleAgent - 经济周期分析 Agent

分析康波周期、朱格拉周期、基钦周期的当前阶段
"""

import json
from datetime import datetime
from typing import Dict, Any

class EconomicCycleAgent:
    """经济周期分析 Agent"""
    
    def __init__(self):
        self.name = "EconomicCycleAgent"
        self.weight = 0.3  # 默认权重
        
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析当前经济周期
        
        Args:
            context: 包含时间、市场等信息
            
        Returns:
            周期分析结果
        """
        year = context.get("year", datetime.now().year)
        
        # 康波周期分析（50-60年）
        kondratieff = self._analyze_kondratieff(year)
        
        # 朱格拉周期分析（7-11年）
        juglar = self._analyze_juglar(year)
        
        # 基钦周期分析（3-4年）
        kitchin = self._analyze_kitchin(year)
        
        # 货币周期分析
        rate_cycle = self._analyze_rate_cycle(context)
        
        # 综合信号
        signal = self._combine_signals(kondratieff, juglar, kitchin, rate_cycle)
        
        return {
            "agent": self.name,
            "weight": self.weight,
            "analysis": {
                "kondratieff": kondratieff,
                "juglar": juglar,
                "kitchin": kitchin,
                "rate_cycle": rate_cycle
            },
            "signal": signal["direction"],
            "confidence": signal["confidence"],
            "reasoning": signal["reasoning"]
        }
    
    def _analyze_kondratieff(self, year: int) -> Dict[str, Any]:
        """康波周期分析"""
        # 第五轮康波：1991-2050
        # 繁荣期：1991-2000
        # 衰退期：2000-2015
        # 萧条期：2015-2025
        # 回升期：2025-2050
        
        if 2025 <= year < 2050:
            phase = "回升期"
            signal = "bullish"
            description = "新周期起点，技术革命酝酿，投资机会增多"
        elif 2015 <= year < 2025:
            phase = "萧条期"
            signal = "bearish"
            description = "经济低迷，存量博弈，风险资产承压"
        elif 2000 <= year < 2015:
            phase = "衰退期"
            signal = "neutral"
            description = "增长放缓，泡沫破裂风险"
        else:
            phase = "繁荣期"
            signal = "bullish"
            description = "技术革命爆发，经济高速增长"
            
        return {
            "cycle": "康波周期",
            "phase": phase,
            "signal": signal,
            "description": description,
            "period": "50-60年"
        }
    
    def _analyze_juglar(self, year: int) -> Dict[str, Any]:
        """朱格拉周期分析（设备投资周期）"""
        # 中国朱格拉周期约 7-10 年
        # 2009-2016, 2016-2023, 2023-2030
        
        cycle_year = (year - 2009) % 7
        
        if cycle_year < 3:
            phase = "扩张期"
            signal = "bullish"
        elif cycle_year < 5:
            phase = "顶部期"
            signal = "neutral"
        else:
            phase = "收缩期"
            signal = "bearish"
            
        return {
            "cycle": "朱格拉周期",
            "phase": phase,
            "signal": signal,
            "period": "7-11年"
        }
    
    def _analyze_kitchin(self, year: int) -> Dict[str, Any]:
        """基钦周期分析（库存周期）"""
        # 约 40 个月
        cycle_month = ((year - 2000) * 12) % 40
        
        if cycle_month < 20:
            phase = "补库存"
            signal = "bullish"
        else:
            phase = "去库存"
            signal = "bearish"
            
        return {
            "cycle": "基钦周期",
            "phase": phase,
            "signal": signal,
            "period": "3-4年"
        }
    
    def _analyze_rate_cycle(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """货币周期分析"""
        # 根据上下文判断
        rate_trend = context.get("rate_trend", "unknown")
        
        if rate_trend == "降息":
            signal = "bullish"
            description = "降息周期利好风险资产"
        elif rate_trend == "加息":
            signal = "bearish"
            description = "加息周期压制估值"
        else:
            signal = "neutral"
            description = "利率稳定"
            
        return {
            "cycle": "货币周期",
            "trend": rate_trend,
            "signal": signal,
            "description": description
        }
    
    def _combine_signals(self, kondratieff, juglar, kitchin, rate_cycle) -> Dict[str, Any]:
        """综合多周期信号"""
        signals = [
            (kondratieff["signal"], 0.4),  # 康波权重最高
            (juglar["signal"], 0.25),
            (kitchin["signal"], 0.15),
            (rate_cycle["signal"], 0.2)
        ]
        
        bullish_score = sum(w for s, w in signals if s == "bullish")
        bearish_score = sum(w for s, w in signals if s == "bearish")
        
        if bullish_score > bearish_score + 0.2:
            direction = "bullish"
            confidence = bullish_score
        elif bearish_score > bullish_score + 0.2:
            direction = "bearish"
            confidence = bearish_score
        else:
            direction = "neutral"
            confidence = 0.5
            
        reasoning = f"康波{kondratieff['phase']}+朱格拉{juglar['phase']}+基钦{kitchin['phase']}"
        
        return {
            "direction": direction,
            "confidence": confidence,
            "reasoning": reasoning
        }
    
    def update_weight(self, accuracy: float):
        """根据准确率更新权重"""
        if accuracy > 0.7:
            self.weight = min(0.5, self.weight + 0.05)
        elif accuracy < 0.5:
            self.weight = max(0.1, self.weight - 0.05)


if __name__ == "__main__":
    agent = EconomicCycleAgent()
    result = agent.analyze({"year": 2026, "rate_trend": "降息"})
    print(json.dumps(result, indent=2, ensure_ascii=False))