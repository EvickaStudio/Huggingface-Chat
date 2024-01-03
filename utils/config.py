# Copyright 2024 EvickaStudio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import configparser
import logging
import os
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class Config:
    r"""
    Configuration handler for Huggingface-Chat.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A class that handles reading from and writing to a configuration file.

    ----

    Attributes
    ----------
    filename : str
        The name of the configuration file. Defaults to 'config.ini'.
    config : configparser.ConfigParser
        An instance of the `configparser.ConfigParser` class used to read and write INI files.

    Methods
    -------
    config_exists() -> bool:
        Checks if the configuration file has values for email and password.
    get_login_details() -> Dict[str, str]:
        Returns login details as a dictionary.
    set_login_details(**kwargs):
        Sets login details using kwargs.
    get_token() -> Dict[str, str]:
        Returns token information as a dictionary.
    set_token(**kwargs):
        Sets token information using kwargs.
    save_auth_data(*args, **kwargs):
        Saves authentication data.
    load_auth_data() -> Dict[str, Optional[str]]:
        Loads authentication data from the configuration file.
    update_tokens_data(*args, **kwargs):
        Updates token data.
    delete_section(section: str):
        Deletes a section from the configuration file.
    is_logged_in() -> bool:
        Checks whether there is a valid token present.
    user_credentials() -> Dict[str, Optional[str]]:
        Returns user credentials as a dictionary.

    Example
    -------
    >>> from utils.config import Config
    >>>
    >>> config = Config()
    >>> config.save_auth_data(email="E-MAIL", password="PASS")
    >>> config.update_tokens_data(token="TOKEN", expire_date="2024-06-09")
    """

    def __init__(self, filename="config.ini"):
        """
        Constructs all the necessary attributes for the Config object.

        Parameters
        ----------
            filename : str
                The name of the configuration file. Defaults to 'config.ini'.
        """
        self.filename = filename
        self.config = configparser.ConfigParser()

        if not os.path.exists(self.filename):
            self._create_config()
        else:
            self.config.read(self.filename)

    def _create_config(self):
        """Creates a default configuration file."""
        logger.debug("Creating new configuration file.")
        self.config["LOGIN"] = {}
        self.config["TOKEN"] = {}

    def config_exists(self) -> bool:
        """
        Checks if the configuration file has values for email and password.

        Returns
        -------
        bool
            True if the configuration file has values for email and password, False otherwise.
        """
        logger.debug("Checking if configuration file exists.")
        return all(self.config["LOGIN"].values())

    def get_login_details(self) -> Dict[str, str]:
        """
        Returns login details as a dictionary.

        Returns
        -------
        dict
            A dictionary of login details.
        """
        logger.debug("Retrieving login details.")
        return dict(self.config["LOGIN"].items())

    def set_login_details(self, **kwargs):
        """
        Sets login details using kwargs.

        Parameters
        ----------
            **kwargs : dict
                Keyword arguments representing login details.
        """
        logger.debug(f"Setting login details ({', '.join(kwargs)}).")
        allowed_keys = ("email", "password")
        for key, value in kwargs.items():
            assert key in allowed_keys, f"Invalid keyword argument '{key}'."

            self.config["LOGIN"].setdefault(key, "")
            self.config["LOGIN"][key] = value

        with open(self.filename, "w") as f:
            self.config.write(f)

    def get_token(self) -> Dict[str, str]:
        """
        Returns token information as a dictionary.

        Returns
        -------
        dict
            A dictionary of token information.
        """
        logger.debug("Retrieving token information.")
        return dict(self.config["TOKEN"].items())

    def set_token(self, **kwargs):
        """
        Sets token information using kwargs.

        Parameters
        ----------
            **kwargs : dict
                Keyword arguments representing token information.
        """
        logger.debug(f"Setting token information ({', '.join(kwargs)}).")
        allowed_keys = ("token", "expire_date")
        for key, value in kwargs.items():
            assert key in allowed_keys, f"Invalid keyword argument '{key}'."

            self.config["TOKEN"].setdefault(key, "")
            self.config["TOKEN"][key] = value

        with open(self.filename, "w") as f:
            self.config.write(f)

    def save_auth_data(self, *args, **kwargs):
        """
        Saves authentication data.

        Parameters
        ----------
            *args : tuple
                Positional arguments.
            **kwargs : dict
                Keyword arguments.
        """
        self.set_login_details(*args, **kwargs)

    def load_auth_data(self) -> Dict[str, Optional[str]]:
        """
        Loads authentication data from the configuration file.

        Returns
        -------
        dict
            A dictionary of authentication data.
        """
        return {
            "email": self.get_login_details().get("email"),
            "password": self.get_login_details().get("password"),
        }

    def update_tokens_data(self, *args, **kwargs):
        """
        Updates token data.

        Parameters
        ----------
            *args : tuple
                Positional arguments.
            **kwargs : dict
                Keyword arguments.
        """
        self.set_token(*args, **kwargs)

    def delete_section(self, section: str):
        """
        Deletes a section from the configuration file.

        Parameters
        ----------
            section : str
                The name of the section to delete.
        """
        logger.debug(f"Deleting section '{section}'.")
        self.config.remove_section(section)
        with open(self.filename, "w") as f:
            self.config.write(f)

    @property
    def is_logged_in(self) -> bool:
        """
        Checks whether there is a valid token present.

        Returns
        -------
        bool
            True if there is a valid token present, False otherwise.
        """
        logger.debug("Checking if logged in.")
        return bool(self.get_token().get("token"))

    @property
    def user_credentials(self) -> Dict[str, Optional[str]]:
        """
        Returns user credentials as a dictionary.

        Returns
        -------
        dict
            A dictionary of user credentials.
        """
        return {
            "email": self.get_login_details().get("email"),
            "password": self.get_login_details().get("password"),
        }


if __name__ == "__main__":
    # Works as expected
    logging.basicConfig(level=logging.DEBUG)
    config = Config()
    print(config.is_logged_in)
    config.save_auth_data(email="test@example.com", password="test123")
    config.update_tokens_data(token="abcdefg12345", expire_date="2024-06-09")
    print(config.is_logged_in)
