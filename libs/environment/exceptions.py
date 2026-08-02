from pathlib import Path


class EnvironmentError(Exception):
    """Base exception for all environment-related errors."""


class EnvFileNotFoundError(EnvironmentError):
    """Raised when the file at the specified path is not found."""

    def __init__(self, path: Path):
        super().__init__(f'.env file not found at: {path}')


class EnvVariableNotDefinedError(EnvironmentError):
    """Raised when a required environment variable is not set or empty."""

    def __init__(self, key: str):
        self.key = key
        super().__init__(
            f'Environment variable "{key}" is required but not defined'
        )


class EnvironmentNotLoadedError(EnvironmentError):
    """Raised when environment variables are accessed
    before Environment.load() has been called.
    """

    def __init__(self):
        super().__init__(
            'Environment is not loaded. Call Environment.load() first'
        )
