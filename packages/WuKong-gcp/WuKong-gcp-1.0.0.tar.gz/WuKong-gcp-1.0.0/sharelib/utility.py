import json
import logging
import os
import pathlib
import shutil
import tarfile
import urllib.request as request
from contextlib import closing
from typing import Tuple
from urllib.parse import urlparse, ParseResult
from zipfile import ZipFile

import colorlog


def is_url(path: str):
    parse_result: ParseResult = urlparse(path)
    return parse_result.scheme and parse_result.netloc


def download(
    url: str,
    target_path: str = "./",
    new_name: str = None,
    overwrite_existing=False,
):
    name = new_name
    if not name:
        names = url.rsplit("/", 1)
        name = names[1] if len(names) > 1 else names[0]

    dest_path = pathlib.Path(target_path)
    dest_path.mkdir(parents=True, exist_ok=True)

    target = dest_path.joinpath(name)
    if overwrite_existing or (not target.exists()):
        with closing(request.urlopen(url)) as r:
            with open(target, "wb") as f:
                shutil.copyfileobj(r, f)
    return target


def download_or_copy(url: str, output_dir: str, logger: logging):
    arr = url.rsplit("/", 1)
    name = arr[1] if len(arr) > 1 else arr[0]
    target = pathlib.Path(output_dir).joinpath(name)
    if is_url(url):
        logger.info(f"Downloading {name} to: {output_dir}")
        download(url, output_dir)
        logger.info("Done...")
    elif pathlib.Path(url).exists():
        pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
        shutil.copy(url, target)
    else:
        raise FileNotFoundError(url)
    return target


def get_env_proxy():
    proxy_url = os.environ["http_proxy"] if "http_proxy" in os.environ else None
    if proxy_url is None:
        proxy_url = (
            os.environ["https_proxy"] if "https_proxy" in os.environ else None
        )
    return proxy_url


def set_log(
    use_color=True, verbose=False, name="deployer_logger"
) -> Tuple[logging.Logger, str]:
    logger = colorlog.getLogger(name) if use_color else logging.getLogger(name)
    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)
    logFormatter = (
        colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s [%(levelname)-5.5s] %(message)s"
        )
        if use_color
        else logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
    )

    c_handler = logging.StreamHandler()
    c_handler.setFormatter(logFormatter)
    c_handler.setLevel(level)
    logger.addHandler(c_handler)

    return logger


def get_suite_base_ver(suite_meta_path: str):
    max_ver = ""
    version_key = "base_version"
    with tarfile.open(suite_meta_path, "r:gz") as f:
        f.extractall("/tmp")
    with open("/tmp/suite-metadata/suiteinfo.json", "r") as f:
        data = json.load(f)
        for version_data in data["versions"]:
            cur_version = (
                version_data[version_key] if version_key in version_data else ""
            )
            max_ver = cur_version if cur_version > max_ver else max_ver
    shutil.rmtree("/tmp/suite-metadata", ignore_errors=True)
    return max_ver


def get_cdf_version(cdf_pkg_path: str):
    ver = ""
    with ZipFile(cdf_pkg_path, "r") as zipObj:
        target_dir = "/tmp/.cdfpkg"
        version_file_name = ""
        list_of_file_names = zipObj.namelist()
        for fileName in list_of_file_names:
            if pathlib.Path(fileName).name == "version.txt":
                zipObj.extract(fileName, target_dir)
                version_file_name = fileName
                break
        version_file_path = pathlib.Path(target_dir).joinpath(version_file_name)
        with version_file_path.open("r") as f:
            for line in f:
                if line:
                    versions = line.split(".")
                    ver = str.join(".", versions[:2])
        shutil.rmtree(target_dir)
    return ver
