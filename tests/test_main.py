import pytest
from mock import MagicMock, AsyncMock

from wiiload import __main__


@pytest.mark.parametrize("from_env", [False, True])
async def test_execute_args(mocker, monkeypatch, from_env):
    mock_upload_bytes = mocker.patch("wiiload.upload.upload_file", new_callable=AsyncMock)

    args = MagicMock()
    args.dol = "foo_file"
    args.rest = ["foo"]
    if from_env:
        args.wii = None
        monkeypatch.setenv("WIILOAD", "tcp:wii_ip")
    else:
        args.wii = "wii_ip"
        monkeypatch.delenv("WIILOAD", raising=False)

    # Run
    await __main__.execute_args(args)

    # Assert
    mock_upload_bytes.assert_awaited_once_with("foo_file", ["foo"], "wii_ip")


@pytest.mark.parametrize("missing", [False, True])
def test_get_wii_from_env_fail(monkeypatch, missing):
    if missing:
        expected_msg = '--wii not specified, and WIILOAD environment variable is missing'
        monkeypatch.delenv("WIILOAD", raising=False)
    else:
        expected_msg = "does not start with"
        monkeypatch.setenv("WIILOAD", "wrong env")

    with pytest.raises(RuntimeError, match=expected_msg):
        __main__.get_wii_from_env()
