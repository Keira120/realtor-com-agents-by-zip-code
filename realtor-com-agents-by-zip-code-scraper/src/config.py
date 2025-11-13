import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml
from dotenv import load_dotenv

@dataclass
class Settings:
    base_url: str = "https://www.realtor.com/realestateagents"
    rate_limit_rpm: int = 30
    user_agent: Optional[str] = None
    cookie: Optional[str] = None
    trial_limit: Optional[int] = None
    output_dir: Path = Path("data")

    @classmethod
    def from_dict(cls, data: dict) -> "Settings":
        return cls(
            base_url=data.get("base_url", cls.base_url),
            rate_limit_rpm=int(data.get("rate_limit_rpm", cls.rate_limit_rpm)),
            user_agent=data.get("user_agent"),
            cookie=data.get("cookie"),
            trial_limit=data.get("trial_limit"),
            output_dir=Path(data.get("output_dir", cls.output_dir)),
        )

def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]

def _load_env() -> None:
    root = _project_root()
    env_path = root / ".env"
    if env_path.exists():
        load_dotenv(env_path)

def _load_yaml_settings(path: Optional[str]) -> dict:
    root = _project_root()
    if path:
        yaml_path = Path(path)
    else:
        yaml_path = root / "config" / "settings.yaml"

    if not yaml_path.is_absolute():
        yaml_path = root / yaml_path

    if not yaml_path.exists():
        # Fall back to example settings for defaults if available
        example_path = root / "config" / "settings.example.yaml"
        if example_path.exists():
            with example_path.open("r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        return {}

    with yaml_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def get_settings(yaml_path: Optional[str] = None) -> Settings:
    _load_env()
    data = _load_yaml_settings(yaml_path)
    settings = Settings.from_dict(data)

    # Environment overrides
    base_url = os.getenv("REALTOR_BASE_URL")
    if base_url:
        settings.base_url = base_url

    rate_limit = os.getenv("RATE_LIMIT_RPM")
    if rate_limit:
        try:
            settings.rate_limit_rpm = int(rate_limit)
        except ValueError:
            pass

    ua = os.getenv("USER_AGENT")
    if ua:
        settings.user_agent = ua

    cookie = os.getenv("KP_UIDZ_SSN")
    if cookie:
        settings.cookie = cookie

    trial = os.getenv("TRIAL_LIMIT")
    if trial:
        try:
            settings.trial_limit = int(trial)
        except ValueError:
            pass

    output_dir = os.getenv("OUTPUT_DIR")
    if output_dir:
        settings.output_dir = Path(output_dir)

    return settings