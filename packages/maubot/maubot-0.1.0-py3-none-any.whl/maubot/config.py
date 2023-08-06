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
import random
import string
import bcrypt
import re

from mautrix.util.config import BaseFileConfig, ConfigUpdateHelper

bcrypt_regex = re.compile(r"^\$2[ayb]\$.{56}$")


class Config(BaseFileConfig):
    @staticmethod
    def _new_token() -> str:
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=64))

    def do_update(self, helper: ConfigUpdateHelper) -> None:
        base = helper.base
        copy = helper.copy
        copy("database")
        copy("crypto_database.type")
        copy("crypto_database.postgres_uri")
        copy("crypto_database.pickle_dir")
        copy("plugin_directories.upload")
        copy("plugin_directories.load")
        copy("plugin_directories.trash")
        copy("plugin_directories.db")
        copy("server.hostname")
        copy("server.port")
        copy("server.public_url")
        copy("server.listen")
        copy("server.base_path")
        copy("server.ui_base_path")
        copy("server.plugin_base_path")
        copy("server.override_resource_path")
        copy("server.appservice_base_path")
        shared_secret = self["server.unshared_secret"]
        if shared_secret is None or shared_secret == "generate":
            base["server.unshared_secret"] = self._new_token()
        else:
            base["server.unshared_secret"] = shared_secret
        copy("registration_secrets")
        copy("admins")
        for username, password in base["admins"].items():
            if password and not bcrypt_regex.match(password):
                if password == "password":
                    password = self._new_token()
                base["admins"][username] = bcrypt.hashpw(password.encode("utf-8"),
                                                         bcrypt.gensalt()).decode("utf-8")
        copy("api_features.login")
        copy("api_features.plugin")
        copy("api_features.plugin_upload")
        copy("api_features.instance")
        copy("api_features.instance_database")
        copy("api_features.client")
        copy("api_features.client_proxy")
        copy("api_features.client_auth")
        copy("api_features.dev_open")
        copy("api_features.log")
        copy("logging")

    def is_admin(self, user: str) -> bool:
        return user == "root" or user in self["admins"]

    def check_password(self, user: str, passwd: str) -> bool:
        if user == "root":
            return False
        passwd_hash = self["admins"].get(user, None)
        if not passwd_hash:
            return False
        return bcrypt.checkpw(passwd.encode("utf-8"), passwd_hash.encode("utf-8"))
