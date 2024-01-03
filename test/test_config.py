# pytest test/test_config.py

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

import os

import pytest

from utils.config import Config

# Constants for test
CONFIG_FILE = "test_config.ini"
VALID_EMAIL = "test@example.com"
VALID_PASSWORD = "securepassword123"
VALID_TOKEN = "sometoken"
VALID_EXPIRE_DATE = "2024-06-09"


@pytest.fixture
def config():
    # Ensure any existing test config is removed before each test
    if os.path.exists(CONFIG_FILE):
        os.unlink(CONFIG_FILE)
    return Config(filename=CONFIG_FILE)


@pytest.mark.parametrize(
    "email, password, token, expire_date, test_id",
    [
        (
            VALID_EMAIL,
            VALID_PASSWORD,
            VALID_TOKEN,
            VALID_EXPIRE_DATE,
            "valid_credentials_and_token",
        ),
        ("", VALID_PASSWORD, VALID_TOKEN, VALID_EXPIRE_DATE, "empty_email"),
        (VALID_EMAIL, "", VALID_TOKEN, VALID_EXPIRE_DATE, "empty_password"),
        (VALID_EMAIL, VALID_PASSWORD, "", VALID_EXPIRE_DATE, "empty_token"),
        (VALID_EMAIL, VALID_PASSWORD, VALID_TOKEN, "", "empty_expire_date"),
        (None, VALID_PASSWORD, VALID_TOKEN, VALID_EXPIRE_DATE, "none_email"),
        (VALID_EMAIL, None, VALID_TOKEN, VALID_EXPIRE_DATE, "none_password"),
        (VALID_EMAIL, VALID_PASSWORD, None, VALID_EXPIRE_DATE, "none_token"),
        (VALID_EMAIL, VALID_PASSWORD, VALID_TOKEN, None, "none_expire_date"),
    ],
)
def test_config_operations(config, email, password, token, expire_date, test_id):
    # Arrange
    expected_login = {"email": email, "password": password}
    expected_token = {"token": token, "expire_date": expire_date}

    # Act
    if email is not None and password is not None:
        config.set_login_details(email=email, password=password)
    if token is not None and expire_date is not None:
        config.set_token(token=token, expire_date=expire_date)

    # Assert
    assert (
        config.get_login_details() == expected_login
    ), f"Failed on {test_id}: Login details mismatch"
    assert (
        config.get_token() == expected_token
    ), f"Failed on {test_id}: Token details mismatch"
    assert config.is_logged_in == bool(
        token
    ), f"Failed on {test_id}: is_logged_in check failed"
    assert (
        config.user_credentials == expected_login
    ), f"Failed on {test_id}: User credentials mismatch"


@pytest.mark.parametrize(
    "section, test_id",
    [
        ("LOGIN", "delete_login_section"),
        ("TOKEN", "delete_token_section"),
        ("NON_EXISTENT", "delete_non_existent_section"),
    ],
)
def test_delete_section(config, section, test_id):
    # Arrange
    config.set_login_details(email=VALID_EMAIL, password=VALID_PASSWORD)
    config.set_token(token=VALID_TOKEN, expire_date=VALID_EXPIRE_DATE)

    # Act
    config.delete_section(section)

    # Assert
    if section in config.config.sections():
        assert False, f"Failed on {test_id}: Section {section} was not deleted"


@pytest.mark.parametrize(
    "key, value, exception, test_id",
    [
        ("email", VALID_EMAIL, None, "valid_email"),
        ("password", VALID_PASSWORD, None, "valid_password"),
        ("token", VALID_TOKEN, None, "valid_token"),
        ("expire_date", VALID_EXPIRE_DATE, None, "valid_expire_date"),
        ("invalid_key", "some_value", AssertionError, "invalid_login_key"),
        ("invalid_key", "some_value", AssertionError, "invalid_token_key"),
    ],
)
def test_set_details_with_invalid_keys(config, key, value, exception, test_id):
    # Act / Assert
    if exception:
        with pytest.raises(exception):
            if test_id.startswith("invalid_login"):
                config.set_login_details(**{key: value})
            else:
                config.set_token(**{key: value})
    else:
        if test_id.startswith("valid_email") or test_id.startswith("valid_password"):
            config.set_login_details(**{key: value})
            assert (
                config.get_login_details()[key] == value
            ), f"Failed on {test_id}: Login detail {key} was not set correctly"
        else:
            config.set_token(**{key: value})
            assert (
                config.get_token()[key] == value
            ), f"Failed on {test_id}: Token detail {key} was not set correctly"
