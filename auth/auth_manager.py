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
from typing import Optional

import httpx

from auth.constants import CONSTANTS
from auth.login import Login
from utils.config import Config

logger = logging.getLogger(__name__)


class AuthenticationManager:
    """
    A class to manage authentication operations.

    ...

    Attributes
    ----------
    config : Config
        configuration object to manage application settings

    Methods
    -------
    set_up_authentication(email: str, password: str):
        Sets up authentication using given credentials and saves them to the configuration file.
    tear_down_authentication():
        Deletes stored authentication information from the configuration file.
    authenticate() -> Optional[httpx.Client]:
        Authenticates using previously saved credentials and returns an authenticated HTTP client.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the AuthenticationManager object.
        """
        self.config = Config()

    def set_up_authentication(self, email: str, password: str):
        """
        Sets up authentication using given credentials and saves them to the configuration file.

        Parameters
        ----------
            email : str
                user's email address
            password : str
                user's password
        """
        login = Login(email, password)
        if (
            login.sign_in_with_email()
        ):  # sign_in_with_email() returns True if authentication is successful
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
        else:
            logger.error("Authentication failed.")

    def tear_down_authentication(self):
        """
        Deletes stored authentication information from the configuration file.
        """
        self.config.delete_section("TOKENS")

    def authenticate(self) -> Optional[httpx.Client]:
        """
        Authenticates using previously saved credentials and returns an authenticated HTTP client.

        Returns
        -------
        httpx.Client
            An authenticated HTTP client, or None if authentication fails.
        """
        try:
            user_data = self.config.load_auth_data()
            return httpx.Client(
                auth=httpx.BasicAuth(user_data["email"], user_data["password"]),
                headers={"User-Agent": CONSTANTS["USER_AGENT"]},
                cookies=self.config.get_token(),
            )
        except FileNotFoundError:
            logger.warning("No authentication data found.")
            return None
        except KeyError as e:
            logger.warning(f"Missing key in authentication data: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            return None
