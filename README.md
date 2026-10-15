# Dotfiles

由 AI agent 维护的个人工作环境，支持新 Mac 和 Ubuntu／Debian server。

在目标设备上 clone 仓库、进入目录并启动 agent session，然后直接描述任务：

> 配置这台新 Mac，使用默认环境，并加上 Zed 和 Aerospace。
>
> 把本机配置和软件选择同步回仓库，保留这台设备特有的设置。

Agent 从 [AGENTS.md](AGENTS.md) 进入 [setup](workflows/setup.md) 或
[sync](workflows/sync.md) 流程。软件和默认组合记录在
[catalog.toml](catalog.toml)，配置路径只在 Dotter 中维护。

## 仓库组成

- `src/dotfiles_tools/`：状态检查和配置选择工具，命令名 `dots`。
- `dots/`：实际配置；`dots/private-dotfiles/` 保存个人配置。
- `.dotter/`：配置映射；`local.toml` 和缓存仅留本机。
- `workflows/`：agent 的操作流程和判断依据。
- `raycast_scripts/`：独立项目，保留自己的 Python 环境。
- `legacy/`：旧安装器和 Mackup 快照，仅作历史参考。

## 辅助命令

安装 [uv](https://docs.astral.sh/uv/getting-started/installation/) 后运行；
uv 会按 `.python-version` 使用 **Python 3.12.15**，不依赖系统 Python。
项目支持 Python 3.12 系列，使用 Pydantic 校验组件目录和配置模型。

```sh
uv run dots profile mac
uv run dots profile linux-server
uv run dots profile mac --with zed --with aerospace
uv run dots profile mac --without zsh --with oh-my-zsh

uv run dots inspect
uv run dots inspect --json
uv run dots inspect --profile linux-server --home /tmp/example-home
```

`profile` 只向标准输出生成 Dotter 配置，不保存文件。Agent 比较已有本机选择后，
再将所需组合保存为 `.dotter/local.toml`；默认软件组合仅在组件目录维护。

`inspect` 默认检查现有 `local.toml`，缺失时也支持 Dotter 的 hostname 配置；
`--profile` 用于预览某个默认组合。它不写配置、部署或缓存，也不输出文件内容。
uv 首次运行可能安装 Python 并创建项目虚拟环境。

检查结果区分已链接、独立文件相同／不同、缺少源文件、目标缺失、错误链接、
类型冲突和需要手动处理的模板。目录内额外文件会单独列出，不推断为待删除文件。
`previous_deployments` 表示缓存中不属于当前选择的旧部署，部署前应审阅。
成功完成检查返回 `0`，配置错误或无法完成检查返回 `2`；`0` 不表示设备没有差异。
JSON 包含路径和 Git 状态，仍可能涉及个人信息，应留在本机。

## 开发

```sh
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv build
```

工具按职责分为 `cli`、`catalog`、`dotter`、`inspect`，CLI 使用 Typer，
不执行安装命令或自动合并。
新增组件先更新目录，只有存在需要可靠复用的机械操作时才增加代码。

旧 Brewfile 和已有配置源文件保留原路径，以兼容当前设备链接。
迁移关系见 [legacy/README.md](legacy/README.md)。
