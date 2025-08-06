#!/usr/bin/env python3
"""
Main script for interacting with OpenAI API
Supports loading environment variables and calling completion API
Quiz solving functionality for math problems
"""

import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI

# initialize open ai client and provide completion behavior
class OpenAIClient:
    """General-purpose OpenAI client wrapper with API key management"""
    
    def __init__(self, api_key=None):
        """
        Initialize OpenAI client with API key
        
        Args:
            api_key: Optional API key. If not provided, loads from environment
        """
        if api_key is None:
            # In python 3, you can call a class static method via `self` but it is not ideal
            api_key = OpenAIClient._load_api_key_from_env()
        
        self.client = OpenAI(api_key=api_key)
        self.api_key = api_key
    
    @staticmethod
    def _load_api_key_from_env():
        """Load API key from environment variables"""
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in your .env file.")
        
        return api_key
    
    def get_completion(self, user_input, system_message="You are a helpful assistant.", **kwargs):
        """
        Get completion from OpenAI API with role-based conversation
        
        Args:
            user_input: User's input message
            system_message: System message to define assistant's role
            **kwargs: Additional parameters for the API call (model, temperature, max_tokens, etc.)
        
        Returns:
            str: Assistant's response
        """
        default_params = {
            "model": "gpt-3.5-turbo",
            "max_tokens": 1000,
            "temperature": 0.7
        }
        default_params.update(kwargs)
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_input}
                ],
                # unpacking dictionary
                **default_params
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error calling OpenAI API: {str(e)}"


class MathSolver:
    """Math problem solver using OpenAI client"""
    
    def __init__(self, openai_client):
        """
        Initialize math solver with an OpenAI client
        
        Args:
            openai_client: Instance of OpenAIClient
        """
        self.client = openai_client
    
    def solve_problem(self, question):
        """
        Solve a math problem and extract numerical answer
        
        Args:
            question: Math problem text
            
        Returns:
            tuple: (numerical_answer, full_response)
        """
        system_message = """
            I need you to switch your role to Math PHD, and using <<How to solve it >> math problem solving steps to solve the given math problem from user.
            Make sure to show your work clearly for each step and end with a clear statement of your final answer as a number.
        """
        
        try:
            ai_response = self.client.get_completion(
                question,
                system_message=system_message,
                model="gpt-3.5-turbo",
                max_tokens=500,
                temperature=0.1  # Lower temperature for more consistent math answers
            )
            
            ai_answer = MathSolver._extract_number_from_response(ai_response)
    
            return ai_answer, ai_response
        
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    @staticmethod
    def _extract_number_from_response(response):
        """Extract numerical answer from AI response"""
        # Look for numbers in the response, prioritizing the last number found
        numbers = re.findall(r'-?\d+\.?\d*', response)
        
        if numbers:
            try:
                # Try to convert the last number found to float
                return float(numbers[-1])
            except ValueError:
                pass
        return None




def load_quiz_questions(filename="questions.json"):
    """Load quiz questions from JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            questions = json.load(file)
        print(f"✓ Loaded {len(questions)} quiz questions")
        return questions
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {filename}")
        return []

def is_answer_correct(ai_answer, ground_truth, tolerance=0.01):
    """Check if AI answer matches ground truth within tolerance"""
    if ai_answer is None:
        return False
    try:
        return abs(float(ai_answer) - float(ground_truth)) <= tolerance
    except (ValueError, TypeError):
        return False

def run_quiz_evaluation(openai_client, questions):
    """Run the complete quiz evaluation process using OpenAIClient and MathSolver"""
    print("\n" + "="*80)
    print("QUIZ EVALUATION RESULTS")
    print("="*80)
    
    # Create math solver using the OpenAI client
    math_solver = MathSolver(openai_client)
    
    correct_count = 0
    total_questions = len(questions)
    
    for i, q in enumerate(questions, 1):
        question_id = q.get('id', i)
        question_text = q['question']
        ground_truth = q['ground_truth']
        
        print(f"\nQuestion {question_id}:")
        print(f"Q: {question_text}")
        
        # Get AI solution using the math solver
        ai_answer, ai_response = math_solver.solve_problem(question_text)
        
        # Check if correct
        is_correct = is_answer_correct(ai_answer, ground_truth)
        if is_correct:
            correct_count += 1
        
        # Format output
        ai_result_display = ai_answer if ai_answer is not None else "No answer extracted"
        actual_result_display = ground_truth
        match_status = "YES" if is_correct else "NO"
        
        print(f"AI result: {ai_result_display}, Actual result: {actual_result_display}")
        print(f"Is Matched: {match_status}")
        
        if ai_answer is None:
            print("AI Response snippet:", ai_response[:100] + "..." if len(ai_response) > 100 else ai_response)
        
        print("-" * 40)
    
    # Final statistics
    accuracy = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    
    print("\n" + "="*80)
    print("FINAL RESULTS")
    print("="*80)
    print(f"Total quizzes: {total_questions}")
    print(f"AI solved correctly: {correct_count}")
    print(f"Accuracy: {accuracy:.1f}%")
    print("="*80)
    
    return correct_count, total_questions, accuracy

def main():
    """Main function to run the script"""
    try:
        # Create OpenAI client (automatically loads API key from environment)
        print("Initializing OpenAI client...")
        openai_client = OpenAIClient()
        print("✓ OpenAI client initialized successfully")
        
        # Load quiz questions
        print("Loading quiz questions...")
        questions = load_quiz_questions()
        
        if not questions:
            print("No quiz questions loaded. Exiting.")
            return 1
        
        # Ask user what they want to do
        print("\nChoose an option:")
        print("1. Run quiz evaluation")
        print("2. Interactive chat")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            # Run quiz evaluation
            print("Starting quiz evaluation...")
            run_quiz_evaluation(openai_client, questions)
            
        elif choice == "2":
            # Interactive loop
            print("\n" + "="*50)
            print("OpenAI Chat Interface")
            print("Type 'quit' or 'exit' to end the session")
            print("="*50 + "\n")
            
            while True:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit']:
                    print("Goodbye!")
                    break
                
                if not user_input:
                    print("Please enter a message.")
                    continue
                
                print("Assistant: ", end="")
                response = openai_client.get_completion(user_input)
                print(response)
                print()
        
        elif choice == "3":
            print("Goodbye!")
            
        else:
            print("Invalid choice. Please run the script again.")
            return 1
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

def run_quiz_only():
    """Convenience function to run quiz evaluation directly"""
    try:
        # Create OpenAI client (automatically loads API key)
        openai_client = OpenAIClient()
        questions = load_quiz_questions()
        
        if not questions:
            print("No quiz questions loaded.")
            return
        
        # Run quiz evaluation directly
        run_quiz_evaluation(openai_client, questions)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    exit(main())