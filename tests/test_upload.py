from __future__ import annotations

import io
from unittest.mock import AsyncMock, MagicMock

import wiiload


async def test_upload_bytes(unused_tcp_port, mocker):
    result = io.BytesIO()

    reader = AsyncMock()
    writer = AsyncMock()
    writer.write = result.write
    writer.close = MagicMock()
    mock_open_connection = mocker.patch(
        "asyncio.open_connection", new_callable=AsyncMock, return_value=(reader, writer)
    )

    expected_data = (
        b"HAXX\x00\x05\x00\x08\x00\x00\x00\x0c\x00\x00\x00\x04x\x9c3426\x01\x00"
        b"\x01\xf8\x00\xcbme\x00that\x00"
    )

    await wiiload.upload_bytes(b"1234", ["me", "that"], "localhost", unused_tcp_port)
    assert result.getvalue() == expected_data

    mock_open_connection.assert_awaited_once_with("localhost", unused_tcp_port)
    writer.drain.assert_awaited_once_with()
    writer.close.assert_called_once_with()
    writer.wait_closed.assert_awaited_once_with()


async def test_upload_file(tmp_path, mocker):
    mock_upload_bytes = mocker.patch(
        "wiiload.upload.upload_bytes", new_callable=AsyncMock
    )

    path = tmp_path.joinpath("somewhere.bin")
    path.write_bytes(b"foobar")

    # Run
    await wiiload.upload_file(path, ["foo"], "localhost")

    # Assert
    mock_upload_bytes.assert_awaited_once_with(
        b"foobar", ["somewhere.bin", "foo"], "localhost", 4299
    )
