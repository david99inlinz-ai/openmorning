# 🚀 推送到 GitHub 指南

## 步骤 1：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名称：`openmorning`
3. 描述：`🌅 OpenMorning - 开源预测引擎 | Open-Source Prediction Engine`
4. 可见性：**Public**（公开）
5. **不要**勾选 "Initialize this repository with a README"
6. 点击 "Create repository"

## 步骤 2：推送代码

```bash
cd /home/ubuntu/.openclaw/workspace/skills/openmorning

# 添加远程仓库（替换 YOUR_GITHUB_USERNAME 为你的 GitHub 用户名）
git remote add origin git@github.com:YOUR_GITHUB_USERNAME/openmorning.git

# 或者使用 HTTPS
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/openmorning.git

# 推送
git push -u origin main
```

## 步骤 3：验证

访问 https://github.com/YOUR_GITHUB_USERNAME/openmorning 确认代码已上传。

## 步骤 4：分享

分享仓库链接给用户使用！

---

**仓库链接格式**: `https://github.com/YOUR_GITHUB_USERNAME/openmorning`