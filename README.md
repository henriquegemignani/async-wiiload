# async-wiiload
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fhenriquegemignani%2Fasync-wiiload.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fhenriquegemignani%2Fasync-wiiload?ref=badge_shield)


This package implements the Wiiload client side, using asyncio sockets.

See Wiibrew's [Wiiload](http://wiibrew.org/wiki/Wiiload) for more details.



## Usage

```python

import wiiload
await wiiload.upload_file("homebrew.dol", [], "192.168.1.2")

```

## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fhenriquegemignani%2Fasync-wiiload.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fhenriquegemignani%2Fasync-wiiload?ref=badge_large)