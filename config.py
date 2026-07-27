import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"

load_dotenv(ROOT / ".env")


def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value or value.startswith("RGAPI-your"):
        raise RuntimeError(
            f"Set {name} in .env (copy from .env.example). "
            "Get a key at https://developer.riotgames.com/"
        )
    return value


RIOT_API_KEY = os.getenv("RIOT_API_KEY", "")
RIOT_GAME_NAME = os.getenv("RIOT_GAME_NAME", "")
RIOT_TAG_LINE = os.getenv("RIOT_TAG_LINE", "NA1")
RIOT_PLATFORM = os.getenv("RIOT_PLATFORM", "na1")
RIOT_REGION = os.getenv("RIOT_REGION", "americas")
