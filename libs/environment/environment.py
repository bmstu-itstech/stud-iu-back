import logging
from pathlib import Path

import environ

from libs.environment.exceptions import (
    EnvFileNotFoundError,
    EnvironmentNotLoadedError,
    EnvVariableNotDefinedError,
)

logger = logging.getLogger(__name__)


class Environment:
    """Load and provide access to project environment variables.

    Values must be loaded via load() before any getter is used.

    Example:
        >>> env = Environment()
        >>> env.load(BASE_DIR / '.env')
        >>> SECRET_KEY = env.require('SECRET_KEY')
    """

    def __init__(self) -> None:
        self._env = environ.Env()
        self._is_loaded = False

    def load(self, env_path: Path) -> None:
        """Load environment variables from the given .env file.

        Raises EnvFileNotFoundError if the file does not exist.
        """
        if not env_path.exists():
            raise EnvFileNotFoundError(env_path)

        environ.Env.read_env(env_path)
        self._is_loaded = True

    def require(self, key: str) -> str:
        """Return a required variable's value, or raise if it's not set."""
        self._ensure_loaded()
        value = self._env(key, default=None)
        if not value:
            raise EnvVariableNotDefinedError(key)
        return value

    def get(self, key: str, default: str = '') -> str:
        """Return a string variable's value, or default if not set."""
        self._ensure_loaded()
        return self._env(key, default=default)

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Return a boolean variable's value, or default if not set."""
        self._ensure_loaded()
        return self._env.bool(key, default=default)

    def get_int(self, key: str, default: int = 0) -> int:
        """Return an integer variable's value, or default if not set."""
        self._ensure_loaded()
        return self._env.int(key, default=default)

    def get_list(self, key: str, default: str = '') -> list[str]:
        """Return a whitespace-separated variable's value as a list.

        Example: "127.0.0.1 localhost" -> ['127.0.0.1', 'localhost']
        """
        self._ensure_loaded()
        raw = self._env(key, default=default)
        return [v.strip() for v in raw.split() if v.strip()]

    def _ensure_loaded(self) -> None:
        if not self._is_loaded:
            raise EnvironmentNotLoadedError()
