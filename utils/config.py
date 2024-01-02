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

logger = logging.getLogger(__name__)


class Config:
    """
    A class that handles reading from and writing to a configuration file.

    Attributes:
        filename (str): The name of the configuration file. Defaults to 'config.ini'.
        config (configparser.ConfigParser): An instance of the `configparser.ConfigParser` class used to read and write INI files.
    """

    def __init__(self, filename="config.ini"):
        self.filename = filename
        self.config = (
            configparser.ConfigParser()
        )  # Initialize the config attribute here

        if not os.path.exists(self.filename):
            self._create_config()
        else:
            self.config.read(self.filename)

    def _create_config(self):
        """Create a default configuration file."""
        logger.debug("Creating new configuration file.")
        self.config["LOGIN"] = {}
        self.config["TOKEN"] = {}

    # check if config exitst with values for email and password
    def config_exists(self) -> bool:
        """Check if the configuration file has values for email and password."""
        logger.debug("Checking if configuration file exists.")
        return bool(self.get_login_details().get("email")) and bool(
            self.get_login_details().get("password")
        )

    def get_login_details(self):
        """Return login details as a dictionary."""
        logger.debug("Retrieving login details.")
        return {k: v for k, v in self.config["LOGIN"].items()}

    def set_login_details(self, *, email: str, password: str):
        """
        Set login details using email and password.

        Args:
            email (str): Email address.
            password (str): Password.

        Raises:
            AssertionError: If email or password are invalid keyword arguments.
        """
        logger.debug(f"Setting login details ({email}, {password}).")
        details = {"email": email, "password": password}
        for key, value in details.items():
            assert key in ["email", "password"], f"Invalid keyword argument '{key}'."

            self.config["LOGIN"].setdefault(key, "")
            self.config["LOGIN"][key] = value

        with open(self.filename, "w") as f:
            self.config.write(f)

    def get_token(self):
        """Return token information as a dictionary."""
        logger.debug("Retrieving token information.")
        return {k: v for k, v in self.config["TOKEN"].items()}

    def set_token(self, *, token: str, expire_date: str = ""):
        """
        Set token information using token and expiration date.

        Args:
            token (str): Token string.
            expire_date (str): Expiration date as a string.

        Raises:
            AssertionError: If token or expire_date are invalid keyword arguments.
        """
        logger.debug(f"Setting token information ({token}, {expire_date}).")
        token_info = {"token": token, "expire_date": expire_date}
        for key, value in token_info.items():
            assert key in ["token", "expire_date"], f"Invalid keyword argument '{key}'."

            self.config["TOKEN"].setdefault(key, "")
            self.config["TOKEN"][key] = value

        with open(self.filename, "w") as f:
            self.config.write(f)

    def save_auth_data(self, email: str, password: str):
        login_data = {"email": email, "password": password}
        self.set_login_details(**login_data)

    def load_auth_data(self):
        email = self.config["LOGIN"]["email"]
        password = self.config["LOGIN"]["password"]

        # Load tokens and expiration dates too
        token = self.config["TOKENS"].get("token", "")
        expiration_date = self.config["TOKENS"].get("expiration_date", "")

        return {
            "email": email,
            "password": password,
            "token": token,
            "expiration_date": expiration_date,
        }

    # # ItemsView(<Cookies[<Cookie token=bIdNwPGMpKERhHfaBsycCNbiDiWMWVundFsrClNMywqzNAcMIRSpHGmwpjYxFdAhIMPlPAXpOyImKicbqMhUfoJeJMtghmdfIaTqnloEetZesitFZKMppTnSjZCtdGjl for .huggingface.co />]>)
    # parse token from cookie response
    def update_cookies_data(self, cookies: dict):
        """Update the tokens section of the configuration file."""
        logger.debug("Updating cookies data.")
        cookies_dict = dict(cookies)  # Convert ItemsView to dictionary
        for key, value in cookies_dict.items():
            self.config["TOKENS"].setdefault(key, "")
            self.config["TOKENS"][key] = value

        with open(self.filename, "w") as f:
            self.config.write(f)

    def load_auth_data(self):
        """Load authentication data from the configuration file."""
        return {
            "email": self.get_login_details().get("email"),
            "password": self.get_login_details().get("password"),
        }

    def delete_section(self, section: str):
        """Delete a section from the configuration file."""
        logger.debug(f"Deleting section '{section}'.")
        self.config.remove_section(section)
        with open(self.filename, "w") as f:
            self.config.write(f)

    @property
    def is_logged_in(self):
        """Check whether there is a valid token present."""
        logger.debug("Checking if logged in.")
        return bool(self.get_token().get("token"))

    @property
    def user_credentials(self):
        """Return user credentials as a dictionary."""
        return {
            "email": self.get_login_details().get("email"),
            "password": self.get_login_details().get("password"),
        }


if __name__ == "__main__":
    # Works as expected
    logging.basicConfig(level=logging.DEBUG)
    config = Config()
    print(config.is_logged_in)
    config.set_login_details(email="test@example.com", password="test123")
    config.set_token(token="abcdefg12345", expire_date="2024-06-09")
    print(config.is_logged_in)
