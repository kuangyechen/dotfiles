# Setup: configure the target device

Use when the user requests setup on the current device. Cover personal shells, CLI tools,
editors, and optional Mac apps. System security, business services, login-shell changes,
startup services, and macOS defaults require a corresponding user request.
The agent session runs on the target device; SSH orchestration is out of scope.

## 1. Inspect the device

1. Identify OS, architecture, user, HOME, PATH, and permissions. Support Apple Silicon/Intel Macs
   and Ubuntu/Debian on x86_64/aarch64. Check downloaded binaries' libc requirements.
2. Read the catalog. Record root and initialized submodule Git state and preserve existing work.
   Do not run `git submodule update --remote`.
3. Install uv from its official instructions if missing. On macOS, use existing Homebrew;
   if absent, follow [brew.sh](https://brew.sh) and its prerequisites. Do not install Homebrew on Linux.
4. Run `uv run dots inspect --json`. Without a local selection, preview with
   `uv run dots inspect --profile mac --json` or `--profile linux-server`.

## 2. Select and install components

- Defaults cover shells, CLI tools, and an editor. Add optional components for the user's needs;
  do not restore the historical Brewfile wholesale. Understand an existing `.dotter/local.toml`
  before changing it; a new default profile must not overwrite its choices.
- Preview with `uv run dots profile mac --with zed`. Repeat `--with` to add components;
  use `--without` to exclude defaults. Full Oh My Zsh uses `--without zsh --with oh-my-zsh`.
  Dependencies are included automatically; conflicting components cannot be selected together.
- Check component `binaries` and native installation state. Installation guidance is data for
  the agent, not a script to execute wholesale. Follow current upstream instructions where linked.
  Preserve suitable installations; setup does not imply machine-wide upgrades or removals.
- Prefer apt on Linux, then upstream prebuilt releases when suitable packages are unavailable.
  Do not install Rust by default merely to obtain CLI tools. Check architecture and complete
  runtime requirements; Helix needs more than its `hx` binary.
- Debian packages may expose `fdfind`/`batcat` instead of `fd`/`bat`. Create links in `~/.local/bin/`
  only when the desired commands are missing and targets are free; verify PATH access.
- Default Fish needs no Fisher. Install selected plugins inside Fish and verify the plugin list.
- Initialize only required private/theme submodules at the parent-pinned commits. If access fails,
  continue shared setup and report the affected component as blocked.
- Zed restores `auto_install_extensions` from the selected settings. Deploy settings before launching
  Zed, then verify the extension panel or installation directory. Do not copy extension code,
  downloaded language servers, or caches.

## 3. Compare, back up, and deploy

1. Generate the selection into a temporary file under `.local/`. Compare with the current selection,
   preserving machine-specific overrides. Back up the original before updating `.dotter/local.toml`;
   do not commit local selections.
2. Run inspect again and review `previous_deployments`. Dotter may remove cached deployments when
   selections change, so include files leaving management in the comparison.
3. Review Git diffs for files already linked to the repo. Compare independent files and merge reusable
   changes. Without a common baseline, modification time alone cannot resolve a conflict; show the
   concrete diff and ask when intent remains unclear.
4. Back up targets to replace and existing Dotter local configuration/cache under
   `.local/backups/<UTC-timestamp>/`, preserving permissions and symlinks themselves. Preserve
   HOME-relative paths; place other paths under `absolute/`. Record original-to-backup paths.
   Verify backups before moving resolved targets aside; never overwrite an earlier backup.
5. Run `dotter deploy --dry-run`, review deployment and old-link removals, then run
   `dotter deploy --verbose`. Avoid blanket `--force`. Recompare targets rewritten by apps
   between preview and deployment.

Prefer explicit symbolic mappings. Inspect marks templates, conditions, and ownership as `manual`;
review them with Dotter rather than copying rendered output over source templates.
Authentication files are not deployed. If an old device still links authentication state into the
repo, preserve it as a device-local regular file before retiring the mapping; exclude contents
from reports.

Codex configuration is also device-local. Never deploy or copy it from shared or private repository
snapshots on a new machine. If an existing device links its Codex configuration into the repo,
back up the link and its current contents, replace the link with an identical device-local regular
file, then retire its cached deployment. Preserve local settings and verify the file is no longer
a symlink before deploying other configurations.

## 4. Local overrides and verification

- Git identity belongs in `~/.config/git/local.gitconfig`, included by shared defaults. Preserve
  the device's existing valid identity; ask if missing rather than using a system-guessed identity.
- Fish reads `~/.config/fish/local_env.fish`. Minimal Zsh reads `~/.config/local_env` and
  `~/.config/zsh/local.zsh`. Local overrides load last. Never copy tokens between devices or assume
  the `en_US.UTF-8` locale exists.
- Verify selected commands and versions, Fish syntax with `fish --no-execute`, Zsh with `zsh -n`,
  and TOML syntax. Check interactive shell startup, `hx --health`, and actual Zellij config parsing.
  For GUI components, verify installation and config loading. Service activation and system
  permissions require the corresponding user request.
- Rerun inspect. Report completed items, retained local differences, optional items, and blockers.
  Continue independent work after failures; retry detection after fixing them rather than blindly
  reinstalling. Before restoring backups, inspect new changes, then restore files and selections
  individually using the backup manifest.
