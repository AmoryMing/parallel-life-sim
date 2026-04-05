# Parallel Life Simulator -- Your Life's What-Ifs

**Monte Carlo simulation of life trajectories based on real decision variables.**

基于真实人生决策变量的蒙特卡洛人生轨迹模拟器。

---

## What is this / 这是什么

Parallel Life Simulator lets you explore the roads not taken. Feed it your real personality, experiences, and life conditions -- it runs Monte Carlo simulations to show how your life might have unfolded under different choices.

平行人生模拟器让你探索那些"没走的路"。输入你的真实性格、经历和生活条件，它会通过蒙特卡洛模拟，展示你在不同选择下的人生可能走向。

### Core Parameters / 核心参数

- **34 social variables** across 5 layers: personal, interpersonal, social, national, international
- **67 life events** as structured simulation templates
- **5 层 34 个社会变量** + **67 个人生事件模板**

### What makes it different / 差异化

[Simile](https://simile.ai/) raised $100M to prove the life simulation market exists. Their approach: fictional characters in game-like worlds.

Ours: **simulate YOUR life, with YOUR real choices.** Not a game character -- you.

Simile 拿了 1 亿美金融资，证明了"人生模拟"这个市场真实存在。他们的路线是虚构角色 + 游戏世界。

我们的路线：**模拟你自己的人生，基于你真实的选择。** 不是游戏角色，是你。

## Quick Start / 快速开始

```bash
# Clone
git clone https://github.com/AmoryMing/parallel-life-sim.git
cd parallel-life-sim

# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure API key (any OpenAI-compatible LLM)
export DASHSCOPE_API_KEY="your-api-key-here"

# Run
python3 app.py
```

Open http://localhost:5678 in your browser.

浏览器打开 http://localhost:5678 即可使用。

## How it works / 使用流程

1. **Know you / 认识你** -- Chat with the AI interviewer, it builds your personality profile
2. **Your baseline / 你的原本** -- Review the AI-generated persona card and 34-variable panel
3. **Parallel lives / 平行人生** -- Pick a simulation preset (realistic / pessimistic / career-focused) and run
4. **Branch / 分支** -- Fork from any point, change one condition, re-simulate

## Tech Stack / 技术栈

| Component | Technology |
|-----------|------------|
| Backend | Python (Flask) |
| Frontend | Vanilla HTML/CSS/JS |
| AI Engine | Qwen 3.5-plus (any OpenAI-compatible API) |
| Simulation | Monte Carlo method |
| Design | Light theme, Notion + Claude aesthetic |

**Version: v2.1.1**

## Roadmap / 路线图

- [x] Conversational personality profiling / 对话式人格采集
- [x] AI persona generation / AI 人格档案生成
- [x] 5-layer variable system / 5 层变量系统
- [x] Life simulation with streaming output / 人生模拟（流式输出）
- [x] Branch system / 分支系统
- [ ] Step-by-step simulation engine (pause / dialogue / rewind) / 步进式仿真引擎
- [ ] Layered memory system / 分层记忆系统
- [ ] Knowledge graph visualization / 知识图谱可视化
- [ ] Talk to any-age version of yourself / 跟任意年龄的"世另我"对话
- [ ] Social event library (59 structured templates) / 社会事件库
- [ ] Multi-version cross-dialogue / 多版本互相对话

## License / 许可证

[Apache 2.0](LICENSE)

Copyright 2026 Ming Mu (AmoryMing)
