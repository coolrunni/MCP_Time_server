import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Configure how to start the server
server_params = StdioServerParameters(
    command="python",
    args=["server.py"]
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Get list of tools
            tools_response = await session.list_tools()
            tools = [tool.name for tool in tools_response.tools]
            print(f"Available tools: {tools}")

            # Ask user for timezone and time
            if "convert_time" in tools:
                print("\n--- Convert Time Between Locations ---")
                source_timezone = input("Enter source timezone (e.g., Asia/Kolkata): ")
                time_str = input("Enter time in HH:MM (24-hour format): ")
                target_timezone = input("Enter target timezone (e.g., America/New_York): ")

                result = await session.call_tool("convert_time", {
                    "source_timezone": source_timezone,
                    "time": time_str,
                    "target_timezone": target_timezone
                })

                print("\n🕒 Converted Time:")
                print(result.content[0].text)

            if "get_current_time" in tools:
                tz = input("\nEnter a timezone to get current time (or press Enter to skip): ").strip()
                if tz:
                    result = await session.call_tool("get_current_time", {"timezone": tz})
                    print("\n📍 Current Time:")
                    print(result.content[0].text)

if __name__ == "__main__":
    asyncio.run(run())
