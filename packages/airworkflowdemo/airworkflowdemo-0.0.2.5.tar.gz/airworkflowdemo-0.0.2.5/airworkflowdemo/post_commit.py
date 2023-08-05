from pathlib import Path
from typing import List

from git import Repo

import airworkflowdemo.constants as const
from airworkflowdemo.master_config import get_master_config
from airworkflowdemo.util import file, functions


def add_path_to_git(path: Path) -> None:
    repo = Repo(const.ROOT_DIR)
    if path.is_file():
        add_file_to_git(repo, path)
    else:
        for f in path.iterdir():
            if f.is_file():
                repo.git.execute(["git", "add", str(f)])


def add_file_to_git(repo: Repo, path: Path) -> None:
    repo.git.execute(["git", "add", str(path)])


def get_function_paths(paths: List[Path]) -> List[str]:
    return [functions.get_relative_function_path(p) for p in paths]  # noqa


def add_function_names_to_work_flows(function_names: List[str], work_flows: List[Path]) -> None:
    function_names_str = f"function: [{', '.join(function_names)}]"
    regex = r"function: \[.*\]"
    for wf in work_flows:
        file.sub_file_content(wf, regex, function_names_str)


def write_version_to_init(config: dict) -> None:
    for model_path, value in config.items():
        version_str = f'__version__ = "{value.model_version}"\n__model_name__ = "{str(model_path.parts[-1])}"\n'
        file_path = model_path / const.FUNCTION_REL_INIT_PATH
        file.write(file_path, version_str)
        add_path_to_git(file_path)


def commit_to_git() -> None:
    repo = Repo(const.ROOT_DIR)
    repo.git.execute(["git", "commit", "--amend", "-C", "HEAD", "--no-verify"])


if __name__ == "__main__":
    """
    1. Load, validate and merge the individual function configs
    2. Add the function names to the Github Action workflows
    3. Update version in functions __init__.py files
    4. Commit the changes to Git
    """
    master_config, project_to_config = get_master_config()
    add_function_names_to_work_flows(get_function_paths(list(master_config.keys())), const.WORK_FLOWS)
    write_version_to_init(master_config)
    add_path_to_git(const.WORK_FLOW_PATH)
    commit_to_git()
