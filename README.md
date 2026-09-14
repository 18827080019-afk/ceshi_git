# AI 学习项目

当前进度：阶段 2，2026.8 第三周，Agent 生命周期。主要在 VS Code 中学习，每次完成优化后保留独立 commit，用于回顾学习路径。

## 目录

- `AI学习/阶段2/2026.8第三周 生命周期(学习修改内容)/`：当前代码、models 模块和原有测试脚本。
- `AI学习/建议/`：旧项目全部 29 份文本笔记，保留来源分类和原文件名，包含带日期但没有标准文本扩展名的笔记。
- `.vscode/`：当前项目的解释器、调试入口和扩展建议。
- `requirements.txt`：当前代码需要的依赖；OpenAI SDK 版本与源项目环境一致。
- `.env.example`：可提交的配置模板；真实配置仅放本地 `.env`。

原项目保留原样。旧阶段代码、聊天 JSON、无关脚本、旧虚拟环境和缓存未迁入。当前阶段的 `runtime生命周期` 笔记已归入建议目录。

## 在 VS Code 中继续学习

用 VS Code 打开本项目根目录 `ceishi_git`，或打开本地 `github copilot.code-workspace`。首次使用时，在项目根目录的 PowerShell 终端执行：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

通过“Python: Select Interpreter”选择 `.venv\Scripts\python.exe`。本机迁移时已保存本地 `.env`；新电脑上先复制 `.env.example` 为 `.env`，填入自己的 API 密钥，不要覆盖已有配置。

调试入口已配置。当前代码仍有下述原有待办，修复后可按 F5，选择“当前学习：Agent 生命周期”，或执行：

```powershell
.\.venv\Scripts\python.exe "AI学习\阶段2\2026.8第三周 生命周期(学习修改内容)\main.py"
```

输入 `exit` 退出。入口会从项目根目录加载 `.env`；实际对话会调用 DeepSeek API。

### 当前学习待办与迁移验证

- 原有 `main.py` 向 `Agent` 传入 8 个参数，但 `Agent.__init__` 只接收 6 个参数（均不含 `self`）。启动验证停在此处，报 `TypeError`，尚不能进行对话。
- 下一次优化可从入口与生命周期接口的衔接开始，并检查输出记录是否应使用每轮创建的 `agent.trace`。本次迁移保留业务逻辑原状。
- 已验证：29 份原始笔记逐字节一致、16 个未修改的代码文件与源文件一致、17 个 Python 文件语法检查、VS Code JSON 格式、依赖完整性、原执行器脚本三种场景。
- 入口已加载新环境依赖并执行到 `Agent` 初始化；未发起实际 API 请求。

原有执行器演示可离线运行，覆盖正常参数、错误参数和不存在工具三种情况：

```powershell
.\.venv\Scripts\python.exe "AI学习\阶段2\2026.8第三周 生命周期(学习修改内容)\test_executor.py"
```

## 每次优化如何留档

先确认优化计划，再修改、验证并创建一次本地 commit。提交标题写本次学习主题，正文记录“改动、原因、验证”。在 VS Code 源代码管理中查看历史与差异，或运行：

```powershell
git log --oneline
git show <提交编号>
```

后续按需执行 `git push` 同步到 GitHub。详细工作约定见 `AGENTS.md`。
