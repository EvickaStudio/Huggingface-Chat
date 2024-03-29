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
import os

from auth.auth_manager import AuthenticationManager
from utils.config import Config

logging.basicConfig(level=logging.DEBUG)

try:
    config_obj = Config()

    if config_obj.config_exists():
        logging.info(f"Config exists: {str(config_obj.config_exists())}")

        token = config_obj.get_token()

        if token is not None and token != {"token": "", "expire_date": ""}:
            logging.info(f"Token found in config file: {token}")
            auth_manager = AuthenticationManager()
        else:  # If no token can be found, its starts a login process with email, password from file
            logging.info("No token found in config file, starting authentication.")
            login_details = config_obj.get_login_details()
            email = str(login_details.get("email"))
            password = str(login_details.get("password"))
            # delete config.ini
            os.remove("config.ini")
            auth_manager = AuthenticationManager()
            auth_manager.set_up_authentication(email, password)

            if auth_manager.set_up_authentication(email, password):
                logging.info("Login and token set up was successful.")

    else:
        logging.info("Config doesn't exist, setting up initial configurations.")
        email = "example@mail.com"
        password = "password123"
        auth_manager = AuthenticationManager()
        auth_manager.set_up_authentication(email, password)

except KeyError:
    logging.error("Login details missing in config file.")

# session = auth_manager.authenticate()
# logging.info(session)
