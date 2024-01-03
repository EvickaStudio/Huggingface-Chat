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
    r"""
    Authentication manager for Hugging Face APIs.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A class managing authentication operations for Hugging Face services.

    ----

    Attributes
    ----------
    config : Config
        Object holding the configurations and settings.

    Methods
    -------
    set_up_authentication(email: str, password: str) -> bool
        Setups authentication using the given credentials and persists them into the configuration file.
    tear_down_authentication()
        Tears down the authentication by removing stored authentication info from the configuration file.
    authenticate() -> Optional[httpx.Client]
        Performs authentication using saved credentials and yields an authenticated HTTP client instance.

    Example
    -------
    >>> from auth.auth_manager import AuthenticationManager
    >>>
    >>> auth_manager = AuthenticationManager()
    >>> auth_manager.set_up_authentication(email, password)
    True
    >>> session = auth_manager.authenticate()
    """

    def __init__(self):
        """Creates instances needed for the Authentication Manager."""
        self.config = Config()

    def set_up_authentication(self, email: str, password: str) -> bool:
        """
        Setups authentication using the given credentials and persists them into the configuration file.

        Parameters
        ----------
        email : str
            User's email address
        password : str
            User's password

        Returns
        -------
        bool
            Indicates whether the setup was successful or not.
        """
        login = Login(email, password)

        if (
            login.sign_in_with_email()
        ):  # sign_in_with_email() returns True if authentication is successful
            cookies = login.get_cookies()

            # Persist email, password, and token inside the config file
            logger.debug("Persisting authentication data to config...")
            try:
                self.config.set_login_details(email=email, password=password)

                # Extract token from cookie response
                for cookie in cookies:
                    if cookie[0] == "token":
                        self.config.set_token(token=cookie[1])

                return True
            except Exception as e:
                logger.error(
                    f"Encountered unexpected error during saving credential data: {str(e)}"
                )
                return False
        else:
            logger.error("Failed to complete authentication.")
            return False

    def tear_down_authentication(self):
        """Removes stored authentication information from the configuration file."""
        self.config.delete_section("TOKENS")

    def authenticate(self) -> Optional[httpx.Client]:
        """
        Perform authentication using saved credentials and generates an authenticated HTTP client instance.

        Returns
        -------
        httpx.Client | None
            Instance of authenticated HTTP Client or None if authentication fails.
        """
        try:
            user_data = self.config.load_auth_data()

            return httpx.Client(
                auth=httpx.BasicAuth(user_data["email"], user_data["password"]),
                headers={"User-Agent": CONSTANTS["USER_AGENT"]},
                cookies=self.config.get_token(),
            )
        except FileNotFoundError:
            logger.warning(
                "Configuration file containing authentication data does not exist."
            )
            return None
        except KeyError as e:
            logger.warning(f"Missing key '{e}' within loaded authentication data.")
            return None
        except Exception as e:
            logger.error(f"Encountered unexpected exception: {str(e)}")
            return None
