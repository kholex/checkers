import asyncio
from Server.server import chat

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 6000)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
