import os
from pathlib import Path

import toml

CONFIG_FILE = "pyproject.toml"
DEFAULT_SRC_DIR = "src"
DEFAULT_BUILD_DIR = "build"
DEFAULT_INSTALL_DIR = "D:\\Steam\\steamapps\\common\\Elin\\Package"
DEFAULT_INSTALL_TEMPLATE_DIR = os.path.join(Path.home(), "AppData\\LocalLow\\Lafrontier\\Elin\\User\\PCC")


class Config:
    _cfg = {}

    root = None
    package_name = None
    src_dir = None
    build_dir = None
    install_dir = None
    install_template_dir = None

    def __init__(self):
        self.root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self._cfg = toml.load(os.path.join(self.root, CONFIG_FILE))

        self.package_name = self.get("tool.elin.package-name") or "My_Mod"

        self.src_dir = os.path.join(self.root, self.get("tool.elin.src-dir") or DEFAULT_SRC_DIR)
        self.build_dir = os.path.join(self.root, self.get("tool.elin.build-dir") or DEFAULT_BUILD_DIR)

        self.install_dir = os.path.join(os.path.abspath(self.get("tool.elin.install-dir") or DEFAULT_INSTALL_DIR))
        self.install_template_dir = os.path.abspath(
            self.get("tool.elin.install-template-dir") or DEFAULT_INSTALL_TEMPLATE_DIR)

    def get(self, key: str):
        path = key.split(".")
        return self._safe_dict(self._cfg, *path)

    def to_dict(self):
        return self._cfg

    @staticmethod
    def _safe_dict(_dict: dict[str, any], *kwargs: str) -> any or None:
        try:
            entry = _dict.get(kwargs[0])

            if len(kwargs) > 1:
                return Config._safe_dict(entry, *kwargs[1:])
            else:
                return entry
        except KeyError:
            return None
