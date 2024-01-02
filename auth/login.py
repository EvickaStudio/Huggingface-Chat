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
from typing import Dict

import httpx

from auth.constants import CONSTANTS

logger = logging.getLogger(__name__)


class Login:
    """
    A class to handle user login to a Huggingface account via email.

    ...

    Attributes
    ----------
    email : str
        user's email address
    password : str
        user's password
    _client : httpx.Client
        HTTP client for making requests

    Methods
    -------
    get_cookies() -> Dict[str, str]:
        Returns a dictionary of cookie names and values from the last HTTP response.
    sign_in_with_email():
        Signs in to the Huggingface account using the provided email and password.
    """

    def __init__(self, email: str, password: str):
        """
        Constructs all the necessary attributes for the Login object.

        Parameters
        ----------
            email : str
                user's email address
            password : str
                user's password
        """
        self.email = email
        self.password = password
        self._client = httpx.Client(
            auth=httpx.BasicAuth(email, password),
            headers={"User-Agent": CONSTANTS["USER_AGENT"]},
        )

    def get_cookies(self) -> Dict[str, str]:
        """
        Returns a dictionary of cookie names and values from the last HTTP response.

        Returns
        -------
        dict
            A dictionary of cookie names and values.
        """
        return dict(self._client.cookies.items())

    def sign_in_with_email(self) -> bool:
        """
        Signs in to the Huggingface account using the provided email and password.

        Raises
        ------
        httpx.HTTPStatusError
            If the HTTP response status code is not 302 (Redirection), an error is raised.

        Returns
        -------
        bool
            True if login is successful, False otherwise.
        """
        data = {"username": self.email, "password": self.password}
        response = self._client.post(url=CONSTANTS["LOGIN_URL"], data=data)
        if response.status_code != 302:
            raise httpx.HTTPStatusError(
                f"Login failed with status code {response.status_code}"
            )
        logger.debug("Login successful")
        return True
