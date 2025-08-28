from dotenv import load_dotenv
from groq import Groq
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from typing import List, Dict, TypedDict
from contextlib import AsyncExitStack
import json
import asyncio

load_dotenv()

class ToolDefinition(TypedDict):
    name: str
    description: str
    input_schema: dict

class MCP_ChatBot:

    def __init__(self):
        self.sessions: List[ClientSession] = []
        self.exit_stack = AsyncExitStack()
        self.groq = Groq()
        self.available_tools: List[ToolDefinition] = []
        self.tool_to_session: Dict[str, ClientSession] = {}

    async def connect_to_server(self, server_name: str, server_config: dict) -> None:
        try:
            server_params = StdioServerParameters(**server_config)
            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            read, write = stdio_transport
            session = await self.exit_stack.enter_async_context(ClientSession(read, write))
            await session.initialize()
            self.sessions.append(session)

            # List available tools
            response = await session.list_tools()
            tools = response.tools
            print(f"\nConnected to {server_name} with tools:", [t.name for t in tools])

            for tool in tools:
                self.tool_to_session[tool.name] = session
                self.available_tools.append({
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                })
        except Exception as e:
            print(f"Failed to connect to {server_name}: {e}")

    async def connect_to_servers(self):
        try:
            with open("server_config.json", "r") as file:
                data = json.load(file)

            servers = data.get("mcpServers", {})
            for server_name, server_config in servers.items():
                await self.connect_to_server(server_name, server_config)
        except Exception as e:
            print(f"Error loading server configuration: {e}")
            raise

    async def process_query(self, query):
        messages = [
            {'role': 'system', 'content': 'You are a helpful assistant with access to tools. Call tools directly.'},
            {'role': 'user', 'content': query}
        ]

        groq_tools = [{
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["input_schema"]
            }
        } for tool in self.available_tools]

        response = self.groq.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            tools=groq_tools,
            max_tokens=2024
        )

        process_query = True
        while process_query:
            choice = response.choices[0]
            message = choice.message

            # Normal assistant text output
            if hasattr(message, 'content') and message.content:
                print(message.content)
                process_query = False

            # Tool calls from assistant
            elif hasattr(message, 'tool_calls') and message.tool_calls:
                # Preserve assistant message with tool_calls
                assistant_tool_calls = []
                for tc in message.tool_calls:
                    assistant_tool_calls.append({
                        "id": getattr(tc, "id", None),
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    })
                messages.append({
                    "role": "assistant",
                    "content": message.content or "",
                    "tool_calls": assistant_tool_calls,
                })

                # Execute each tool
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args_raw = tool_call.function.arguments

                    # Parse arguments safely
                    parsed_args = tool_args_raw
                    if isinstance(parsed_args, str):
                        try:
                            parsed_args = json.loads(parsed_args)
                        except json.JSONDecodeError:
                            parsed_args = {}

                    print(f"Calling tool {tool_name} with args {parsed_args}")

                    try:
                        session = self.tool_to_session[tool_name]
                        result = await session.call_tool(tool_name, arguments=parsed_args)
                    except Exception as e:
                        print(f"Tool {tool_name} failed: {e}")
                        process_query = False
                        break

                    # Extract result content safely
                    if hasattr(result, 'content'):
                        if isinstance(result.content, dict):
                            content_text = json.dumps(result.content, indent=2)
                        else:
                            content_text = str(result.content)
                    else:
                        content_text = str(result)

                    messages.append({
                        "role": "tool",
                        "tool_call_id": getattr(tool_call, "id", None),
                        "content": content_text,
                    })

                # Get next model response
                response = self.groq.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=messages,
                    tools=groq_tools,
                    max_tokens=2024
                )
            else:
                process_query = False

    async def chat_loop(self):
        print("\nMCP Chatbot Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() == 'quit':
                    break

                await self.process_query(query)
                print("\n")
            except Exception as e:
                print(f"\nError: {e}")

    async def cleanup(self):
        await self.exit_stack.aclose()


async def main():
    chatbot = MCP_ChatBot()
    try:
        await chatbot.connect_to_servers()
        await chatbot.chat_loop()
    finally:
        await chatbot.cleanup()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nChatbot exited by user")
