import os
import gzip
import shutil
import logging
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

def _gzip_rotator(source, dest):
    """
    Compresse le fichier rotated en .gz et supprime l'original.
    """
    with open(source, "rb") as f_in, gzip.open(dest + ".gz", "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    os.remove(source)


def build_logging_dict():
    """
    Retourne un dict LOGGING Django :
    - console toujours activée
    - fichier activé si DJANGO_LOG_DIR est défini
    - rotation quotidienne + gzip + rétention
    """
    log_level = os.getenv("DJANGO_LOG_LEVEL", "INFO").upper()
    log_dir = os.getenv("DJANGO_LOG_DIR", "").strip()

    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "level": log_level,
            "formatter": "standard",
        }
    }

    if log_dir:
        Path(log_dir).mkdir(parents=True, exist_ok=True)

        file_handler = TimedRotatingFileHandler(
            filename=str(Path(log_dir) / "backend.log"),
            when="midnight",
            interval=1,
            backupCount=14,   # 14 jours
            utc=False,
            encoding="utf-8",
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
        file_handler.rotator = _gzip_rotator

        # Django logging accepte un handler via une factory "()"
        handlers["file"] = {"()": lambda: file_handler}

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"}
        },
        "handlers": handlers,
        "root": {
            "handlers": list(handlers.keys()),
            "level": log_level,
        },
        "loggers": {
            "django": {"handlers": list(handlers.keys()), "level": log_level, "propagate": False},
            "auth_oidc": {"handlers": list(handlers.keys()), "level": log_level, "propagate": False},
            "urllib3": {"handlers": list(handlers.keys()), "level": "WARNING", "propagate": False},
        },
    }
