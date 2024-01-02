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

logger = logging.getLogger(__name__)


class Login:
    """Handles signing in via email."""

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self._client = httpx.Client(
            auth=httpx.BasicAuth(email, password),
            headers={"User-Agent": CONSTANTS["USER_AGENT"]},
        )

    def get_cookies(self) -> dict:
        """Returns cookie values from the last HTTP response."""
        return self._client.cookies.items()

    def sign_in_with_email(self):
        """Signs in using specified email and password."""
        data = {"username": self.email, "password": self.password}
        response = self._client.post(url=CONSTANTS["LOGIN_URL"], data=data)
        if response.status_code != 302:
            raise httpx.HTTPStatusError(
                f"Login failed with status code {response.status_code}"
            )
        logger.debug("Login successful")
