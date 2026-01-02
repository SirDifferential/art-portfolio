from pathlib import Path
import logging
from rich.logging import RichHandler
from logging.handlers import RotatingFileHandler

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

class DebugEasy:
    def __repr__(self):
        cls = self.__class__.__name__
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{cls}({attrs})"

    def __eq__(self, other):
            return type(self) is type(other) and vars(self) == vars(other)

    def __hash__(self):
        # order-independent; all your value types are hashable
        return hash(frozenset(vars(self).items()))

class ArtPiece:
    def __init__(self, path, thumbnail_path):
        self.path = path
        self.thumbnail_path = thumbnail_path

class Category:
    def __init__(self, name, first_layer_p, second_layer_p):
        self.name = name
        self.first_layer_p = first_layer_p
        self.second_layer_p = second_layer_p
        self.art_pieces = []

        self._get_art()

        
    def _get_art(self):
        name_to_key_mapping = {}
        thumbnail_mapping = {}
        for p in self.first_layer_p.iterdir():
            if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
                thumbnail_mapping[p] = None
                name_to_key_mapping[p.name] = p

        for p in self.second_layer_p.iterdir():
            if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
                if p.name in name_to_key_mapping:
                    k = name_to_key_mapping[p.name]
                    thumbnail_mapping[k] = p
                    log.debug(f"Associated \"{self.name}/{p.name}\" art piece.")
                else:
                    log.warning(f"WARNING: \"{self.name}/{p.name}\" thumbnail was not matched with anything.")

        for k in thumbnail_mapping:
            if thumbnail_mapping[k] == None:
                log.warning(f"WARNING: \"{self.name}/{k.name}\" artwork was not matched with anything.")
            else:
                self.art_pieces.append(ArtPiece(k, thumbnail_mapping[k]))



cwd = Path.cwd()
detected_categories = []

for first_layer in sorted([p for p in cwd.iterdir() if p.is_dir()]):
    if first_layer.name == ".git":
        continue

    second_layer = next((p for p in first_layer.iterdir() if p.is_dir()), None)

    if second_layer is not None and second_layer.name == "thumbnails":
        log.info(f"Added {first_layer.name} as a category.")
        detected_categories.append(Category(first_layer.name, first_layer, second_layer))


