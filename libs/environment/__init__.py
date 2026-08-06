from libs.environment.environment import Environment
from libs.environment.exceptions import (
    EnvironmentError,
    EnvironmentNotLoadedError,
    EnvVariableNotDefinedError,
)

env = Environment()

__all__ = [
    "Environment",
    "env",
    "EnvironmentError",
    "EnvVariableNotDefinedError",
    "EnvironmentNotLoadedError",
]
