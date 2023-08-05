from enum import Enum
from typing import Optional

from airworkflowdemo.util import env


class Project(Enum):
    AKERBP = "akerbp"
    AKERBP_TEST = "akerbp-test"
    EXXON = "exxon"
    EUREKA_TAD_DEV = "eureka-tad-dev"
    SEBNICKELGREENFIELD = "sebnickelgreenfield"
    FRAMO = "framo"

    @classmethod
    def _missing_(cls, value):
        raise ValueError(f"{value} is not a valid AIR project, must be one of {[p.value for p in Project]}")


class ProjectInfo:
    def __init__(self, project: Project, deployment_key_name: str, client_key_name: str, base_url: str = None):
        self.name: str = project.value
        self.deployment_key_name: str = deployment_key_name
        self.client_key_name: str = client_key_name
        self.base_url: Optional[str] = base_url
        self.project: Project = project

    def get_deployment_key(self) -> str:
        return env.get_env_value(self.deployment_key_name)

    def get_client_api_key(self) -> str:
        return env.get_env_value(self.client_key_name)
