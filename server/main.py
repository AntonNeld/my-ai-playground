from pathlib import Path

from app import create_app

PARENT_DIR = Path(__file__).parent

challenge_dir = PARENT_DIR / "challenges"
static_dir = PARENT_DIR / "static"
app = create_app(challenge_dir=challenge_dir, static_dir=static_dir)
