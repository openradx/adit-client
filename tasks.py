import sys
from pathlib import Path
from shutil import copy
from typing import Literal

from invoke.context import Context
from invoke.runners import Result
from invoke.tasks import task

project_dir = Path(__file__).resolve().parent


def run_cmd(ctx: Context, cmd: str, silent=False) -> Result:
    if not silent:
        print(f"Running: {cmd}")

    hide = True if silent else None

    result = ctx.run(cmd, pty=True, hide=hide)
    assert result and result.ok
    return result


@task
def init_workspace(ctx: Context):
    """Initialize workspace"""
    copy(f"{project_dir}/example.env", f"{project_dir}/.env")


@task
def lint(ctx: Context):
    """Lint the source code (ruff, pyright)"""
    cmd_ruff = "poetry run ruff ."
    run_cmd(ctx, cmd_ruff)
    cmd_pyright = "poetry run pyright"
    run_cmd(ctx, cmd_pyright)


@task
def bump_version(ctx: Context, rule: Literal["patch", "minor", "major"]):
    """Bump version, create a tag, commit and push to GitHub"""
    result = ctx.run("git status --porcelain", hide=True, pty=True)
    assert result and result.ok
    if result.stdout.strip():
        print("There are uncommitted changes. Aborting.")
        sys.exit(1)

    ctx.run(f"poetry version {rule}", pty=True)
    ctx.run("git add pyproject.toml", pty=True)
    ctx.run("git commit -m 'Bump version'", pty=True)
    ctx.run("git tag -a $(poetry version -s) -m 'Release $(poetry version -s)'", pty=True)
    ctx.run("git push --follow-tags", pty=True)


@task
def publish_client(ctx: Context):
    """Publish ADIT Client to PyPI

    - Make sure to bump the version first (see `bump_version` above)
    - Make sure PyPI API token is set: poetry config pypi-token.pypi your-api-token
    - Execute with `invoke publish-client`
    """
    run_cmd(ctx, "poetry publish --build")


@task
def show_outdated(ctx: Context):
    """Show outdated dependencies"""
    print("### Outdated Python dependencies ###")
    poetry_cmd = "poetry show --outdated --top-level"
    result = run_cmd(ctx, poetry_cmd)
    print(result.stderr.strip())
