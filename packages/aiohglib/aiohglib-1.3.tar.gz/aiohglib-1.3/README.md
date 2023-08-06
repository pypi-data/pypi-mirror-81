# aiohglib

The aiohglib is an asynchronous variant of [hglib](https://www.mercurial-scm.org/wiki/PythonHglib), which is library with a fast, convenient interface to Mercurial. It uses Mercurial's command server for communication with hg.

The code itself takes advantage of asyncio library and async/await syntax.

Another difference against standard hglib is suport for timezones and changesets details like p1, p2 and extras.

## Basic usage

```python
import asyncio
import aiohglib

async def main():
    async with aiohglib.open(path) as client:
        log = await client.log(revrange="tip")
        print(log)

asyncio.run(main())
```

## Dependencies ##

* Python 3.6
* [pytz](https://pypi.org/project/pytz/)

## Licence ##

MIT

## Contact ##

Michal Šiška <michal.515k4@gmail.com>
