import os
import shutil
import subprocess
import tomllib

import pytest

from dotfiles_tools.catalog import Catalog
from dotfiles_tools.dotter import load_configuration
from dotfiles_tools.inspect import inspect


def test_include_precedence_and_local_file_override(environment):
    (environment.repo / ".dotter/first.toml").write_text('[single.files]\nsingle = "~/.first"\n')
    (environment.repo / ".dotter/second.toml").write_text('[single.files]\nsingle = "~/.second"\n')
    local = {"packages": ["single"], "includes": [".dotter/first.toml", ".dotter/second.toml"]}
    assert environment.configuration(local).mappings[0].target == environment.home / ".second"
    local["files"] = {"single": {"target": "~/.override", "type": "symbolic"}}
    mapping = environment.configuration(local).mappings[0]
    assert mapping.target == environment.home / ".override"
    assert mapping.package == "local"


def test_empty_target_disables_mapping(environment):
    assert (
        environment.configuration({"packages": ["single"], "files": {"single": ""}}).mappings == []
    )


def test_dependencies_from_included_new_package(environment):
    (environment.repo / ".dotter/extra.toml").write_text('[extra]\ndepends = ["single"]\n')
    result = environment.configuration({"packages": ["extra"], "includes": [".dotter/extra.toml"]})
    assert result.packages == ["extra", "single"]


@pytest.mark.parametrize(
    "local",
    [
        {"packages": ["unknown"]},
        {"packages": ["single"], "unexpected": True},
    ],
)
def test_unknown_packages_and_unsupported_fields_fail(environment, local):
    with pytest.raises(ValueError):
        environment.configuration(local)


def test_environment_expansion_uses_requested_home(environment, monkeypatch):
    mapping = environment.configuration(
        {
            "packages": [],
            "files": {"single": {"target": "$HOME/space dir/file", "type": "symbolic"}},
        }
    ).mappings[0]
    assert mapping.target == environment.home / "space dir/file"
    monkeypatch.delenv("UNDEFINED_DOTFILES_TEST", raising=False)
    with pytest.raises(ValueError, match="Undefined"):
        environment.configuration(
            {"packages": [], "files": {"single": "$UNDEFINED_DOTFILES_TEST/file"}}
        )


@pytest.mark.parametrize(
    "spec",
    [
        {"type": "template", "target": "~/.single"},
        {"type": "symbolic", "target": "~/.single", "if": "some helper"},
    ],
)
def test_template_and_condition_are_not_compared_as_raw_content(environment, spec):
    result = environment.report({"packages": [], "files": {"single": spec}})
    assert result["files"][0]["status"] == "manual"


def test_sources_outside_checkout_are_rejected(environment):
    with pytest.raises(ValueError, match="escapes"):
        environment.configuration({"packages": [], "files": {"../outside": "~/.outside"}})


def test_hostname_selection_matches_dotter_fallback(environment, monkeypatch):
    (environment.repo / ".dotter/local.toml").rename(environment.repo / ".dotter/test-host.toml")
    monkeypatch.setattr("dotfiles_tools.dotter.socket.gethostname", lambda: "test-host")
    assert environment.configuration().selection == ".dotter/test-host.toml"


@pytest.mark.skipif(not shutil.which("dotter"), reason="Dotter integration requires its binary")
@pytest.mark.parametrize("profile", ["mac", "linux-server"])
def test_default_profiles_deploy_twice_into_temporary_home(root, tmp_path, profile):
    home = tmp_path / "home with spaces"
    home.mkdir()
    local = tmp_path / "local.toml"
    text = Catalog(root).select(profile).render()
    local.write_text(text)
    command = [
        shutil.which("dotter"),
        "--local-config",
        str(local),
        "--cache-file",
        str(tmp_path / "cache.toml"),
        "--cache-directory",
        str(tmp_path / "cache"),
        "deploy",
    ]
    for _ in range(2):
        result = subprocess.run(
            command, cwd=root, env={**os.environ, "HOME": str(home)}, capture_output=True, text=True
        )
        assert result.returncode == 0, result.stdout + result.stderr
        config = load_configuration(root, home, tomllib.loads(text))
        report = inspect(root, config)
        assert set(report["summary"]) == {"linked"}, report["files"]
    assert (home / ".config/fish/config.fish").is_symlink()
    assert not (home / ".codex/auth.json").exists()


@pytest.mark.parametrize(
    "shell, source, arguments",
    [
        ("zsh", "dots/zsh/minimal.zshrc", ["-f", "-i", "-c"]),
        ("fish", "dots/fish/default.fish", ["--no-config", "--interactive", "-c"]),
    ],
)
def test_shared_shell_starts_without_local_overrides(root, tmp_path, shell, source, arguments):
    binary = shutil.which(shell)
    if not binary:
        pytest.skip(f"{shell} is not installed")
    home = tmp_path / "home"
    home.mkdir()
    env = {
        **os.environ,
        "HOME": str(home),
        "ZDOTDIR": str(home),
        "XDG_CONFIG_HOME": str(home / ".config"),
        "XDG_DATA_HOME": str(home / ".local/share"),
        "XDG_CACHE_HOME": str(home / ".cache"),
        "TERM": "xterm-256color",
    }
    result = subprocess.run(
        [binary, *arguments, 'source "$DOTFILES_TEST_SOURCE"'],
        env={**env, "DOTFILES_TEST_SOURCE": str(root / source)},
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
