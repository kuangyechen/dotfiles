# Sync: capture local changes

Cover registered configurations, new configurations requested by the user, and software choices
from known package managers. Produce local diffs; commit or push only when requested.

## 1. Record the baseline

- Inspect root and private submodule Git state, separating pre-existing changes from this task.
  Run `uv run dots inspect --json`. Without a local selection, establish the actual device selection;
  do not treat a fresh-device default profile as the current state.
- Keep intermediate files in `.local/`. Read relevant configs, not the entire HOME. Exclude history,
  caches, databases, sessions, and authentication state. Check whether apps are rewriting files
  before comparing and recheck before writing.
- Exclude Codex configuration from sync, including plugin/runtime settings. Keep it device-local;
  existing repository snapshots are historical references, not deployment or sync sources.

## 2. Handle configuration states

| State                                                                | Action                                                                                                                 |
| -------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `linked`                                                             | Changes are already in the source; review the owning repository's Git diff.                                            |
| `identical`                                                          | No copy needed. Restoring links is a separately requested setup/repair task.                                           |
| `different`                                                          | Compare both sides and merge reusable changes; do not overwrite unconditionally.                                       |
| `missing` / `source-missing`                                         | Check deployment, submodule availability, and deletion intent before removing mappings.                                |
| `foreign-link` / `broken-link` / `type-conflict` / `parent-conflict` | Diagnose the cause; do not follow unknown links to capture unrelated files.                                            |
| `manual`                                                             | Review templates, conditions, automatic targets, or ownership with Dotter; do not copy rendered output over templates. |
| `unreadable`                                                         | Report the path and blocker; continue independent items.                                                               |

`unmanaged` files are candidates only. Generated plugin functions, completions, and caches do not
belong in version control merely because they sit in a config directory. New mappings require
clear reusable intent.

The first inspection after migration may report `foreign-link` because the default source changed
while the device still links to a preserved old source. Consult `previous_deployments`. If the link
points to a known old source inside this repo, review its Git diff and choose a migration rather
than treating it as unknown external config. Full historical Zsh uses `oh-my-zsh`; personal Zed
settings use `zed-private`.

Keep reusable settings in the main repo, personal settings in the private submodule, and machine
paths/environment differences in local overrides. Merge concurrent changes individually, preserving
baseline user edits. Without a common ancestor, compare both versions and ask only about unresolved
intent.

Sync captures content; it does not relink or deploy other files automatically. If the user also
requests restored management, follow setup's comparison, backup, and deployment procedure.

## 3. Software and extensions

Inspect only package managers already present:

- Homebrew: `brew leaves`, `brew list --cask`; consult metadata to distinguish direct installs from dependencies.
- apt: `apt-mark showmanual`; filter system packages and unrelated server software.
- uv: `uv tool list`.
- Cargo: `cargo install --list`, if available.

Compare with the catalog and distinguish lasting needs, project tools, and temporary installs.
Add lasting new software as optional components; promote it to defaults only when needed across
devices. Record purpose, platform, installation guidance, binaries, and Dotter groups. Do not
replace the catalog with a machine dump. Absence on one device does not imply removal from defaults
or permission to uninstall software.

Capture Zed extensions in `auto_install_extensions` using IDs from `extension.toml`, not display
names. On macOS, inspect `~/Library/Application Support/Zed/extensions/installed/`; on Linux,
`$XDG_DATA_HOME/zed/extensions/installed/`, falling back to `~/.local/share/zed/extensions/installed/`.
Select lasting extensions and keep shared choices aligned in shared and private settings;
retain device/personal extensions in the appropriate config. Never track the entire `extensions/`
directory.

## 4. Validate and report

- Review root and submodule diffs for authentication data, machine-specific absolute paths, and
  generated state. Do not include complete private diffs in shared reports.
- After catalog or mapping changes, run tests and regenerate affected profiles to check platform/group
  consistency. Validate changed configuration syntax, rerun inspect, and compare with the baseline.
- Report captured configs, software changes, retained local differences, and blockers. Explain private
  submodule changes separately: a parent pointer cannot save uncommitted submodule content.
- When commits are requested, review scope, commit the private submodule first, then its parent pointer.
  Push only when requested and keep unrelated pre-existing edits out of task commits.
