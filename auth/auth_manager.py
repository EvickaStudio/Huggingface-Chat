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

import logging

import httpx

from auth.constants import CONSTANTS
from auth.login import Login
from utils.config import Config

logger = logging.getLogger(__name__)


class AuthenticationManager:
    """Manages authentication operations."""

    def __init__(self):
        self.config = Config()

    def set_up_authentication(self, email: str, password: str):
        """Sets up authentication using given credentials."""
        login = Login(email, password)
        login.sign_in_with_email()

        # Retrieve the tokens and expiration dates
        cookies = login.get_cookies()

        # Save the email, password and token to the config file
        logger.debug("Writing authentication data to config file.")
        try:
            self.config.set_login_details(email=email, password=password)
            # extract token from cookie response
            for cookie in cookies:
                if cookie[0] == "token":
                    self.config.set_token(token=cookie[1])
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")

    def tear_down_authentication(self):
        """Deletes stored authentication information."""
        self.config.delete_section("TOKENS")

    def authenticate(self):
        """Authenticates using previously saved credentials."""
        try:
            user_data = self.config.load_auth_data()
            client = httpx.Client(
                auth=httpx.BasicAuth(user_data["email"], user_data["password"]),
                headers={"User-Agent": CONSTANTS["USER_AGENT"]},
                cookies=self.config.get_token(),
            )
            return client
        except FileNotFoundError:
            logger.warning("No authentication data found.")
            return None
        except KeyError as e:
            logger.warning(f"Missing key in authentication data: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            return None
