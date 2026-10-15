from pathlib import Path

import pytest
from pydantic import BaseModel

from dotfiles_tools.dotter import load_configuration
from dotfiles_tools.inspect import inspect


class Repository(BaseModel):
    repo: Path
    home: Path

    def configuration(self, local=None):
        return load_configuration(self.repo, self.home, local)

    def report(self, local=None):
        return inspect(self.repo, self.configuration(local))

    def statuses(self, local=None):
        return {Path(item["target"]).name: item["status"] for item in self.report(local)["files"]}


@pytest.fixture
def environment(tmp_path):
    repo = tmp_path / "repo with spaces"
    home = tmp_path / "home with spaces"
    (repo / ".dotter").mkdir(parents=True)
    (repo / "conf").mkdir()
    home.mkdir()
    (repo / "single").write_text("shared value\n")
    (repo / "conf/preferences.toml").write_text('theme = "shared"\n')
    (repo / ".dotter/global.toml").write_text("""
[settings]
default_target_type = "symbolic"
[single.files]
single = "~/.single"
[directory.files]
conf = "~/.config/example"
[private.files]
"private/settings.toml" = "~/.private"
""")
    (repo / ".dotter/local.toml").write_text('packages = ["single", "directory"]\n')
    return Repository(repo=repo, home=home)


@pytest.fixture
def root():
    return Path(__file__).resolve().parents[1]
