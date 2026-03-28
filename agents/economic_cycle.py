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
        
        # 历史重大事件数据库（区间 + 衰减）
        self.major_events = [
            (1997, 1999, {"event": "亚洲金融危机", "signal": "bearish", "decay": [1.0, 0.6, 0.3]}),
            (2001, 2003, {"event": "加入WTO", "signal": "bullish", "decay": [1.0, 0.7, 0.4]}),
            (2008, 2010, {"event": "全球金融危机", "signal": "bearish", "decay": [1.0, 0.6, 0.3]}),
            (2015, 2017, {"event": "股灾+去杠杆", "signal": "bearish", "decay": [1.0, 0.5, 0.2]}),
            (2020, 2022, {"event": "疫情", "signal": "neutral", "decay": [1.0, 0.6, 0.3]})
        ]
        
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析当前经济周期
        
        Args:
            context: 包含时间、市场、问题等信息
            
        Returns:
            周期分析结果
        """
        year = context.get("year", datetime.now().year)
        question = context.get("question", "")
        
        # 检测风险关键词（仅作为标记，不影响信号）
        risk_keywords = ["危机", "崩盘", "暴跌", "股灾", "泡沫", "次贷", "制裁", "衰退"]
        risk_flag = any(kw in question for kw in risk_keywords)
        
        # 检查历史重大事件（区间 + 衰减）
        event_signal = None
        event_desc = ""
        event_weight = 1.0
        
        for start, end, info in self.major_events:
            if start <= year <= end:
                year_offset = year - start
                decay = info["decay"]
                event_weight = decay[year_offset] if year_offset < len(decay) else decay[-1]
                event_signal = info["signal"]
                event_desc = f" [重大事件: {info['event']}, 影响系数: {event_weight:.1f}]"
                break
        
        # 康波周期分析（50-60年）
        kondratieff = self._analyze_kondratieff(year)
        
        # 朱格拉周期分析（7-11年）
        juglar = self._analyze_juglar(year)
        
        # 基钦周期分析（3-4年）
        kitchin = self._analyze_kitchin(year, context)
        
        # 货币周期分析
        rate_cycle = self._analyze_rate_cycle(context)
        
        # 综合信号（考虑历史事件）
        signal = self._combine_signals(kondratieff, juglar, kitchin, rate_cycle, event_signal, event_weight)
        
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
            "reasoning": signal["reasoning"] + event_desc,
            "risk_flag": risk_flag
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
        # 定义已知周期区间
        JUGLAR_CYCLES = [
            (2009, 2016, ["扩张", "扩张", "扩张", "顶部", "顶部", "收缩", "收缩"]),
            (2016, 2023, ["扩张", "扩张", "扩张", "顶部", "顶部", "收缩", "收缩"]),
            (2023, 2030, ["扩张", "扩张", "扩张", "顶部", "顶部", "收缩", "收缩"])
        ]
        
        for start, end, phases in JUGLAR_CYCLES:
            if start <= year < end:
                idx = year - start
                phase = phases[idx] if idx < len(phases) else "收缩"
                signal = "bullish" if phase == "扩张" else ("neutral" if phase == "顶部" else "bearish")
                return {
                    "cycle": "朱格拉周期",
                    "phase": phase,
                    "signal": signal,
                    "period": "7-11年"
                }
        
        # 超出已知区间
        return {
            "cycle": "朱格拉周期",
            "phase": "unknown",
            "signal": "neutral",
            "period": "7-11年"
        }
    
    def _analyze_kitchin(self, year: int, context: Dict[str, Any]) -> Dict[str, Any]:
        """基钦周期分析（库存周期）"""
        # 优先使用 PMI 数据判断
        pmi = context.get("pmi")
        pmi_signal = context.get("pmi_signal")
        
        if pmi and pmi_signal:
            phase = "补库存" if pmi_signal == "扩张" else "去库存"
            signal = "bullish" if pmi > 50 else "bearish"
            data_source = f"PMI {pmi}"
        else:
            # 使用月份精度计算
            month = context.get("month", 1)
            total_months = (year - 2020) * 12 + month
            cycle_months = total_months % 40  # 40个月周期
            
            if cycle_months < 20:
                phase = "补库存"
                signal = "bullish"
            else:
                phase = "去库存"
                signal = "bearish"
            data_source = "周期估算"
            
        return {
            "cycle": "基钦周期",
            "phase": phase,
            "signal": signal,
            "period": "3-4年",
            "data_source": data_source
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
    
    def _combine_signals(self, kondratieff, juglar, kitchin, rate_cycle, event_signal=None, event_weight=1.0) -> Dict[str, Any]:
        """综合多周期信号"""
        signals = [
            (kondratieff["signal"], 0.4),  # 康波权重最高
            (juglar["signal"], 0.25),
            (kitchin["signal"], 0.15),
            (rate_cycle["signal"], 0.2)
        ]
        
        bullish_score = sum(w for s, w in signals if s == "bullish")
        bearish_score = sum(w for s, w in signals if s == "bearish")
        
        # 历史事件影响（对称处理 + 衰减权重）
        if event_signal == "bearish":
            bearish_score *= (1.0 + event_weight)
        elif event_signal == "bullish":
            bullish_score *= (1.0 + event_weight)
        
        # 归一化 confidence 到 0-1
        total = bullish_score + bearish_score
        if total > 0:
            if bullish_score > bearish_score + 0.2:
                direction = "bullish"
                confidence = bullish_score / total
            elif bearish_score > bullish_score + 0.2:
                direction = "bearish"
                confidence = bearish_score / total
            else:
                direction = "neutral"
                confidence = 0.5
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