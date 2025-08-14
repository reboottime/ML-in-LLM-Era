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
    welcome_agent = Agent(name="welcome agent", instructions="You are my frontdesk assitant. You are proffesional and helpful")
    executive_agent= Agent(name="executive agent", instructions="You are my executive assitant, you keep me accountable")
    
    guest_name="Walter White"
    message_to_welcome_agent ="I'm here to visit kate"
    message_to_executive_agent = "I have a appointment with Kate at 03:00 p.m"
    
    try:
        # unpacking tuple. A tuple is a fixed list
        welcome_result, executive_result = await asyncio.gather(
            Runner.run(welcome_agent, f"I'm {guest_name}. {message_to_welcome_agent}"),
            Runner.run(executive_agent, f"I'm {guest_name}, {message_to_executive_agent}")
        )
    
       print(welcome_result.final_output)
       print(executive_result.final_output)
    except Exception as e:
        print(f"Error happened: {e!r}")

if __name__ == "__main__":
    asyncio.run(run_test())