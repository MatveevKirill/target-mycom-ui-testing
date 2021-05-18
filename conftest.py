import os
import shutil
import logging
import pytest
from _pytest.fixtures import FixtureRequest

from ui.fixtures import *
from ui.fixtures_data import *


def pytest_configure(config):
    abs_path = os.path.abspath(os.curdir)

    base_test_dir = os.path.join(abs_path, "tmp", "tests")

    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_test_dir):
            shutil.rmtree(base_test_dir)
        os.makedirs(base_test_dir)

    config.abs_path = abs_path
    config.base_test_dir = base_test_dir


def pytest_addoption(parser) -> None:
    parser.addoption("--timeout-limit", default=15)
    parser.addoption('--debugging', action="store_true")


@pytest.fixture(scope="session")
def abs_path(request) -> str:
    return request.config.abs_path


@pytest.fixture(scope="function")
def test_dir(request: FixtureRequest) -> str:
    test_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')
    test_dir = os.path.join(request.config.base_test_dir, test_name)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope="session")
def configuration(request: FixtureRequest) -> dict:
    timeout_limit = float(request.config.getoption("--timeout-limit"))
    debugging = request.config.getoption("--debugging")

    return {
        "timeout_limit": timeout_limit,
        "debugging": debugging
    }


@pytest.fixture(scope="function", autouse=True)
def logger(test_dir: str, configuration: dict) -> logging.Logger:
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-15s - %(levelname)-6s - %(message)s')
    log_file = os.path.join(test_dir, 'test.log')
    log_level = logging.DEBUG if configuration['debugging'] else logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('pytest-logger')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

    with open(log_file, 'r') as f:
        allure.attach(f.read(), 'test.log', attachment_type=allure.attachment_type.TEXT)