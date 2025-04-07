from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from .server import TimeServer
import json, logging

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("MCP-Time")

    mcp = FastMCP("MCP-Time-Server")
    time_server = TimeServer()

    @mcp.tool()
    def get_current_time(timezone: str) -> TextContent:
        result = time_server.get_current_time(timezone)
        return TextContent(type="text", text=json.dumps(result.model_dump(), indent=2))

    @mcp.tool()
    def convert_time(source_timezone: str, time: str, target_timezone: str) -> TextContent:
        result = time_server.convert_time(source_timezone, time, target_timezone)
        return TextContent(type="text", text=json.dumps(result.model_dump(), indent=2))

    logger.info("Running MCP Time Server...")
    mcp.run()
