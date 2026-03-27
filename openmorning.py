"""
OpenMorning - 开源预测引擎
主脚本
"""

import json
import os
import uuid
from datetime import datetime
from typing import Dict, Any, List

from agents.economic_cycle import EconomicCycleAgent
from agents.sentiment import SentimentAgent
from agents.metaphysics import MetaphysicsAgent
from report_generator import generate_report

class OpenMorning:
    """OpenMorning 预测引擎"""
    
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), "data")
        
        self.data_dir = data_dir
        self.predictions_file = os.path.join(data_dir, "predictions.json")
        self.cases_file = os.path.join(data_dir, "cases.json")
        
        # 初始化 Agent
        self.agents = {
            "economic_cycle": EconomicCycleAgent(),
            "sentiment": SentimentAgent(),
            "metaphysics": MetaphysicsAgent()
        }
        
        # 加载数据
        self.predictions = self._load_predictions()
        self.cases = self._load_cases()
    
    def predict(self, question: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        生成预测
        
        Args:
            question: 预测问题
            context: 上下文信息
            
        Returns:
            预测结果
        """
        if context is None:
            context = {}
        
        # 解析问题
        parsed = self._parse_question(question)
        context.update(parsed)
        
        # 全量分析（不筛选）
        analysis = {}
        for name, agent in self.agents.items():
            try:
                result = agent.analyze(context)
                analysis[name] = result
            except Exception as e:
                analysis[name] = {"error": str(e)}
        
        # 生成多方案预测
        predictions = self._generate_predictions(analysis, context)
        
        # 查找相似历史案例
        similar_cases = self._find_similar_cases(context)
        
        # 生成预测记录
        prediction_id = f"pred_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        record = {
            "id": prediction_id,
            "question": question,
            "created_at": datetime.now().isoformat(),
            "verify_date": context.get("verify_date", self._auto_verify_date(context)),
            "analysis": analysis,
            "predictions": predictions,
            "similar_cases": similar_cases,
            "status": "pending",
            "verification": None,
            "lessons": None
        }
        
        # 保存预测
        self._save_prediction(record)
        
        # 生成专业投资报告（中英双语）
        cn_report, en_report = generate_report(record)
        
        return {"report_cn": cn_report, "report_en": en_report, "prediction_id": prediction_id, "raw_data": record}
    
    def verify(self, prediction_id: str, actual_result: str) -> Dict[str, Any]:
        """
        验证预测结果
        
        Args:
            prediction_id: 预测 ID
            actual_result: 实际结果
            
        Returns:
            验证报告
        """
        # 查找预测记录
        record = None
        for pred in self.predictions.get("predictions", []):
            if pred["id"] == prediction_id:
                record = pred
                break
        
        if not record:
            return {"error": f"预测记录 {prediction_id} 不存在"}
        
        # 分析预测准确性
        verification = self._analyze_verification(record, actual_result)
        
        # 生成经验教训
        lessons = self._generate_lessons(record, verification)
        
        # 更新记录
        record["verification"] = verification
        record["lessons"] = lessons
        record["status"] = "verified"
        
        # 保存验证结果
        self._save_predictions()
        
        # 添加到历史案例库
        self._add_to_cases(record, actual_result, lessons)
        
        # 更新 Agent 权重
        self._update_agent_weights(verification)
        
        return {
            "prediction_id": prediction_id,
            "verification": verification,
            "lessons": lessons
        }
    
    def _parse_question(self, question: str) -> Dict[str, Any]:
        """解析问题，提取关键信息"""
        result = {
            "question": question,
            "year": datetime.now().year,
            "market": "A 股"
        }
        
        # 提取年份
        import re
        year_match = re.search(r'(20\d{2})', question)
        if year_match:
            result["year"] = int(year_match.group(1))
        
        # 提取市场
        if "比特币" in question or "BTC" in question:
            result["market"] = "crypto"
        elif "美股" in question:
            result["market"] = "US"
        elif "A 股" in question:
            result["market"] = "A 股"
        
        # 判断问题类型
        if "涨" in question or "上涨" in question:
            result["expectation"] = "bullish"
        elif "跌" in question or "下跌" in question:
            result["expectation"] = "bearish"
        
        return result
    
    def _generate_predictions(self, analysis: Dict, context: Dict) -> List[Dict]:
        """生成多方案预测"""
        # 综合所有 Agent 的信号
        bullish_score = 0
        bearish_score = 0
        
        for agent_name, result in analysis.items():
            if "error" in result:
                continue
            
            weight = result.get("weight", 0.2)
            signal = result.get("signal", "neutral")
            
            if signal == "bullish":
                bullish_score += weight
            elif signal == "bearish":
                bearish_score += weight
        
        # 生成三个方案
        if bullish_score > bearish_score + 0.2:
            # 乐观方案概率高
            predictions = [
                {"scenario": "乐观", "result": "上涨 50-70%", "probability": 0.5},
                {"scenario": "中性", "result": "上涨 20-40%", "probability": 0.3},
                {"scenario": "悲观", "result": "下跌 10-20%", "probability": 0.2}
            ]
        elif bearish_score > bullish_score + 0.2:
            # 悲观方案概率高
            predictions = [
                {"scenario": "乐观", "result": "上涨 10-20%", "probability": 0.2},
                {"scenario": "中性", "result": "下跌 20-40%", "probability": 0.3},
                {"scenario": "悲观", "result": "下跌 50-70%", "probability": 0.5}
            ]
        else:
            # 中性
            predictions = [
                {"scenario": "乐观", "result": "上涨 20-40%", "probability": 0.3},
                {"scenario": "中性", "result": "横盘震荡", "probability": 0.4},
                {"scenario": "悲观", "result": "下跌 20-40%", "probability": 0.3}
            ]
        
        # 添加关键因素
        key_factors = []
        for agent_name, result in analysis.items():
            if "error" in result:
                continue
            if result.get("confidence", 0) > 0.6:
                key_factors.append(f"{agent_name}: {result.get('signal', 'unknown')}")
        
        for pred in predictions:
            pred["key_factors"] = key_factors
        
        return predictions
    
    def _find_similar_cases(self, context: Dict) -> List[Dict]:
        """查找相似历史案例"""
        similar = []
        
        for case in self.cases.get("cases", []):
            # 简单匹配：康波周期阶段相同
            case_context = case.get("context", {})
            if case_context.get("kondratieff") == context.get("kondratieff_phase"):
                similar.append({
                    "year": case["time"],
                    "context": case_context,
                    "result": case["result"]
                })
        
        return similar[:3]  # 返回最多 3 个
    
    def _analyze_verification(self, record: Dict, actual_result: str) -> Dict:
        """分析验证结果"""
        # 提取实际结果的方向和幅度
        import re
        
        direction = "neutral"
        amplitude = 0
        
        if "涨" in actual_result or "上涨" in actual_result:
            direction = "bullish"
            match = re.search(r'涨 (?:了 | 幅)?(\d+)%?', actual_result)
            if match:
                amplitude = int(match.group(1))
        elif "跌" in actual_result or "下跌" in actual_result:
            direction = "bearish"
            match = re.search(r'跌 (?:了 | 幅)?(\d+)%?', actual_result)
            if match:
                amplitude = -int(match.group(1))
        
        # 对比预测
        predictions = record.get("predictions", [])
        correct_direction = False
        
        for pred in predictions:
            pred_result = pred.get("result", "")
            if direction == "bullish" and "上涨" in pred_result:
                correct_direction = True
                break
            elif direction == "bearish" and "下跌" in pred_result:
                correct_direction = True
                break
        
        return {
            "actual_result": actual_result,
            "direction": direction,
            "amplitude": amplitude,
            "correct_direction": correct_direction,
            "verified_at": datetime.now().isoformat()
        }
    
    def _generate_lessons(self, record: Dict, verification: Dict) -> Dict:
        """生成经验教训"""
        lessons = {
            "what_went_right": [],
            "what_went_wrong": [],
            "improvements": []
        }
        
        if verification.get("correct_direction"):
            lessons["what_went_right"].append("方向判断正确")
        else:
            lessons["what_went_wrong"].append("方向判断错误")
            lessons["improvements"].append("需要优化周期判断逻辑")
        
        # 分析各 Agent 的表现
        analysis = record.get("analysis", {})
        for agent_name, result in analysis.items():
            if "error" in result:
                continue
            
            signal = result.get("signal", "neutral")
            if signal == verification.get("direction"):
                lessons["what_went_right"].append(f"{agent_name} 判断正确")
            else:
                lessons["what_went_wrong"].append(f"{agent_name} 判断错误")
        
        return lessons
    
    def _update_agent_weights(self, verification: Dict):
        """更新 Agent 权重"""
        # 简化实现：根据验证结果调整
        if verification.get("correct_direction"):
            # 增加权重
            for agent in self.agents.values():
                agent.weight = min(0.5, agent.weight + 0.01)
        else:
            # 减少权重
            for agent in self.agents.values():
                agent.weight = max(0.1, agent.weight - 0.01)
    
    def _add_to_cases(self, record: Dict, actual_result: str, lessons: Dict):
        """添加到历史案例库"""
        case = {
            "id": record["id"],
            "time": datetime.now().year,
            "question": record["question"],
            "context": {
                "kondratieff": "回升期",  # 简化
                "juglar": "扩张期",
                "rate_cycle": "降息"
            },
            "prediction": record["predictions"][0]["result"],
            "result": actual_result,
            "analysis": lessons.get("what_went_right", []) + lessons.get("what_went_wrong", []),
            "lessons": str(lessons)
        }
        
        self.cases.setdefault("cases", []).append(case)
        self._save_cases()
    
    def _auto_verify_date(self, context: Dict) -> str:
        """自动设置验证日期"""
        year = context.get("year", datetime.now().year)
        return f"{year}-12-31"
    
    def _load_predictions(self) -> Dict:
        """加载预测记录"""
        if os.path.exists(self.predictions_file):
            with open(self.predictions_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"predictions": [], "metadata": {"version": "1.0.0"}}
    
    def _load_cases(self) -> Dict:
        """加载历史案例"""
        if os.path.exists(self.cases_file):
            with open(self.cases_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"cases": [], "metadata": {"version": "1.0.0"}}
    
    def _save_prediction(self, record: Dict):
        """保存预测记录"""
        self.predictions.setdefault("predictions", []).append(record)
        self._save_predictions()
    
    def _save_predictions(self):
        """保存所有预测"""
        with open(self.predictions_file, "w", encoding="utf-8") as f:
            json.dump(self.predictions, f, ensure_ascii=False, indent=2)
    
    def _save_cases(self):
        """保存历史案例"""
        with open(self.cases_file, "w", encoding="utf-8") as f:
            json.dump(self.cases, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    om = OpenMorning()
    
    # 测试预测
    result = om.predict("2026 年 A 股会涨吗？", {"rate_trend": "降息"})
    print(json.dumps(result, indent=2, ensure_ascii=False))