import asyncio
import os
import struct
import zlib
from os import PathLike
from typing import List

WIILOAD_VERSION_MAJOR = 0
WIILOAD_VERSION_MINOR = 5


async def upload(dol: bytes, argv: List[str], host: str, port: int = 4299):
    """
    Uploads a file it to a Wii.
    :param dol: The bytes of a file to upload to wii.
    :param argv: Arguments to send to wii. The first value is usually the name of the file.
    :param host: The Wii's hostname/ip
    :param port: The port that Homebrew Channel is listening at.
    :return:
    """

    c_data = zlib.compress(dol, 6)

    args = b"\x00".join(arg.encode("utf-8") for arg in argv)
    args += b"\x00"

    reader, writer = await asyncio.open_connection(host, port)

    writer.write(b"HAXX")
    writer.write(struct.pack("B", WIILOAD_VERSION_MAJOR))  # one byte, unsigned
    writer.write(struct.pack("B", WIILOAD_VERSION_MINOR))  # one byte, unsigned
    writer.write(struct.pack(">H", len(args)))  # bigendian, 2 bytes, unsigned
    writer.write(struct.pack(">L", len(c_data)))  # bigendian, 4 bytes, unsigned
    writer.write(struct.pack(">L", len(dol)))  # bigendian, 4 bytes, unsigned
    writer.write(c_data)
    writer.write(args)
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def upload_file(path: PathLike, argv: List[str], host: str, port: int = 4299):
    """
    Reads a file from disk and uploads it to a Wii.
    :param path: Path to a file to be uploaded.
    :param argv: Extra arguments to send to wii, after the name of the file.
    :param host: The Wii's hostname/ip
    :param port: The port that Homebrew Channel is listening at.
    :return:
    """

    with open(path, "rb") as f:
        dol = f.read()

    args = [os.path.basename(path)]
    args.extend(argv)

    return await upload(dol, args, host, port)
