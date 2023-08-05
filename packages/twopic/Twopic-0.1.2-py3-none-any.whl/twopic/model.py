# coding: utf-8

import hashlib
import logging
import os
import re
import tarfile
import urllib.request
from pathlib import Path

logging.basicConfig(level=logging.INFO)

# model_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
# model_root = r"C:\Users\Kydlaw\Documents\GitHub\semantic-propagation\models"


def set_local_model(model_url: str, model_root: str):
    model_root = Path(model_root)
    model_hash: str = hashlib.sha1(model_url.encode("utf8")).hexdigest()
    if model_root.exists():
        logging.debug("models/ exists")
        model_dir = model_root / model_hash
        if model_dir_exists(model_root, model_hash):
            logging.debug("063d866c06683311b44b4992fd46003be952409c exists")
            if model_dir_is_empty(model_dir):
                logging.debug("063d866c06683311b44b4992fd46003be952409c is empty")
                dl_model(model_url, model_dir)
            else:
                logging.debug("063d866c06683311b44b4992fd46003be952409c is NOT empty")
                return str(model_dir)
        else:
            logging.debug("063d866c06683311b44b4992fd46003be952409c NOT exists")
            model_dir: Path = create_model_dir(model_root, model_hash)
            dl_model(model_url, model_dir)
    else:
        logging.debug("models/ NOT exists")
        model_root.mkdir()
        model_dir: Path = create_model_dir(model_root, model_hash)
        dl_model(model_url, model_dir)

    return str(model_dir)


def to_download_url(model_url: str) -> str:
    tmp_url = re.sub(r"tfhub.dev", "storage.googleapis.com/tfhub-modules", model_url)
    url_download: str = tmp_url + ".tar.gz"
    return url_download


def write_downloaded_model(handle, dest: Path):
    file_name = dest / "model.tar.gz"
    # Download the model as a compressed archive
    with open(file_name, "wb") as out:
        while True:
            data = handle.read(1024)
            if len(data) == 0:
                break
            out.write(data)
    # Extract the model
    tar = tarfile.open(file_name, "r:gz")
    tar.extractall(file_name.parent)
    tar.close()
    # Clean the compressed archive
    file_name.unlink()


def dl_model(model_url: str, model_dir: Path):
    os.environ["TFHUB_CACHE_DIR"] = str(model_dir)
    url_download = to_download_url(model_url)
    handle = urllib.request.urlopen(url_download)
    write_downloaded_model(handle, dest=model_dir)


def model_dir_is_empty(model_dir: Path) -> bool:
    if not [elt for elt in model_dir.iterdir()]:
        return True
    else:
        return False


def model_dir_exists(model_root: Path, model_hash: str) -> bool:
    if model_hash in {str(model.parts[-1]) for model in model_root.iterdir()}:
        return True
    else:
        return False


def create_model_dir(model_root: Path, model_hash: str) -> Path:
    model_path = model_root / model_hash
    if not model_path.exists():
        model_path.mkdir()
        return model_path

