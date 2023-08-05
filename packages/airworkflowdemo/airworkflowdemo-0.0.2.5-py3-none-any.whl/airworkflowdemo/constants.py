from pathlib import Path,PosixPath
from typing import Dict
from airworkflowdemo.util import env
from airworkflowdemo.model.project import Project, ProjectInfo


working_path = env.get_env_value("PWD")
ROOT_DIR = PosixPath(working_path)
FUNCTIONS_PATH = ROOT_DIR / "functions"
CUSTOMERS_FUNCTIONS_PATH = FUNCTIONS_PATH / "customers"
AIR_INFRA_FUNCTIONS_PATH = FUNCTIONS_PATH / "air_infrastructure"
SHARED_FUNCTIONS_PATH = FUNCTIONS_PATH / "shared"
IGNORE_MODELS_PATH = ROOT_DIR / ".ignore_models"

# Paths within a functions folder
FUNCTION_REL_PATH = Path("function")
FUNCTION_REL_CONFIG_PATH = FUNCTION_REL_PATH / "config.yaml"
FUNCTION_REL_RESOURCE_PATH = FUNCTION_REL_PATH / "resources"
FUNCTION_REL_DEPLOYMENT_PATH = FUNCTION_REL_RESOURCE_PATH / "dependencies.yaml"
FUNCTION_REL_INIT_PATH = FUNCTION_REL_PATH / "__init__.py"

# WORK FLOW PATHS
WORK_FLOW_PATH = ROOT_DIR / ".github" / "workflows"
WORK_FLOWS = [WORK_FLOW_PATH / p for p in ["build-master.yaml", "build-pr.yaml", "delete-pr.yaml"]]

    # CONFIG PATHS
BASE_PATH =  Path(__file__).parent.resolve()
SCHEMAS_PATH = BASE_PATH / "schemas"
DEPLOYMENT_SCHEMA_PATH = SCHEMAS_PATH / "deployment-schema.yaml"
CONFIG_SCHEMA_PATH = SCHEMAS_PATH / "config-schema.yaml"

# Tenant name to api key variables name
PROJECT_TO_API_KEYS: Dict[Project, ProjectInfo] = {
    Project.AKERBP: ProjectInfo(Project.AKERBP, "AKERBP_DEPLOY_KEY", "AKERBP_KEY"),
    Project.AKERBP_TEST: ProjectInfo(Project.AKERBP_TEST, "AKERBP_TEST_DEPLOY_KEY", "AKERBP_TEST_KEY"),
    Project.EXXON: ProjectInfo(Project.EXXON, "EXXON_DEPLOY_KEY", "EXXON_KEY", ""),
    Project.EUREKA_TAD_DEV: ProjectInfo(Project.EUREKA_TAD_DEV, "EUREKA_TAD_DEV_DEPLOY_KEY", "EUREKA_TAD_DEV_KEY"),
    Project.SEBNICKELGREENFIELD: ProjectInfo(
        Project.SEBNICKELGREENFIELD,
        "SEBNICKELGREENFIELD_DEPLOY_KEY",
        "SEBNICKELGREENFIELD_KEY",
        "https://greenfield.cognitedata.com",
    ),
    Project.FRAMO: ProjectInfo(Project.FRAMO, "FRAMO_DEPLOY_KEY", "FRAMO_KEY"),
}
