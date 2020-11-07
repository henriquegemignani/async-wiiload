# async-wiiload

This package implements the Wiiload client side, using asyncio sockets.

See Wiibrew's [Wiiload](http://wiibrew.org/wiki/Wiiload) for more details.



## Usage

```python

import wiiload
await wiiload.upload_file("homebrew.dol", [], "192.168.1.2")

```