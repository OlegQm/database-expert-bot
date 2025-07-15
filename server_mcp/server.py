import logging
from typing import Any, AsyncGenerator
from contextlib import asynccontextmanager

from fastmcp import FastMCP

from server_mcp.tools.postgresql_schema import (
    postgresql_tool,
    postgres_get_structure,
    postgres_get_table_details,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MCP Lifespan:

async def initialize_mcp_tools():
    """Initialize MCP tools at startup"""
    logger.info("Initializing MCP tools...")
    await postgresql_tool.initialize()
    logger.info("MCP tools initialized.")
    
async def close_mcp_tools():
    """Close MCP tools at shutdown"""
    logger.info("Closing MCP tools...")
    await postgresql_tool.close()
    logger.info("MCP tools closed.")

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncGenerator[Any, Any]:
    """Manage application lifecycle with type-safe context"""
    await initialize_mcp_tools()
    yield
    await close_mcp_tools()

# MCP Tools Registration:

mcp = FastMCP("Stubarag MCP Server", lifespan=app_lifespan)

mcp.tool(postgres_get_structure)
mcp.tool(postgres_get_table_details)

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8070)
