from dotenv import load_dotenv
from groq import Groq
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from typing import List
import asyncio
import nest_asyncio

nest_asyncio.apply()

load_dotenv()

class MCP_ChatBot:

    def __init__(self):
        # Initialize session and client objects
        self.session: ClientSession = None
        self.groq = Groq()
        self.available_tools: List[dict] = []

    async def process_query(self, query):
        messages = [{'role':'user', 'content':query}]
        response = self.groq.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            tools=self.available_tools,
            max_tokens=2024
        )
        process_query = True
        while process_query:
            assistant_content = []
            choice = response.choices[0]
            message = choice.message
            
            if hasattr(message, 'content') and message.content:
                print(message.content)
                assistant_content.append({'role': 'assistant', 'content': message.content})
                if not hasattr(message, 'tool_calls') or not message.tool_calls:
                    process_query = False
                    
            if hasattr(message, 'tool_calls') and message.tool_calls:
                for tool_call in message.tool_calls:
                    assistant_content.append({'role': 'assistant', 'content': None, 'tool_calls': [tool_call]})
                    messages.append({'role':'assistant', 'content': None, 'tool_calls': [tool_call]})
                    tool_id = tool_call.id
                    tool_args = tool_call.function.arguments
                    tool_name = tool_call.function.name
                    
                    # Parse tool arguments if they're a string
                    if isinstance(tool_args, str):
                        import json
                        try:
                            tool_args = json.loads(tool_args)
                        except json.JSONDecodeError:
                            tool_args = {}
    
                    print(f"Calling tool {tool_name} with args {tool_args}")
                    
                    # Call a tool
                    #result = execute_tool(tool_name, tool_args): not anymore needed
                                        # tool invocation through the client session
                    result = await self.session.call_tool(tool_name, arguments=tool_args)
                    # Extract the text content from the result
                    if hasattr(result, 'content') and hasattr(result.content, 'text'):
                        content_text = result.content.text
                    elif hasattr(result, 'content'):
                        content_text = str(result.content)
                    else:
                        content_text = str(result)
                    
                    messages.append({"role": "user", 
                                      "content": f"Tool result: {content_text}"})
                    response = self.groq.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=messages,
                        tools=self.available_tools,
                        max_tokens=2024
                    )
                    
                    choice = response.choices[0]
                    message = choice.message
                    if hasattr(message, 'content') and message.content and not hasattr(message, 'tool_calls'):
                        print(message.content)
                        process_query = False

    
    
    async def chat_loop(self):
        """Run an interactive chat loop"""
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
                print(f"\nError: {str(e)}")
    
    async def connect_to_server_and_run(self):
        # Create server parameters for stdio connection
        server_params = StdioServerParameters(
            command="uv",  # Executable
            args=["run", "mcp_server.py"],  # Optional command line arguments
            env=None,  # Optional environment variables
        )
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                self.session = session
                # Initialize the connection
                await session.initialize()
    
                # List available tools
                response = await session.list_tools()
                
                tools = response.tools
                print("\nConnected to server with tools:", [tool.name for tool in tools])
                
                self.available_tools = [{
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                } for tool in response.tools]
    
                await self.chat_loop()


async def main():
    chatbot = MCP_ChatBot()
    await chatbot.connect_to_server_and_run()
  

if __name__ == "__main__":
    asyncio.run(main())