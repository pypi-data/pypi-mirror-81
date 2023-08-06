import os
import importlib
import json
from typing import Union

from flask import Response
from flask.testing import Client
import pytest


@pytest.fixture
def app(service_module_name):
    # Ensure that test configuration will be loaded
    os.environ["SERVER_ENVIRONMENT"] = "test"
    service_module = importlib.import_module(service_module_name)
    service_module.application.testing = True
    service_module.application.config["PROPAGATE_EXCEPTIONS"] = False
    return service_module.application


def assert_201(response: Response, expected_location: str) -> str:
    """
    Assert that status code is 201.
    201 stands for Created, meaning that location header is expected as well.
    Assert that location header is containing the expected location (hostname trimmed for tests)

    :param response: response object from service to be asserted
    :param expected_location: Expected location starting from server root (eg: /xxx)
    :return Location from server root.
    """
    assert response.status_code == 201
    actual_location = response.headers["location"].replace("http://localhost", "")
    assert expected_location == actual_location
    return actual_location


def assert_file(response: Response, expected_file_path: str):
    """
    Assert that response is containing the bytes contained in expected file.

    :param response: Received query response.
    :param expected_file_path: Path to the file containing expected bytes.
    """
    with open(expected_file_path, "rb") as expected_file:
        assert response.data == expected_file.read()


def post_json(
    client: Client, url: str, json_body: Union[dict, list], **kwargs
) -> Response:
    """
    Send a POST request to this URL.

    :param client: Flask test client.
    :param url: Relative server URL (starts with /).
    :param json_body: Python structure corresponding to the JSON to be sent.
    :return: Received response.
    """
    return client.post(
        url, data=json.dumps(json_body), content_type="application/json", **kwargs
    )


def post_file(
    client: Client,
    url: str,
    file_name: str,
    file_path: str,
    additional_json: dict = None,
    **kwargs,
) -> Response:
    """
    Send a POST request to this URL.

    :param client: Flask test client.
    :param url: Relative server URL (starts with /).
    :param file_name: Name of the parameter corresponding to the file to be sent.
    :param file_path: Path to the file that should be sent.
    :param additional_json: Additional JSON to be sent in body.
    :return: Received response.
    """
    with open(file_path, "rb") as file:
        data = {file_name: (file, file_name)}
        if additional_json:
            data.update(additional_json)
        return client.post(url, data=data, **kwargs)


def put_json(
    client: Client, url: str, json_body: Union[dict, list], **kwargs
) -> Response:
    """
    Send a PUT request to this URL.

    :param client: Flask test client.
    :param url: Relative server URL (starts with /).
    :param json_body: Python structure corresponding to the JSON to be sent.
    :return: Received response.
    """
    return client.put(
        url, data=json.dumps(json_body), content_type="application/json", **kwargs
    )
