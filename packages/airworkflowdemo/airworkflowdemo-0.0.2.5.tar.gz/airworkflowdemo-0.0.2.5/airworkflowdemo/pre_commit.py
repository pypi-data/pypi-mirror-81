from pathlib import Path

from airworkflowdemo.master_config import get_master_config

if __name__ == "__main__":
    """
    Load, validate and merge the individual function configs.
    Create a .commit file to signal to the post-commit hook that a commit has happened.
    """
    get_master_config()
    (Path(".") / ".commit").touch(exist_ok=True)
