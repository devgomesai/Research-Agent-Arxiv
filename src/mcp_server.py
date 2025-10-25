import asyncio
import os
from langchain_mcp_adapters.client import MultiServerMCPClient

async def mcp_client():

    client = MultiServerMCPClient({
        "arxiv": {
            "transport": "stdio",
            "command": "uv",
            "args": [
                "tool",
                "run",
                "arxiv-mcp-server",
                "--storage-path",
                "C:/arxiv_storage/", # Create a folder named as arxiv_storage in C drive
            ],
        }
    })

    return client

if __name__ == "__main__":
    asyncio.run(mcp_client())
