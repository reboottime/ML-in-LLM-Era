
import os
import json
import asyncio
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI
from agents import Agent, Runner, WebSearchTool

# load api key
load_dotenv()


async def fetch_answer(question: str) -> str:
    keyword_extractor_agent = Agent(
        name="Keyword Extractor",
        instructions="""
        You are a search keyword optimization expert. Extract 3-5 highly effective search keywords from user's question.
        Process:
        1. Identify core entities (people, places, organizations, products)
        2. Extract key concepts and technical terms
        3. Include time-sensitive modifiers (recent, latest, 2025) when relevant
        4. Add synonyms or alternative terms that improve search coverage
        5. Prioritize specific terms over generic ones

        Guidelines:
        - Focus on words that would appear in authoritative sources
        - Include proper nouns and specific terminology
        - Avoid stop words and overly broad terms
        - Consider both technical and common language variants

        Output format: Return exactly 3-5 keywords separated by spaces, no additional text.
        """,
        handoffs=[],
    )

    question_clarifier_agent = Agent(
        name="Question Clarifier",
        instructions="""
        You are a question clarification expert. Transform vague or unclear questions into precise, searchable queries.
        
        Your process:
        1. Identify the core information need behind the question
        2. Resolve ambiguous pronouns and unclear references
        3. Add necessary context from the original text
        4. Make the question specific and factual
        5. Ensure the question can be answered with current information

        Transformation rules:
        - Replace "this/that/it" with specific nouns
        - Add timeframe when relevant (recent, current, as of 2025)
        - Convert implied questions into explicit ones
        - Maintain the user's intent while improving clarity
        - Focus on factual, searchable information

        Output: Return only the clarified question as a single, well-formed sentence. No explanations or alternatives.
        """,
        handoffs=[],
    )

    search_agent = Agent(
        name="Web Search Expert",
        instructions="""
           You are a web search specialist. Use the provided keywords to find comprehensive, accurate information.
            Search strategy:
            1. Use keywords to find authoritative sources (official sites, news, academic)
            2. Prioritize recent and reliable information
            3. Cross-reference multiple sources when possible
            4. Focus on factual, verifiable content

            Response format requirements:
            - Provide exactly 3-5 key findings as a numbered list
            - Each point should be complete and standalone
            - Include specific details, dates, and figures when available
            - Separate points with "; " (semicolon and space)
            - Present as single string: "1. [detailed finding]; 2. [detailed finding]; 3. [detailed finding]"

            Quality standards:
            - Prioritize primary sources over secondary reporting
            - Include quantitative data when relevant
            - Note information recency (e.g., "as of 2025")
            - Avoid speculation or unverified claims
            """,
        tools=[WebSearchTool()],
    )

    qa_agent = Agent(
        name="Question Answer Expert",
        instructions="""
        You are a final answer synthesis expert. Create the best possible response using the clarified question and search results.

        Input analysis:
        1. Compare the original question to the clarified version to understand user intent
        2. Evaluate search results for relevance to the clarified question
        3. Identify the most authoritative and recent information
        4. Synthesize a complete answer that addresses the core user need

        Response creation:
        - Start with the most direct answer to the clarified question
        - Include supporting details and context
        - Maintain factual accuracy - never add unsupported information  
        - Use clear, accessible language appropriate for general audiences
        - Structure information logically (main answer first, then details)

        Quality checks:
        - Does this directly answer what the user wanted to know?
        - Is the information current and from reliable sources?
        - Would this response satisfy the user's information need?

        Output only the final answer - no meta-commentary about the process.
        """,
    )

    async def get_keywords_and_clarified_question(question: str) -> [str, str]:
        try:
            results = await asyncio.gather(
                Runner.run(keyword_extractor_agent, question),
                Runner.run(question_clarifier_agent, question),
            )
            
            print(results[0].final_output)
            print(results[1].final_output)

            return [results[0].final_output, results[1].final_output]
        except Exception as e:
            print(f"unexpected error: {e}")
            raise

    async def get_answer_to_question(question: str) -> str:
        try:
            (
                search_keywords,
                clarified_question,
            ) = await get_keywords_and_clarified_question(question)

            search_result = await Runner.run(search_agent, search_keywords)
            answers = search_result.final_output

            qa_result = await Runner.run(
                qa_agent,
                f"""
                    user original question: {question},
                    clarified question: {clarified_question},
                    answers: {answers}
            """,
            )

            return qa_result.final_output

        except Exception as e:
            print(f"unexpected error: {e}")
            raise

    answer = await get_answer_to_question(question)

    print(answer)

if __name__ == "__main__":
    asyncio.run(
        fetch_answer(
            # correct
            "熊信宽，艺名熊仔，是台湾饶舌创作歌手。2022年获得第33届金曲奖最佳作词人奖，2023年获得第34届金曲奖最佳华语专辑奖。请问熊仔的硕班指导教授为？"
            # "2005 播出的电视剧《终极一班》中，有一个高中生战力排行榜，称为「KO榜」，该榜榜首为？"
        )
    )
