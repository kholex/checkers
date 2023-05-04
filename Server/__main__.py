"""Module for launching server."""
import asyncio

from Server.server import communicator


async def main():
    """Server launcher."""
    server = await asyncio.start_server(communicator, "0.0.0.0", 6000)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
