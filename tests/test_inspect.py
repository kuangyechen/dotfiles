import json
import shutil
import subprocess
from pathlib import Path

import pytest

from dotfiles_tools.inspect import git_status


def test_missing_targets_do_not_get_created(environment):
    before = sorted(environment.home.rglob("*"))
    assert set(environment.statuses().values()) == {"missing"}
    assert before == sorted(environment.home.rglob("*"))
    assert not (environment.repo / ".dotter/cache.toml").exists()


def test_symlink_edit_is_already_a_repository_edit(environment):
    target = environment.home / ".single"
    target.symlink_to(environment.repo / "single")
    target.write_text("local edit through link\n")
    assert environment.statuses()[".single"] == "linked"
    assert (environment.repo / "single").read_text() == "local edit through link\n"


def test_application_replaces_link_and_both_sides_change(environment):
    target = environment.home / ".single"
    target.symlink_to(environment.repo / "single")
    target.unlink()
    target.write_text("application edit\n")
    (environment.repo / "single").write_text("repository edit\n")
    before = {path: path.read_bytes() for path in (target, environment.repo / "single")}
    assert environment.statuses()[".single"] == "different"
    assert before == {path: path.read_bytes() for path in before}


def test_identical_regular_file_is_not_reported_as_linked(environment):
    shutil.copyfile(environment.repo / "single", environment.home / ".single")
    assert environment.statuses()[".single"] == "identical"


def test_broken_and_foreign_links_are_preserved(environment):
    target = environment.home / ".single"
    target.symlink_to("nonexistent")
    assert environment.statuses()[".single"] == "broken-link"
    target.unlink()
    other = environment.home / "other"
    other.write_text("unrelated contents")
    target.symlink_to(other)
    report = environment.report()
    assert environment.statuses()[".single"] == "foreign-link"
    assert "unrelated contents" not in json.dumps(report)
    assert target.is_symlink()


def test_file_symlink_loop_is_reported(environment):
    (environment.home / ".single").symlink_to(".single")
    assert environment.statuses()[".single"] == "unreadable"


def test_file_directory_and_parent_conflicts(environment):
    (environment.home / ".single").mkdir()
    (environment.home / ".config").write_text("not a directory")
    assert environment.statuses()[".single"] == "type-conflict"
    assert environment.statuses()["preferences.toml"] == "parent-conflict"


def test_directory_extras_are_not_collected_or_deleted(environment):
    target = environment.home / ".config/example"
    target.mkdir(parents=True)
    (target / "preferences.toml").symlink_to(environment.repo / "conf/preferences.toml")
    (target / "plugin-generated.fish").write_text("not tracked\n")
    (target / "external-directory").symlink_to(environment.home, target_is_directory=True)
    report = environment.report()
    assert environment.statuses()["preferences.toml"] == "linked"
    assert {Path(item["target"]).name for item in report["unmanaged"]} == {
        "plugin-generated.fish",
        "external-directory",
    }
    assert "not tracked" not in json.dumps(report)
    assert (target / "plugin-generated.fish").exists()


def test_correct_directory_link_and_foreign_directory_link(environment):
    target = environment.home / ".config/example"
    target.parent.mkdir()
    target.symlink_to(environment.repo / "conf", target_is_directory=True)
    assert environment.statuses()["preferences.toml"] == "linked"
    target.unlink()
    target.symlink_to(environment.home, target_is_directory=True)
    assert environment.statuses()["example"] == "foreign-link"
    assert environment.report()["unmanaged"] == []


def test_missing_private_config_and_uninitialized_submodule(environment):
    (environment.repo / "private").mkdir()
    (environment.repo / ".gitmodules").write_text(
        '[submodule "personal"]\npath = private\nurl = example.invalid/private\n'
    )
    report = environment.report({"packages": ["private"]})
    assert report["files"][0]["status"] == "source-missing"
    assert report["submodules"] == [{"path": "private", "state": "uninitialized"}]


def test_cached_retired_deployment_is_reported(environment):
    (environment.repo / ".dotter/cache.toml").write_text(
        '[symlinks]\nold = "/old/target"\n[templates]\n'
    )
    assert environment.report()["previous_deployments"] == [
        {"source": "old", "target": "/old/target", "kind": "symlinks"}
    ]


def test_recursive_source_cycle_is_rejected(environment):
    (environment.repo / "conf/loop").symlink_to(environment.repo / "conf", target_is_directory=True)
    with pytest.raises(ValueError, match="cycle"):
        environment.report()


def test_expanded_target_collision_is_rejected(environment):
    local = {
        "packages": ["directory"],
        "files": {"single": {"target": "~/.config/example/preferences.toml", "type": "symbolic"}},
    }
    with pytest.raises(ValueError, match="overlap"):
        environment.report(local)


def test_nonrecursive_directory_is_not_walked(environment):
    local = {
        "packages": [],
        "files": {"conf": {"target": "~/.whole-directory", "type": "symbolic", "recurse": False}},
    }
    (environment.home / ".whole-directory").symlink_to(
        environment.repo / "conf", target_is_directory=True
    )
    report = environment.report(local)
    assert len(report["files"]) == 1
    assert report["files"][0]["status"] == "linked"


def test_git_renames_and_dirty_files_are_reported_without_refresh(tmp_path):
    def git(*args):
        return subprocess.run(["git", "-C", str(tmp_path), *args], capture_output=True, check=True)

    git("init", "-q")
    (tmp_path / "original file").write_text("initial\n")
    git("add", "original file")
    git(
        "-c",
        "core.hooksPath=/dev/null",
        "-c",
        "commit.gpgsign=false",
        "-c",
        "user.name=Test",
        "-c",
        "user.email=test@example.invalid",
        "commit",
        "-qm",
        "fixture",
    )
    git("mv", "original file", "renamed file")
    (tmp_path / "renamed file").write_text("local changes\n")
    index = tmp_path / ".git/index"
    before = (index.read_bytes(), index.stat().st_mtime_ns)
    report = git_status(tmp_path)
    assert report["status"] == "dirty"
    assert report["changes"] == [
        {"status": "RM", "path": "renamed file", "original_path": "original file"}
    ]
    assert before == (index.read_bytes(), index.stat().st_mtime_ns)


def test_initialized_private_repository_has_separate_dirty_status(environment):
    private = environment.repo / "private"
    private.mkdir()
    subprocess.run(["git", "init", "-q", str(private)], check=True, capture_output=True)
    (private / "settings.toml").write_text('theme = "personal"\n')
    (environment.repo / ".gitmodules").write_text(
        '[submodule "personal"]\npath = private\nurl = example.invalid/private\n'
    )
    report = environment.report({"packages": ["private"]})
    assert report["submodules"][0]["git"] == {
        "status": "dirty",
        "changes": [{"status": "??", "path": "settings.toml"}],
    }
    assert 'theme = "personal"' not in json.dumps(report)
