import multiprocessing
import subprocess
import time

import pytest

from client.network import ClientConnection
from server.network import ServerConnection
from utils.utils import ip_address_is_valid


def run_server():
    server = ServerConnection()
    server.start_listening()


def run_client():
    client = ClientConnection()

    client.start_connection()

    message = "Hello Server!"
    client.send_message(message)

    time.sleep(1)
    client.close_connection()


@pytest.fixture
def good_ip():
    return "127.0.0.1"


@pytest.fixture
def bad_ip_upper():
    return "256.256.256.256"


@pytest.fixture
def bad_ip_lower():
    return "0.-1.-1.-1"


def test_connection():
    pserver = multiprocessing.Process(target=run_server)
    pserver.start()

    time.sleep(1)
    run_client()
    time.sleep(1)

    pserver.kill()
    pserver.join()


def test_user_input(good_ip, bad_ip_upper, bad_ip_lower):
    assert ip_address_is_valid(good_ip)
    assert not ip_address_is_valid(bad_ip_upper)
    assert not ip_address_is_valid(bad_ip_lower)
