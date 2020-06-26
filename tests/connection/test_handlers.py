import time
import pytest

from peerpy import Peer
from ..utils import with_peers
from .conftest import data_test


@pytest.fixture
@with_peers
def peers():
    def set_connection_handler(connection):
        def check_data(data):
            assert data == data_test

        connection.handlers["data"] = check_data
        return True

    return [{}, {"handlers": {"connection": set_connection_handler}}]


def test_data_handler(peers):
    """Tests a peer's connection & data handlers"""
    connection = peers[0].connect(peers[1].address_name)
    connection.send(data_test)

    time.sleep(.1)

    assert peers[1].connections[peers[0].address_name].thread.is_alive()
