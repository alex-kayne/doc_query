import os
import re
from pathlib import Path

import yaml

from app.schemas.config import Settings

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.yml"
ENV_PATTERN = re.compile(r"\${([^}]+?)}")

def _replace_name(line: str) -> str:
    env_name = ENV_PATTERN.search(line)
    if env_name is not None:
        env_value = os.getenv(env_name.group(1))
        if env_value is None:
            raise ValueError(f"В переменных среды отсутствует переменная {env_name.group(1)}")
        return ENV_PATTERN.sub(env_value, line)
    return line


def load_settings() -> Settings:
    end_str = ""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            end_str += _replace_name(line)
        return Settings.model_validate(yaml.safe_load(end_str))


settings = load_settings()

if __name__ == '__main__':
    print(settings)