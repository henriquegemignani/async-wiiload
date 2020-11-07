import asyncio
from asyncio import StreamReader

import pytest
from mock import AsyncMock

from wiiload import upload


@pytest.mark.asyncio
async def test_upload_bytes(tmpdir):
    uploaded_data = None
    expected_data = (b'HAXX\x00\x05\x00\x08\x00\x00\x00\x0c\x00\x00\x00\x04x\x9c3426\x01\x00'
                     b'\x01\xf8\x00\xcbme\x00that\x00')

    def client_connected_cb(reader: StreamReader, writer):
        nonlocal uploaded_data
        uploaded_data = reader.read()

    result = await asyncio.start_server(client_connected_cb, host="localhost")

    host, port = (None, None)
    for sock in result.sockets:
        addr = sock.getsockname()
        if len(addr) >= 2:
            host, port = addr[0:2]
            break

    await upload.upload_bytes(b"1234", ["me", "that"], host, port)
    assert uploaded_data is not None
    assert (await uploaded_data) == expected_data


@pytest.mark.asyncio
async def test_upload_file(tmpdir, mocker):
    mock_upload_bytes = mocker.patch("wiiload.upload.upload_bytes", new_callable=AsyncMock)

    path = tmpdir.join("somewhere.bin")
    path.write_binary(b"foobar")

    # Run
    await upload.upload_file(path, ["foo"], "localhost")

    # Assert
    mock_upload_bytes.assert_awaited_once_with(b"foobar", ["somewhere.bin", "foo"], "localhost", 4299)
