from pathlib import Path
import os
import random

from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client

from autogen import ConversableAgent, LLMConfig
from autogen.agentchat import AssistantAgent
from autogen.mcp import create_toolkit

from autogen.agentchat import initiate_group_chat, a_initiate_group_chat
from autogen.agentchat.group.patterns import AutoPattern

# Only needed for Jupyter notebooks
import nest_asyncio

nest_asyncio.apply()


async def create_toolkit_and_run(session: ClientSession) -> None:
    # Create a toolkit with available MCP tools
    toolkit = await create_toolkit(session=session)

    llm_config = LLMConfig(
        api_type="openai",
        model="gpt-4o-mini",
        api_key=os.environ.get("OPENAI_API_KEY"),
        temperature=0.2,
    )
    with llm_config:
        data_bot = ConversableAgent(
            name="data_bot",
            system_message="You are a data bot. You should use the tools available to you to load the user's questions from the database of json files.",
        )
        assistant_bot = ConversableAgent(
            name="assistant_bot",
            system_message="You are a code assistant. You should use the tools available to you to answer the user's questions provided by the data_bot.",
        )
    # Register MCP tools with the agent
    toolkit.register_for_llm(data_bot)
    toolkit.register_for_execution(data_bot)

    toolkit.register_for_llm(assistant_bot)
    toolkit.register_for_execution(assistant_bot)

    initial_prompt = (
        "Please provide answers to the questions provided in the json files."
    )

    # Create pattern and start group chat
    pattern = AutoPattern(
        initial_agent=data_bot,
        agents=[data_bot, assistant_bot],
        group_manager_args={"llm_config": llm_config},
    )

    result, _, _ = await a_initiate_group_chat(
        pattern=pattern,
        messages=initial_prompt,
    )
    await result.process()


async def main(server_params):
    async with stdio_client(server_params) as (read, write), ClientSession(
        read, write
    ) as session:
        # Initialize the connection
        await session.initialize()
        await create_toolkit_and_run(session)


if __name__ == "__main__":
    # Get the path to the MCP server script
    mcp_server_path = "mcp_server.py"

    server_params = StdioServerParameters(
        command="python",  # The command to run the server
        args=[
            str(mcp_server_path),
            "stdio",
        ],  # Path to server script and transport mode
    )

    # Run the main function
    import asyncio

    asyncio.run(main(server_params=server_params))
