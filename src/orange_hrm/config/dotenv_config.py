"""Provides configuration functionality for loading environment variables."""

from functools import lru_cache

from pydantic import Field, SecretStr, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvConfig(BaseSettings):
    """Configuration class for loading OrangeHRM credentials from environment variables.

    This class uses Pydantic BaseSettings to load and validate username and password
    credentials from environment variables or a .env file. The credentials are stored
    as SecretStr to ensure sensitive data is not accidentally exposed.

    """

    username: SecretStr = Field(description="Username for OrangeHRM", alias="ORANGEHRM_USERNAME")
    password: SecretStr = Field(description="Password for OrangeHRM", alias="ORANGEHRM_PASSWORD")

    @field_validator("username", "password")
    @classmethod
    def validate_credentials(cls, v: SecretStr, info: ValidationInfo) -> SecretStr:
        """Validate that the provided credentials are not empty.

        Args:
            cls: The class reference
            v (SecretStr): The credential value to validate
            info (ValidationInfo): Validation information containing field metadata

        Returns:
            SecretStr: The validated credential value

        Raises:
            ValueError: If the credential value is empty or contains only whitespace

        """
        if not v.get_secret_value().strip():
            msg: str = f"{info.field_name} cannot be empty"
            raise ValueError(msg)
        return v

    # Reads .env and looks for ORANGEHRM_USERNAME, ORANGEHRM_PASSWORD
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Ignore extra fields from environment
    )


@lru_cache(maxsize=1)
def get_dot_env_secrets() -> EnvConfig:
    """Load and cache environment variables from .env file.

    Returns:
        EnvConfig: Configuration object containing validated OrangeHRM credentials
        loaded from environment variables or .env file.

    """
    return EnvConfig()  # type: ignore[call-arg]
