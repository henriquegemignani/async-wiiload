from __future__ import annotations

import argparse
import asyncio
import os
from pathlib import Path

from wiiload import upload


def create_parser():
    parser = argparse.ArgumentParser("wiiload")
    parser.add_argument(
        "--wii",
        help="The hostname of the Wii to upload to. "
        "Defaults to using the WIILOAD environment variable.",
    )
    parser.add_argument("dol", type=Path, help="Path to the dol to upload.")
    parser.add_argument("rest", nargs=argparse.REMAINDER)
    return parser


def get_wii_from_env():
    wiiload_env = os.getenv("WIILOAD")
    if wiiload_env is None:
        raise RuntimeError(
            "--wii not specified, and WIILOAD environment variable is missing"
        )

    if wiiload_env.startswith("tcp:"):
        return wiiload_env[4:]
    else:
        raise RuntimeError(
            f"WIILOAD environment variable ({wiiload_env}) does not start with `tcp:`"
        )


async def execute_args(args):
    wii = args.wii
    if wii is None:
        wii = get_wii_from_env()
    await upload.upload_file(args.dol, args.rest, wii)


async def main():
    args = create_parser().parse_args()
    await execute_args(args)


if __name__ == "__main__":
    asyncio.run(main())
