from pathlib import Path
from shutil import copy

from adit_radis_shared.invoke_tasks import bump_version, lint, show_outdated  # noqa: F401
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
def publish_client(ctx: Context):
    """Publish ADIT Client to PyPI

    - Make sure to bump the version first (see `bump_version` above)
    - Make sure PyPI API token is set: poetry config pypi-token.pypi your-api-token
    - Execute with `invoke publish-client`
    """
    run_cmd(ctx, "poetry publish --build")
