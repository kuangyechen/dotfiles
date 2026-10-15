# Agent instructions

根据用户任务选择流程：

- 在本机建立或修复环境：先读 `workflows/setup.md`。
- 将本机配置／软件选择收回仓库：先读 `workflows/sync.md`。
- 修改仓库代码或文档：直接完成开发，不因此执行设备 setup 或部署。

## 职责与事实来源

- `catalog.toml` 记录组件用途、支持平台、安装指导、默认组合和关联的 Dotter 组。
- `.dotter/` 是配置路径映射的唯一来源。不要在代码或文档中再维护一张映射表。
- `dots/` 保存配置。通用配置留主仓库，个人配置留 `dots/private-dotfiles/` 子模块。
- `src/dotfiles_tools/` 提供轻量工具；安装、配置取舍和合并由 agent 按工作流处理。
- `legacy/` 是归档，不执行其中的脚本，不从新包导入旧安装器。
- `raycast_scripts/` 保持独立项目；根项目不将其注册为 uv workspace member。

## 操作约定

- 先检查主仓库与子模块已有修改，保留用户工作。不使用 reset、checkout 或 blanket copy 清空差异。
- 用 `uv run dots profile ...` 查看组合，`uv run dots inspect --json` 检查路径和状态。
- 常规、可判断的任务连续完成；仅对缺失的用途信息或无法判断的冲突取舍询问。
- 先比较、备份，再部署。Dotter 的 `--force` 会覆盖 `--dry-run`；不要组合使用，也不要批量强制部署。
- 密钥、token、登录态和 shell 历史只留设备本地，不纳入映射、报告内容或提交。
- 本机选择、备份和临时报告放 `.local/` 或已忽略的 Dotter 本机文件中。
- 软件清单反映长期需要的能力。不要用整机包列表覆盖清单，不把依赖包自动加入默认组合。
- 用户只要求 sync 时，默认形成本地 diff；未明确要求时不 commit／push。
- 安装失败或缺少权限时记录具体阻塞，继续独立步骤，不将跳过的必需项报告为成功。

## 开发与验证

- 固定 Python 3.12.15，通过 uv 管理；数据模型与配置校验使用 Pydantic，避免 dataclass。
- CLI 使用 Typer，入口测试使用 `typer.testing.CliRunner`，不使用 argparse。
- 仓库子目录运行应能发现根目录；测试通过 CLI 的 `--repo` 和 `inspect --home` 使用临时目录。
- 单元测试使用 pytest，修改辅助工具后运行 `uv run pytest`。
- 格式和静态检查使用 Ruff：`uv run ruff check .` 和 `uv run ruff format --check .`。
- 需要日志时使用 Loguru；当前工具直接输出检查结果，不添加日志依赖。
- 修改打包配置后运行 `uv build`，确认 legacy、配置内容和私有子模块没有进入产物。
- Dotter 部署验证使用临时 HOME 和独立缓存，不在当前用户 HOME 执行真实部署。
- 验证报告区分代码测试、本机 smoke test 和尚未执行的跨平台验证。
