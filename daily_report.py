#!/usr/bin/env python3
"""
OpenMorning 定时报告推送
每天早上 9:00 推送到飞书
"""

import json
import os
from datetime import datetime, timedelta
import requests

# 配置
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PREDICTIONS_FILE = os.path.join(DATA_DIR, "predictions.json")
CASES_FILE = os.path.join(DATA_DIR, "cases.json")

# 飞书 Webhook（需要替换为实际的）
FEISHU_WEBHOOK = os.environ.get("FEISHU_WEBHOOK", "")

def load_predictions():
    """加载预测数据"""
    if os.path.exists(PREDICTIONS_FILE):
        with open(PREDICTIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"predictions": []}

def load_cases():
    """加载历史案例"""
    if os.path.exists(CASES_FILE):
        with open(CASES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"cases": []}

def get_recent_predictions(hours=24):
    """获取最近 N 小时的预测"""
    data = load_predictions()
    predictions = data.get("predictions", [])
    
    recent = []
    cutoff = datetime.now() - timedelta(hours=hours)
    
    for pred in predictions:
        try:
            created = datetime.fromisoformat(pred.get("created_at", ""))
            if created > cutoff:
                recent.append(pred)
        except:
            pass
    
    return recent

def get_pending_verifications():
    """获取待验证的预测"""
    data = load_predictions()
    predictions = data.get("predictions", [])
    
    pending = []
    now = datetime.now()
    
    for pred in predictions:
        if pred.get("status") == "pending":
            try:
                verify_date = datetime.fromisoformat(pred.get("verify_date", ""))
                if verify_date <= now:
                    pending.append(pred)
            except:
                pass
    
    return pending

def generate_daily_report():
    """生成每日报告"""
    recent = get_recent_predictions(24)
    pending = get_pending_verifications()
    cases = load_cases().get("cases", [])
    
    report = f"""# 🌅 OpenMorning 每日报告
**日期**：{datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 📊 今日预测：{len(recent)} 条
"""
    
    if recent:
        for pred in recent[-5:]:  # 最近5条
            question = pred.get("question", "")
            main_result = pred.get("predictions", [{}])[0].get("result", "")
            report += f"""
- **{question}**
  - 结论：{main_result}
  - ID：`{pred.get('id', '')}`
"""
    
    report += f"""
---

## ⏰ 待验证预测：{len(pending)} 条
"""
    
    if pending:
        for pred in pending[-3:]:
            report += f"""
- `{pred.get('id', '')}`: {pred.get('question', '')}
"""
    
    report += f"""
---

## 📈 案例库：{len(cases)} 条

数据持续积累中，越用越准。

---

*OpenMorning - 让预测成为科学*
"""
    
    return report

def send_to_feishu(report: str):
    """发送到飞书"""
    if not FEISHU_WEBHOOK:
        print("⚠️ FEISHU_WEBHOOK 未配置")
        return False
    
    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "🌅 OpenMorning 每日报告",
                    "content": [[{"tag": "text", "text": report}]]
                }
            }
        }
    }
    
    try:
        response = requests.post(FEISHU_WEBHOOK, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ 推送成功")
            return True
        else:
            print(f"❌ 推送失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 推送异常: {e}")
        return False

def main():
    """主函数"""
    print(f"📅 OpenMorning 每日报告 - {datetime.now()}")
    
    # 生成报告
    report = generate_daily_report()
    print(report)
    
    # 推送到飞书
    if FEISHU_WEBHOOK:
        send_to_feishu(report)
    else:
        print("⚠️ 未配置飞书 Webhook，仅打印报告")

if __name__ == "__main__":
    main()