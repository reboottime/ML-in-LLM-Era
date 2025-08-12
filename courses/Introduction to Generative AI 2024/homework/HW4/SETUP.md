# Setup Instructions

## Environment Setup

1. **Virtual Environment**: A Python virtual environment has been created in the `venv/` directory.

2. **Dependencies**: Install the required packages using:

   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Environment Variables**:
   - Copy the content from `env_template.txt` to create a `.env` file
   - Replace `your_openai_api_key_here` with your actual OpenAI API key

## Usage

### Basic Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Run the main script
python main.py
```

### Features

- **Environment Variable Loading**: Automatically loads `OPENAI_API_KEY` from `.env` file
- **OpenAI API Integration**: Uses the latest OpenAI Python client
- **Role-based Conversation**: Supports system and user roles
- **Interactive Chat**: Command-line interface for real-time interaction
- **Quiz Evaluation**: Automated math problem solving with AI and result comparison
- **Answer Extraction**: Smart number extraction from AI responses
- **Statistics Tracking**: Accuracy calculation and detailed results logging
- **Error Handling**: Graceful error handling for API calls

### Architecture Overview

The codebase follows a clean separation of concerns:

#### OpenAIClient Class
General-purpose OpenAI API client with minimal responsibilities:

**Initialization:**
```python
# Automatic API key loading from environment
client = OpenAIClient()

# Manual API key specification
client = OpenAIClient(api_key="your_api_key_here")
```

**Methods:**
- `get_completion(user_input, system_message, **kwargs)`: General completion API with customizable parameters

#### MathSolver Class
Domain-specific class for mathematical problem solving:

**Initialization:**
```python
openai_client = OpenAIClient()
math_solver = MathSolver(openai_client)
```

**Methods:**
- `solve_problem(question)`: Solve math problems and extract numerical answers
- `_extract_number_from_response(response)`: Extract numbers from AI responses (internal)

#### Utility Functions
- `load_quiz_questions(filename)`: Loads quiz questions from JSON file
- `run_quiz_evaluation(openai_client, questions)`: Orchestrates complete quiz evaluation
- `run_quiz_only()`: Convenience function for direct quiz evaluation

### Quiz Evaluation Usage

When you run the script, you'll get a menu:

1. **Run quiz evaluation** - Automatically processes all 30 math questions
2. **Interactive chat** - Regular chat interface
3. **Exit**

### Output Format

For each question, the output shows:

```
Question 1:
Q: [Question text]
AI result: [AI's numerical answer], Actual result: [Ground truth]
Is Matched: YES/NO
```

Final summary includes:

- Total quizzes count
- Number of correct answers
- Accuracy percentage

### Example Usage in Code

**Quick Quiz Evaluation:**

```python
from main import run_quiz_only

# Run quiz evaluation directly
run_quiz_only()
```

**Using the Separated Architecture:**

```python
from main import OpenAIClient, MathSolver, load_quiz_questions

# 1. Initialize general OpenAI client
openai_client = OpenAIClient()  # Auto-loads API key from .env
# or: openai_client = OpenAIClient(api_key="your_api_key_here")

# 2. Create domain-specific solver
math_solver = MathSolver(openai_client)

# 3. Use for math problems
questions = load_quiz_questions()
ai_answer, ai_response = math_solver.solve_problem(questions[0]['question'])
print(f"AI Answer: {ai_answer}")

# 4. Use OpenAI client for general tasks
response = openai_client.get_completion(
    "What is 2+2?", 
    system_message="You are a helpful math tutor."
)
print(response)

# 5. Custom parameters
response = openai_client.get_completion(
    "Write a poem", 
    temperature=0.9,
    max_tokens=200
)
```

**Full Quiz Evaluation:**

```python
from main import OpenAIClient, load_quiz_questions, run_quiz_evaluation

openai_client = OpenAIClient()
questions = load_quiz_questions()
correct, total, accuracy = run_quiz_evaluation(openai_client, questions)
print(f"Accuracy: {accuracy:.1f}%")
```
