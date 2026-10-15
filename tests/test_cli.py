import json
import tomllib

import pytest
from typer.testing import CliRunner

from dotfiles_tools.cli import app, find_repo


@pytest.fixture
def runner():
    return CliRunner()


def test_profile_output_does_not_replace_local_config(root, runner):
    local = root / ".dotter/local.toml"
    before = local.read_bytes() if local.exists() else None
    result = runner.invoke(app, ["--repo", str(root), "profile", "mac", "--with", "zed"])
    assert result.exit_code == 0, result.output
    assert "zed" in tomllib.loads(result.stdout)["packages"]
    assert result.stderr == ""
    assert before == (local.read_bytes() if local.exists() else None)


def test_repeated_component_options_and_exclusions(root, runner):
    result = runner.invoke(
        app,
        [
            "--repo",
            str(root),
            "profile",
            "mac",
            "--with",
            "zed",
            "--with",
            "oh-my-zsh",
            "--without",
            "zsh",
            "--without",
            "helix",
        ],
    )
    assert result.exit_code == 0, result.output
    packages = set(tomllib.loads(result.stdout)["packages"])
    assert {"zed", "oh-my-zsh"} <= packages
    assert not {"zsh", "helix"} & packages


def test_discovery_from_subdirectory(root, runner, monkeypatch):
    directory = root / "src/dotfiles_tools"
    assert find_repo(directory) == root
    monkeypatch.chdir(directory)
    result = runner.invoke(app, ["profile", "linux-server"])
    assert result.exit_code == 0, result.output
    assert tomllib.loads(result.stdout)["includes"] == [".dotter/ubuntu.toml"]


@pytest.mark.parametrize("args", [["--help"], ["profile", "--help"], ["inspect", "--help"]])
def test_help_is_available_outside_a_checkout(tmp_path, monkeypatch, runner, args):
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(app, args)
    assert result.exit_code == 0, result.output
    assert "Usage:" in result.stdout


@pytest.mark.parametrize(
    "args, message",
    [
        ([], "Missing command"),
        (["unknown"], "No such command"),
        (["profile"], "Missing argument"),
        (["inspect", "--unknown"], "No such option"),
        (["profile", "mac", "--with"], "requires an argument"),
    ],
)
def test_argument_errors_use_exit_code_two(runner, args, message):
    result = runner.invoke(app, args)
    assert result.exit_code == 2
    assert message in result.stderr
    assert result.stdout == ""


def test_component_error_goes_to_stderr(root, runner):
    result = runner.invoke(app, ["--repo", str(root), "profile", "mac", "--with", "unknown"])
    assert result.exit_code == 2
    assert result.stdout == ""
    assert "Unknown component" in result.stderr
    assert "Traceback" not in result.output


def test_missing_configuration_has_actionable_error(environment, monkeypatch, runner):
    (environment.repo / ".dotter/local.toml").unlink()
    monkeypatch.setattr("dotfiles_tools.dotter.socket.gethostname", lambda: "missing-host")
    result = runner.invoke(app, ["--repo", str(environment.repo), "inspect"])
    assert result.exit_code == 2
    assert "--profile" in result.stderr
    assert result.stdout == ""


def test_json_has_no_contents_and_does_not_write(environment, runner):
    before = (environment.repo / ".dotter/local.toml").read_bytes()
    result = runner.invoke(
        app, ["--repo", str(environment.repo), "inspect", "--home", str(environment.home), "--json"]
    )
    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout)["git"]["status"] == "unavailable"
    assert "shared value" not in result.stdout
    assert result.stderr == ""
    assert before == (environment.repo / ".dotter/local.toml").read_bytes()


def test_text_inspection_preserves_readable_summary(environment, runner):
    result = runner.invoke(
        app, ["--repo", str(environment.repo), "inspect", "--home", str(environment.home)]
    )
    assert result.exit_code == 0, result.output
    assert "Selection: .dotter/local.toml" in result.stdout
    assert "missing=2" in result.stdout


def test_profile_inspection_without_local_file(root, tmp_path, runner):
    result = runner.invoke(
        app,
        [
            "--repo",
            str(root),
            "inspect",
            "--profile",
            "linux-server",
            "--home",
            str(tmp_path),
            "--json",
        ],
    )
    assert result.exit_code == 0, result.output
    report = json.loads(result.stdout)
    assert report["selection"] == "profile:linux-server"
    assert set(report["summary"]) == {"missing"}
