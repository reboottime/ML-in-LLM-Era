import os
import json
import asyncio
from typing import Any, Optional
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI
from agents import Agent, Runner, WebSearchTool, trace

load_dotenv()


@dataclass
class Question:
    content: str
    actual_answer: str

class Evaluation:
    def __init__(self):
        with open("./agents.json") as file:
            agent_settings = json.load(file)
            
            self.keyword_extractor_agent = Agent(
                name=agent_settings['keyword_extractor_agent']['name'],
                instructions=agent_settings['keyword_extractor_agent']['instructions'],
                handoffs=[]
            )
            
            self.question_clarifier_agent = Agent(
                name=agent_settings['question_clarifier_agent']['name'],
                instructions=agent_settings['question_clarifier_agent']['instructions'],
                handoffs=[]
            )
            
            self.search_agent = Agent(
                name=agent_settings['search_agent']['name'],
                instructions=agent_settings['search_agent']['instructions'],
                handoffs=[],
                tools=[WebSearchTool()]
            )
            
            self.qa_agent = Agent(
                name=agent_settings['qa_agent']['name'],
                instructions=agent_settings['qa_agent']['instructions']
            )
            
            self.evaluation_agent = Agent(
                name=agent_settings['evaluation_agent']['name'],
                instructions=agent_settings['evaluation_agent']['instructions']
            )

    async def get_llm_answer(self, question: Question) -> str:
        try:
            results = await asyncio.gather(
                Runner.run(self.keyword_extractor_agent, question.content),
                Runner.run(self.question_clarifier_agent, question.content)
            )
            search_keywords = results[0].final_output
            clarified_question = results[1].final_output

            search_result = await Runner.run(self.search_agent, f"""
                question: {clarified_question}
                keywords: {search_keywords}
            """)
            answers = search_result.final_output

            qa_result = await Runner.run(self.qa_agent, f"""
                The original question is: {question.content},
                The clarified question is: {clarified_question},
                The available answers: {answers}
            """)

            print()
            print(f"search keywords: {search_keywords}")
            print(f"clarified question: {clarified_question}")
            print(f"answers: {answers}")
            print(f"llm answer: {qa_result.final_output}")
            print(f"expected answer:{question.actual_answer}")
        
            return qa_result.final_output
        except Exception as e:
            print(f"Error happened: {e}")
            raise e

    async def get_llm_answer_score(self, question: Question, llm_answer: str) -> float:
        try:
            result = await Runner.run(self.evaluation_agent, f"""
                correct answer: {question.actual_answer},
                llm answer: {llm_answer}
            """)
            return float(result.final_output)
        except Exception as e:
            print(f'Error happened: {e}')
            raise e

    async def evaluate_question(self, question: Question) -> float:
        try:
            llm_answer = await self.get_llm_answer(question)
            llm_answer_score = await self.get_llm_answer_score(question, llm_answer)
            return llm_answer_score
        except Exception as e:
            print(f"{e}")
            raise e
        
    async def evaluate_questions(self, questions: list[Question], round_num: int = 3) -> list[list[float]]:
        if round_num <= 0:
            raise Exception('Please provide a correct evaluation round number')
        
        reports: list[list[float]] = []

        for question in questions:
            current_round = 1
            tasks = []
            results: list[float] = []
            total_score = 0.0
            accuracy: float = 0.0
            
            while current_round <= round_num:
                tasks.append(self.evaluate_question(question))
                current_round += 1
            
            results = await asyncio.gather(*tasks)
            
            for result in results:
                total_score += result

            accuracy = round(total_score / round_num, 2)
            question_report = [*results, accuracy]

            print()
            print(f'question: {question.content}')
            print(f"accuracy: {accuracy}")
            print()
            
            reports.append(question_report)

            await asyncio.sleep(1)

        return reports

    
if __name__ == "__main__":
    def load_questions () -> list[Question]:
       try:
            with open('./questions.json') as file:
                data = json.load(file)
                return [Question(content=item['content'], actual_answer=item['actual_answer']) for item in data]
       except Exception as e:
           print(f"Error:{e}")
           raise e

    questions = load_questions()
    evaluation = Evaluation()
    
    # tracing: https://openai.github.io/openai-agents-python/tracing/
    with trace('ML in LLM 2025 HW1'):
        results = asyncio.run(evaluation.evaluate_questions(questions))
    # write json reports
    with open("reports.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print('Evaluation test is done!')
 