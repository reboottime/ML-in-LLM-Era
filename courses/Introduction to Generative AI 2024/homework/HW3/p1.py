# import the packages
import openai
import gradio as gr  # Package for creating web-based user interfaces for ML models
import json
import os
from typing import List, Dict, Tuple
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

## Read OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it before running the script.")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# You should see "Set ChatGPT API sucessfully!!" if nothing goes wrong.
try:
    # Test basic API connection first
    # response = client.chat.completions.create(
    #         model="gpt-3.5-turbo",
    #         messages = [{'role':'user','content': "test"}],
    #         max_tokens=1,
    # )
    # print("Set ChatGPT API sucessfully!!")
    
    # Example of a more complex request for summarization
    summary_response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            # removing `can` varies the content style
            {'role': 'system', 'content': 'You are an expert in making summaries. You can summarize content without losing core points. The summary content should be no more than 100 words.'},
            {'role': 'user', 'content': """Here are some of the biggest take-aways that I have learned from atomic habits.

Small Habits beat larger habits- If you increase or improve something by 1% every single day. Then you will be far off better than if you improve drastically. Compound interest is far off better trying to improve drastically.

Your Environment Matters- You can be disciplined or do anything that you want, however you need to change your environment that you are in. Like the quote goes "you are the result of the people you hang out the most with". If you are in an environment that makes your habit hard to do, then you are most likely not going to do your habit at all. If your environment works in your favor, then you will notice your habits are easier to do.

People who are disciplined are in less tempting situations- People who tend to be more disciplined, tend to not have to rely on discipline as they've made the idea of doing what they have to do easier than if they avoid it. They spend less time in tempting situations due to the fact that they made the hard habit so hard to do, to the point where they can do the habit that they need to do easier.

Make Good Habits Easy and Make Bad Habits Hard-If you want to make good habits easy then you need to follow these 4 rules. Make it super easy, make it pleasurable. Make your new habits super easy to do and make it fun to do. People follow dopamine, if you want to stick to new habits that seem hard, the first step is to make them easy and pleasurable. The opposite applies to bad habits. Make bad habits super hard and make a punishment that is something that you would not want to do. Like if you go and eat at a fast-food restaurant on the weekday, then clean your bathroom. It does not have to be a very severe punishment but rather something to deter you from that habit.

Start With the 2 Minute Rule- When you start a habit, start with the 2-minute rule. This rule applies that if you are going to start a new habit you want to focus on aiming for consistency rather than perfection. Do a new habit for 2 minutes, but then stop. Do it for 2 minutes every single day, then add more time that you spend on the habit. This is to master consistency first and showing up every day.

Find a trigger- All habits have a trigger, something that triggers you to start a bad habit or a new habit. Try to attach a new habit to a trigger that you already have. This is called Habit Stacking. Do you have a habit of drinking coffee, but you want to pray a little? Try drinking coffee but then praying a little. You then start to associate praying with after having some coffee. This allows you to apply a trigger to a habit that you want to have.

Habits are not formed by how many days but how many times- Your brain gets used to something based on the frequency that something is done. If you want to make a new habit happen, then focus on how many times that you do in a day. If you want to make a habit of washing your face after you wake up, try doing it a couple times a day. Pretend to go to sleep, then when you "wake up" wash your face.

Change your Identity- Your habits are votes towards an identity that you have. If you want to change your habits you first have to change how you view yourself. If you change your identity from not going to the gym, then start saying "I am a person who does workouts". Then when you do your workout, you are working on your identity. Each time that you do something that is aligned with that habit then you start behaving like the person that you want to become.

Sorry for this post being so long, if you guys want some more stuff, please let me know. I can send you a DM with other lessons from this book. I highly recommend this book to anyone who wants to start changing their habits or who wants to change their life for the better. This book is one of the best books on self-improvement."""}
        ],
        max_tokens=1000
    )
    
    print("Summary:", summary_response.choices[0].message.content)
except:
    print("There seems to be something wrong with your ChatGPT API. Please follow our demonstration in the slide to get a correct one.")