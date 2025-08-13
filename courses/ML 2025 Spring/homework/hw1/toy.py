import os
import json
import asyncio
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI
from agents import Agent, Runner

# load api key
load_dotenv()

async def run_test():
    welcome_agent = Agent(name="welcome agent", instructions="You are my executive assitant. You are proffesional and helpful")
    result = await Runner.run(welcome_agent, "I'm Walter White. I'm here to visit Kate")
    
    try:
       print(result.final_output)
    except Exception as e:
        print(f"Error happened: {e!r}")

if __name__ == "__main__":
    asyncio.run(run_test())