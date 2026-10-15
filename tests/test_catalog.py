import tomllib
from pathlib import Path

import pytest

from dotfiles_tools.catalog import Catalog, CatalogData
from dotfiles_tools.dotter import load_configuration


@pytest.mark.parametrize("profile", ["mac", "linux-server"])
def test_default_profiles_are_portable_without_private_dependency(root, profile):
    selection = Catalog(root).select(profile)
    config = load_configuration(
        root, Path("/tmp/dotfiles-test-home"), tomllib.loads(selection.render())
    )
    assert {"fish", "zsh"} <= set(config.packages)
    assert not set(selection.components) & {"rust", "oh-my-zsh"}
    assert not any("private-dotfiles" in str(item.source) for item in config.mappings)
    if profile == "linux-server":
        assert not set(config.packages) & {"alacritty", "zed", "aerospace", "warp"}


def test_every_optional_component_resolves_on_declared_platforms(root):
    catalog = Catalog(root)
    for name, component in catalog.components.items():
        for platform in component.platforms:
            profile = "mac" if platform == "macos" else "linux-server"
            exclusions = ("zsh",) if name == "oh-my-zsh" else ()
            selected = catalog.select(profile, (name,), exclusions)
            load_configuration(
                root, Path("/tmp/dotfiles-test-home"), tomllib.loads(selected.render())
            )


def test_component_dependencies(root):
    selection = Catalog(root).select("mac", ("fish-plugins",))
    assert "fisher" in selection.components
    selection = Catalog(root).select("mac", ("oh-my-zsh",), ("zsh",))
    assert "oh-my-zsh" in selection.packages
    assert "zsh" not in selection.packages


@pytest.mark.parametrize(
    "additions, exclusions",
    [
        (("oh-my-zsh",), ()),
        (("zed", "zed-private"), ()),
        (("aerospace", "skhd"), ()),
        (("fish-plugins",), ("fish",)),
    ],
)
def test_component_conflicts_and_excluded_dependencies_fail(root, additions, exclusions):
    with pytest.raises(ValueError):
        Catalog(root).select("mac", additions, exclusions)


@pytest.mark.parametrize(
    "profile, additions",
    [
        ("unknown", ()),
        ("mac", ("unknown",)),
        ("linux-server", ("zed",)),
    ],
)
def test_bad_profile_component_and_platform_fail(root, profile, additions):
    with pytest.raises(ValueError):
        Catalog(root).select(profile, additions)


def test_authentication_is_not_a_deployment_target(root):
    selection = Catalog(root).select("mac", ("codex",))
    config = load_configuration(
        root, Path("/tmp/dotfiles-test-home"), tomllib.loads(selection.render())
    )
    assert not any(item.target.name == "auth.json" for item in config.mappings)


@pytest.mark.parametrize(
    "change",
    [
        {"core": [42]},
        {"version": 2},
        {"unexpected_setting": "should not be ignored"},
        {"profiles": {"mac": {"platform": "windows"}}},
    ],
)
def test_catalog_schema_rejects_invalid_structure(root, change):
    with (root / "catalog.toml").open("rb") as stream:
        data = tomllib.load(stream)
    data.update(change)
    with pytest.raises(ValueError):
        CatalogData.model_validate(data)
