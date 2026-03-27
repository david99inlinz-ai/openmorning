# 🚀 发布到 GitHub 指南

## 方法 1：手动创建（推荐）

1. 打开 https://github.com/new

2. 填写信息：
   - Repository name: `openmorning`
   - Description: `OpenMorning - 开源预测引擎 | 结合经济学周期、市场情绪、玄学分析的持续学习预测系统`
   - 选择 **Public**
   - **不要** 勾选 "Add a README file"
   - **不要** 勾选 ".gitignore"
   - **不要** 选择 License

3. 点击 "Create repository"

4. 复制仓库 URL（SSH 或 HTTPS）

5. 在终端执行：

```bash
cd /home/ubuntu/.openclaw/workspace/skills/openmorning

# 如果使用 SSH
git remote set-url origin git@github.com:openclaw/openmorning.git

# 如果使用 HTTPS
git remote set-url origin https://github.com/openclaw/openmorning.git

# 推送
git push -u origin main
```

## 方法 2：使用 GitHub CLI

```bash
# 安装 gh（如果未安装）
sudo apt-get install gh  # Ubuntu/Debian
brew install gh          # macOS

# 登录
gh auth login

# 创建并推送
gh repo create openclaw/openmorning --public --source=/home/ubuntu/.openclaw/workspace/skills/openmorning --push
```

## 方法 3：使用 curl 创建

```bash
# 替换 YOUR_GITHUB_TOKEN 为你的 GitHub Personal Access Token
curl -X POST https://api.github.com/user/repos \
  -H "Authorization: token YOUR_GITHUB_TOKEN" \
  -d '{"name":"openmorning","description":"OpenMorning - 开源预测引擎","private":false}'

# 然后推送
cd /home/ubuntu/.openclaw/workspace/skills/openmorning
git remote set-url origin https://github.com/openclaw/openmorning.git
git push -u origin main
```

## 获取 GitHub Personal Access Token

1. 打开 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 填写 Note: `OpenMorning Deploy`
4. 勾选权限：`repo` (Full control of private repositories)
5. 点击 "Generate token"
6. **复制 token 并保存**（只显示一次）

## 验证发布

发布后访问：https://github.com/openclaw/openmorning

确认文件都在：
- ✅ SKILL.md
- ✅ openmorning.py
- ✅ agents/
- ✅ data/
- ✅ README.md
- ✅ LICENSE

## 使用方式

发布后，用户可以通过以下方式发现和使用：

1. **OpenClaw 内**：`/openmorning [问题]`
2. **GitHub**：https://github.com/openclaw/openmorning
3. **直接运行**：`python openmorning.py`

---

**🌅 让预测成为科学，让学习持续进化。**