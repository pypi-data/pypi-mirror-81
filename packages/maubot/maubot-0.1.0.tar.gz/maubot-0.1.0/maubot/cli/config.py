# maubot - A plugin-based Matrix bot system.
# Copyright (C) 2019 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import Tuple, Optional, Dict, Any
import json
import os

from colorama import Fore

config: Dict[str, Any] = {
    "servers": {},
    "aliases": {},
    "default_server": None,
}
configdir = os.environ.get("XDG_CONFIG_HOME", os.path.join(os.environ.get("HOME"), ".config"))


def get_default_server() -> Tuple[Optional[str], Optional[str]]:
    try:
        server: Optional[str] = config["default_server"]
    except KeyError:
        server = None
    if server is None:
        print(f"{Fore.RED}Default server not configured.{Fore.RESET}")
        return None, None
    return server, _get_token(server)


def get_token(server: str) -> Tuple[Optional[str], Optional[str]]:
    if not server:
        return get_default_server()
    if server in config["aliases"]:
        server = config["aliases"][server]
    return server, _get_token(server)


def _resolve_alias(alias: str) -> Optional[str]:
    try:
        return config["aliases"][alias]
    except KeyError:
        return None


def _get_token(server: str) -> Optional[str]:
    try:
        return config["servers"][server]
    except KeyError:
        print(f"{Fore.RED}No access token saved for {server}.{Fore.RESET}")
        return None


def save_config() -> None:
    with open(f"{configdir}/maubot-cli.json", "w") as file:
        json.dump(config, file)


def load_config() -> None:
    try:
        with open(f"{configdir}/maubot-cli.json") as file:
            loaded = json.load(file)
            config["servers"] = loaded.get("servers", {})
            config["aliases"] = loaded.get("aliases", {})
            config["default_server"] = loaded.get("default_server", None)
    except FileNotFoundError:
        pass
