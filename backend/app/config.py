from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.1-flash-lite"


    port: int = 8000
    host: str = "0.0.0.0"
    debug: bool = False

    max_file_size_mb: int = 20
    max_rows_sampling: int = 50000
    heavy_step_subsample: int = 5000
    heavy_step_permutations: int = 30
    step_timeout_seconds: int = 120
    vif_threshold: float = 5.0
    leakage_corr_threshold: float = 0.85

    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    sessions_dir: Path = base_dir / "sessions"
    data_dir: Path = base_dir / "data"
    frontend_dir: Path = base_dir / "frontend"

    @property
    def is_offline(self) -> bool:
        return not bool(self.gemini_api_key and self.gemini_api_key.strip())


settings = Settings()
