from pathlib import Path

from app import create_app

PARENT_DIR = Path(__file__).parent

template_dir = PARENT_DIR / "dungeon" / "templates"
static_dir = PARENT_DIR / "static"
app = create_app(template_dir=template_dir, static_dir=static_dir)
