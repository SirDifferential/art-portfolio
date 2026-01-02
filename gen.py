from pathlib import Path
import logging
from rich.logging import RichHandler
from logging.handlers import RotatingFileHandler
from utils import *

FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"

file_handler = RotatingFileHandler(
    "todo2.log",
    maxBytes=5_000_000,   # 5 MB
    backupCount=3,        # keep 3 old logs
    encoding="utf-8",
)
file_handler.setLevel(logging.NOTSET)
file_handler.setFormatter(logging.Formatter(FORMAT, datefmt="[%X]"))

logging.basicConfig(
    level=logging.NOTSET,
    handlers=[
        RichHandler(rich_tracebacks=True),  # console
        file_handler,                      # file
    ],
)

log = logging.getLogger("rich")

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff", ".webp", ".heic", ".heif"}



cwd = Path.cwd()
detected_categories = []

for first_layer in sorted([p for p in cwd.iterdir() if p.is_dir()]):
    if first_layer.name == ".git":
        continue

    second_layer = next((p for p in first_layer.iterdir() if p.is_dir()), None)

    if second_layer is not None and second_layer.name == "thumbnails":
        log.info(f"Added {first_layer.name} as a category.")
        detected_categories.append(Category(first_layer.name, first_layer, second_layer))


