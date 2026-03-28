"""
OpenMorning - 开源预测引擎
主脚本
"""

import json
import os
import uuid
import subprocess
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
        
        # 加载历史权重
        self._load_agent_weights()
    
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
        
        # 🔥 新增：搜索实时数据
        market_data = self._fetch_market_data(question, context)
        context.update(market_data)
        
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
        
        # 生成 PDF 并保存
        pdf_path = self._generate_and_save_pdf(cn_report, prediction_id)
        
        return {"report_cn": cn_report, "report_en": en_report, "prediction_id": prediction_id, "pdf_path": pdf_path, "raw_data": record}
    
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
        self._update_agent_weights(record, verification)
        
        return {
            "prediction_id": prediction_id,
            "verification": verification,
            "lessons": lessons
        }
    
    def _parse_question(self, question: str) -> Dict[str, Any]:
        """解析问题，提取关键信息"""
        import re
        
        result = {
            "question": question,
            "year": datetime.now().year,
            "market": "A股",
            "expectation": "unknown"  # 默认值
        }
        
        # 提取年份（取最大值）
        year_matches = re.findall(r'(20\d{2})', question)
        if year_matches:
            result["year"] = max(int(y) for y in year_matches)
        
        # 提取市场（支持无空格）
        market_map = {
            "比特币": "crypto", "BTC": "crypto", "crypto": "crypto",
            "美股": "US", "纳斯达克": "US", "标普": "US",
            "A股": "A股", "A 股": "A股", "沪深": "A股",
            "港股": "港股", "恒生": "港股"
        }
        for keyword, market_type in market_map.items():
            if keyword in question:
                result["market"] = market_type
                break
        
        # 判断问题类型（避免误匹配）
        if re.search(r'(?<!不)(?<!会)涨(?!跌)', question) or "上涨" in question:
            result["expectation"] = "bullish"
        elif re.search(r'(?<!不)(?<!会)跌(?!涨)', question) or "下跌" in question:
            result["expectation"] = "bearish"
        elif "震荡" in question or "横盘" in question:
            result["expectation"] = "neutral"
        
        return result
    
    def _generate_predictions(self, analysis: Dict, context: Dict) -> List[Dict]:
        """生成多方案预测（数据驱动）"""
        # 市场波动率配置
        VOLATILITY = {
            "A股": (15, 35),
            "crypto": (40, 100),
            "US": (10, 25),
            "港股": (20, 40)
        }
        
        # 综合所有 Agent 的信号（加入置信度）
        weighted_score = 0
        total_weight = 0
        
        for agent_name, result in analysis.items():
            if "error" in result:
                continue
            
            weight = result.get("weight", 0.2)
            confidence = result.get("confidence", 0.5)
            signal = result.get("signal", "neutral")
            
            signal_value = {"bullish": 1, "bearish": -1, "neutral": 0}.get(signal, 0)
            weighted_score += weight * confidence * signal_value
            total_weight += weight
        
        # 归一化到 [-1, 1]
        normalized = weighted_score / max(total_weight, 0.01)
        
        # 获取市场波动率
        market = context.get("market", "A股")
        vol_range = VOLATILITY.get(market, (15, 35))
        
        # 根据信号强度动态生成概率和幅度
        if normalized > 0.15:  # 偏多
            bullish_prob = 0.3 + normalized * 0.3  # [0.35, 0.6]
            neutral_prob = 0.4 - normalized * 0.2
            bearish_prob = 1 - bullish_prob - neutral_prob
            
            predictions = [
                {"scenario": "乐观", "result": f"上涨 {vol_range[1]-10}-{vol_range[1]}%", "probability": round(bullish_prob, 2)},
                {"scenario": "中性", "result": f"上涨 {vol_range[0]}-{vol_range[0]+10}%", "probability": round(neutral_prob, 2)},
                {"scenario": "悲观", "result": f"下跌 {vol_range[0]//2}-{vol_range[0]}%", "probability": round(bearish_prob, 2)}
            ]
        elif normalized < -0.15:  # 偏空
            bearish_prob = 0.3 + abs(normalized) * 0.3
            neutral_prob = 0.4 - abs(normalized) * 0.2
            bullish_prob = 1 - bearish_prob - neutral_prob
            
            predictions = [
                {"scenario": "乐观", "result": f"上涨 {vol_range[0]//2}-{vol_range[0]}%", "probability": round(bullish_prob, 2)},
                {"scenario": "中性", "result": f"下跌 {vol_range[0]}-{vol_range[0]+10}%", "probability": round(neutral_prob, 2)},
                {"scenario": "悲观", "result": f"下跌 {vol_range[1]-10}-{vol_range[1]}%", "probability": round(bearish_prob, 2)}
            ]
        else:  # 中性
            predictions = [
                {"scenario": "乐观", "result": f"上涨 {vol_range[0]}-{vol_range[0]+10}%", "probability": 0.3},
                {"scenario": "中性", "result": "横盘震荡", "probability": 0.4},
                {"scenario": "悲观", "result": f"下跌 {vol_range[0]}-{vol_range[0]+10}%", "probability": 0.3}
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
        """查找相似历史案例（多维度评分）"""
        scored = []
        
        for case in self.cases.get("cases", []):
            case_context = case.get("context", {})
            score = 0
            
            # 多维度匹配
            if case_context.get("kondratieff") == context.get("kondratieff_phase"):
                score += 3  # 康波权重高
            if case_context.get("juglar") == context.get("juglar_phase"):
                score += 2
            if case_context.get("rate_cycle") == context.get("rate_cycle"):
                score += 1
            if case_context.get("sentiment") == context.get("sentiment"):
                score += 1
            
            if score > 0:
                scored.append((score, {
                    "year": case["time"],
                    "context": case_context,
                    "result": case["result"],
                    "similarity_score": score
                }))
        
        # 按相似度排序
        scored.sort(key=lambda x: -x[0])
        return [c for _, c in scored[:3]]
    
    def _analyze_verification(self, record: Dict, actual_result: str) -> Dict:
        """分析验证结果"""
        # 提取实际结果的方向和幅度
        import re
        
        direction = "neutral"
        amplitude = 0.0  # 初始化默认值
        
        # 修复正则表达式，支持小数
        pattern_up = r'(?:涨了?|上涨|涨幅)[约近]?(\d+(?:\.\d+)?)%?'
        pattern_down = r'(?:跌了?|下跌|跌幅)[约近]?(\d+(?:\.\d+)?)%?'
        
        match = re.search(pattern_up, actual_result)
        if match:
            direction = "bullish"
            amplitude = float(match.group(1))
        else:
            match = re.search(pattern_down, actual_result)
            if match:
                direction = "bearish"
                amplitude = -float(match.group(1))
        
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
                lessons["what_went_wrong"].append(f"{agent_name} 执行出错: {result['error']}")
                lessons["improvements"].append(f"修复 {agent_name} 的错误处理")
                continue
            
            signal = result.get("signal", "neutral")
            if signal == verification.get("direction"):
                lessons["what_went_right"].append(f"{agent_name} 判断正确")
            elif signal != "neutral":
                lessons["what_went_wrong"].append(f"{agent_name} 判断错误")
                lessons["improvements"].append(f"优化 {agent_name} 的信号生成逻辑")
        
        return lessons
    
    def _update_agent_weights(self, record: Dict, verification: Dict):
        """更新 Agent 权重（精细化调整 + 归一化）"""
        actual_direction = verification.get("direction", "neutral")
        
        # 从当前验证的预测记录中获取各 Agent 的信号
        analysis = record.get("analysis", {})
        
        # 逐个评估 Agent 的准确性
        for agent_name, agent in self.agents.items():
            agent_result = analysis.get(agent_name, {})
            agent_signal = agent_result.get("signal", "neutral")
            
            old_weight = agent.weight
            
            # 判断该 Agent 是否预测正确
            if agent_signal == actual_direction:
                # 预测对了 → 增加权重
                agent.weight = min(0.5, agent.weight + 0.02)
                print(f"✅ {agent_name} 预测正确，权重 {old_weight:.3f} → {agent.weight:.3f}")
            elif agent_signal != "neutral" and actual_direction != "neutral":
                # 预测错了（且不是中性）→ 减少权重
                agent.weight = max(0.05, agent.weight - 0.02)
                print(f"❌ {agent_name} 预测错误，权重 {old_weight:.3f} → {agent.weight:.3f}")
            else:
                # 中性或方向不明确 → 不惩罚
                print(f"⚖️ {agent_name} 中性，权重保持 {agent.weight:.3f}")
        
        # 归一化权重
        total = sum(a.weight for a in self.agents.values())
        if total > 0:
            for agent in self.agents.values():
                agent.weight = round(agent.weight / total, 4)
        
        # 保存权重到文件
        self._save_agent_weights()
    
    def _add_to_cases(self, record: Dict, actual_result: str, lessons: Dict):
        """添加到历史案例库"""
        # 从 record 中提取真实的 context
        analysis = record.get("analysis", {})
        
        # 提取各周期的实际阶段
        context = {}
        if "economic_cycle" in analysis:
            ec_analysis = analysis["economic_cycle"].get("analysis", {})
            context["kondratieff"] = ec_analysis.get("kondratieff", {}).get("phase", "unknown")
            context["juglar"] = ec_analysis.get("juglar", {}).get("phase", "unknown")
            context["rate_cycle"] = ec_analysis.get("rate_cycle", {}).get("trend", "unknown")
        
        if "sentiment" in analysis:
            context["sentiment"] = analysis["sentiment"].get("label", "unknown")
        
        # 提取主要预测（最高概率）
        predictions = record.get("predictions", [])
        main_prediction = max(predictions, key=lambda p: p.get("probability", 0)) if predictions else {}
        
        case = {
            "id": record["id"],
            "time": datetime.now().isoformat(),  # 完整时间
            "question": record["question"],
            "context": context,
            "prediction": main_prediction.get("result", "unknown"),
            "result": actual_result,
            "analysis": lessons.get("what_went_right", []) + lessons.get("what_went_wrong", []),
            "lessons": lessons  # 直接存字典
        }
        
        self.cases.setdefault("cases", []).append(case)
        self._save_cases()
    
    def _fetch_market_data(self, question: str, context: Dict) -> Dict[str, Any]:
        """搜索实时市场数据"""
        try:
            # 构建搜索查询
            market = context.get("market", "A股")
            year = context.get("year", datetime.now().year)
            
            queries = [
                f"{market} {year} 市场情绪 恐惧贪婪指数",
                f"{market} PMI 库存 经济数据",
                f"{year} 利率 货币政策"
            ]
            
            # 调用 super-search（通过 subprocess）
            search_results = []
            for query in queries[:2]:  # 只搜前2个，省时间
                try:
                    result = subprocess.run(
                        ["node", "../super-search/search.js", query],
                        capture_output=True,
                        text=True,
                        timeout=15,
                        cwd=os.path.dirname(__file__) or "."
                    )
                    if result.returncode == 0:
                        search_results.append(result.stdout)
                except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                    print(f"⚠️ 搜索失败 [{query}]: {e}")
                    continue
            
            # 解析搜索结果，提取关键数据
            extracted = self._extract_data_from_search(search_results)
            return extracted
            
        except Exception as e:
            # 搜索失败不影响主流程
            return {"search_error": str(e)}
    
    def _extract_data_from_search(self, results: List[str]) -> Dict[str, Any]:
        """从搜索结果提取数据"""
        data = {}
        
        combined = " ".join(results)
        
        # 提取恐惧贪婪指数
        import re
        fear_match = re.search(r'恐惧.*?(\d{1,2})', combined)
        if fear_match:
            data["fear_index"] = int(fear_match.group(1))
        
        # 提取利率趋势
        if "降息" in combined or "宽松" in combined:
            data["rate_trend"] = "降息"
        elif "加息" in combined or "紧缩" in combined:
            data["rate_trend"] = "加息"
        
        # 提取 PMI
        pmi_match = re.search(r'PMI.*?(\d{2}\.\d)', combined)
        if pmi_match:
            pmi = float(pmi_match.group(1))
            data["pmi"] = pmi
            data["pmi_signal"] = "扩张" if pmi > 50 else "收缩"
        
        return data
    
    def _auto_verify_date(self, context: Dict) -> str:
        """自动设置验证日期"""
        year = context.get("year", datetime.now().year)
        return f"{year}-12-31"
    
    def _save_agent_weights(self):
        """保存 Agent 权重到文件"""
        weights_file = os.path.join(self.data_dir, "agent_weights.json")
        weights = {
            name: {
                "weight": agent.weight,
                "updated_at": datetime.now().isoformat()
            }
            for name, agent in self.agents.items()
        }
        with open(weights_file, "w", encoding="utf-8") as f:
            json.dump(weights, f, ensure_ascii=False, indent=2)
    
    def _load_agent_weights(self):
        """加载 Agent 权重"""
        weights_file = os.path.join(self.data_dir, "agent_weights.json")
        if os.path.exists(weights_file):
            with open(weights_file, "r", encoding="utf-8") as f:
                weights = json.load(f)
                for name, data in weights.items():
                    if name in self.agents:
                        self.agents[name].weight = data["weight"]
    
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
    
    def _generate_and_save_pdf(self, report_content: str, prediction_id: str) -> str:
        """生成 PDF 并保存到 workspace"""
        workspace_dir = "/home/ubuntu/.openclaw/workspace"
        reports_dir = os.path.join(workspace_dir, "openmorning_reports")
        os.makedirs(reports_dir, exist_ok=True)
        
        pdf_filename = f"{prediction_id}.pdf"
        pdf_path = os.path.join(reports_dir, pdf_filename)
        md_path = pdf_path.replace('.pdf', '.md')
        
        # 保存 markdown
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        # 生成 PDF
        try:
            result = subprocess.run(
                ['pandoc', md_path, '-o', pdf_path, '--pdf-engine=xelatex',
                 '-V', 'CJKmainfont=Noto Sans CJK SC', '-V', 'geometry:margin=1in'],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode == 0 and os.path.exists(pdf_path):
                return pdf_path
            else:
                print(f"PDF 生成失败：{result.stderr[:200]}")
                return md_path
        except Exception as e:
            print(f"pandoc 调用失败：{e}")
            return md_path


if __name__ == "__main__":
    import sys
    
    om = OpenMorning()
    
    if len(sys.argv) > 2 and sys.argv[1] == "predict":
        question = " ".join(sys.argv[2:])
        result = om.predict(question)
        
        # 输出结果（飞书会自动捕获）
        pdf_path = result.get("pdf_path")
        prediction_id = result.get("prediction_id")
        
        if pdf_path and os.path.exists(pdf_path):
            print(f"📊 OpenMorning 投资研究报告")
            print(f"**预测 ID**: {prediction_id}")
            print(f"**文件**: {pdf_path}")
            print(f"\n{result.get('report_cn', '')[:1500]}")
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # 测试预测
        result = om.predict("2026 年 A 股会涨吗？", {"rate_trend": "降息"})
        print(json.dumps(result, indent=2, ensure_ascii=False))