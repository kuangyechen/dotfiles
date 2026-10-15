# Setup：在目标设备建立个人环境

适用于用户明确要求配置当前设备。覆盖个人 shell、CLI、编辑器及按需选择的 Mac 应用。
系统安全策略、业务服务、默认登录 shell、启动服务和 macOS defaults 需要用户提出相应需求。
Agent session 已在目标设备运行，不做 SSH 编排。

## 1. 建立本机事实

1. 查看系统、架构、用户、HOME、PATH 和权限。macOS 支持 Apple Silicon／Intel；
   Linux 覆盖 Ubuntu／Debian，区分 x86_64 与 aarch64，并检查发行物的 libc 要求。
2. 阅读组件目录。记录主仓库及已初始化子模块的 Git 状态，保留已有修改；
   不运行 `git submodule update --remote`。
3. 若缺少 uv，按其官方文档安装；macOS 可用已有 Homebrew。缺少 Homebrew 时，
   按 https://brew.sh 完成前置条件。Linux 不安装 Homebrew。
4. 运行 `uv run dots inspect --json`。尚无本机选择时使用
   `uv run dots inspect --profile mac --json` 或 `--profile linux-server`。

## 2. 选择组件并安装

- 默认是基础 shell、CLI 和编辑器。结合用户用途选择可选组件，不整体恢复历史 Brewfile。
  已有 `.dotter/local.toml` 时先理解当前选择，新默认组合不直接替换它。
- `uv run dots profile mac --with zed` 预览组合。重复 `--with` 添加组件，`--without` 排除默认项。
  完整 Oh My Zsh 使用 `--without zsh --with oh-my-zsh`；依赖会一并加入，互斥组件不能一起选。
- 检查组件的 `binaries` 和原生安装状态。安装指导是给 agent 的数据，不是批量执行脚本。
  指向上游时读取当前官方安装说明；保留符合需求的已有安装，不因 setup 自动升级或卸载整机软件。
- Linux 优先 apt，无合适包时用上游预编译发行物，不为基础 CLI 默认安装 Rust。
  检查架构和完整 runtime，例如 Helix 不能只复制 `hx`。
- `fd-find`／`bat` 可能提供 `fdfind`／`batcat`。仅在对应命令缺失且目标不冲突时，
  在 `~/.local/bin/` 建立 `fd`／`bat` 链接并验证 PATH。
- 默认 Fish 不依赖 Fisher。选中插件组件时在 Fish 内安装并检查插件列表。
- 需要私有配置或主题时，仅初始化所需子模块，使用父仓库记录的 commit。
  无访问权限时继续通用部分，将该组件列为阻塞。
- Zed 扩展由所选 settings 中的 `auto_install_extensions` 声明。先部署配置，再启动 Zed
  自动恢复扩展；通过扩展面板或安装目录核对完成情况。无需复制扩展代码、下载的语言服务器或缓存。

## 3. 比较、备份和部署

1. 将生成的组合先保存到 `.local/` 临时文件，与已有本机选择比较，保留机器级覆盖。
   备份原选择后再更新 `.dotter/local.toml`，不提交本机文件。
2. 再运行 inspect，并审阅 `previous_deployments`。Dotter 更换选择时会处理旧缓存，
   将退出管理的文件也必须纳入比较。
3. 已链接到 repo 的文件先审阅 Git diff。独立普通文件需比较并合并可复用内容；
   没有共同基线时不凭修改时间决定保留哪边，无法取舍才展示具体差异询问。
4. 将要替换的目标及已有 Dotter 本机配置／缓存备份到 `.local/backups/<UTC时间>/`，
   保留权限和链接本身。HOME 内按相对路径保存，其它路径放 `absolute/`，记录原路径与备份对应关系。
   验证备份后将已解决冲突的目标移开，不覆盖同名旧备份。
5. 先运行 `dotter deploy --dry-run`，确认部署和旧链接移除符合预期，再运行
   `dotter deploy --verbose`，不用 blanket `--force`。两次执行之间文件若被应用重写，重新比较。

默认使用显式软链接。模板、条件和 owner 会被检查工具标为 `manual`，需结合 Dotter 处理，
不能反向复制渲染产物覆盖模板。鉴权文件不部署；若旧设备仍将登录态链接到 repo，
先将其保存在设备本地并恢复成普通文件，再退出旧映射，不将内容写入报告。

## 4. 本地覆盖和验证

- Git 身份放 `~/.config/git/local.gitconfig`，由共享配置 include。继承设备已有有效身份，
  缺少时再询问，不使用系统推断的姓名和邮箱。
- Fish 的本地覆盖是 `~/.config/fish/local_env.fish`；精简 Zsh 使用
  `~/.config/local_env` 和 `~/.config/zsh/local.zsh`。本地覆盖最后读取，
  不跨设备复制 token，不假定存在 `en_US.UTF-8` locale。
- 验证所选命令与版本，检查 `fish --no-execute`、`zsh -n` 及 TOML 语法；
  用交互 shell 检查初始化，检查 `hx --health` 和 Zellij 的实际配置解析。
  GUI 组件检查安装和配置加载；启用服务、申请系统权限属于单独需求。
- 最后重跑 inspect，说明已完成项、本机差异、可选项和阻塞项。失败后继续独立步骤，
  修复后重跑检测，不盲目重装。恢复时先检查新修改，再按备份清单逐项恢复文件和本机选择。
