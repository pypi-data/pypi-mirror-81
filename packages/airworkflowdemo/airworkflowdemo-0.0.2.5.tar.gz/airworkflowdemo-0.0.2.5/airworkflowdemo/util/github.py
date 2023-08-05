from typing import List

from github import Github

from airworkflowdemo.util import env


def get_open_pr_refs() -> List[str]:
    client = Github(login_or_token=env.get_github_token(), per_page=100)
    repo = client.get_repo(env.get_repo_name())
    return [pr.head.ref for pr in repo.get_pulls("open")]
