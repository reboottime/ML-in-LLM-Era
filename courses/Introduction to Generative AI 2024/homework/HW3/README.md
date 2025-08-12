# HW3 - Generative AI Application

This project demonstrates the use of OpenAI's API with a web-based interface using Gradio.

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key

## 🚀 Quick Start

### 1. Clone/Navigate to the Project

```bash
cd "Introduction to Generative AI 2024/homework/HW3"
```

### 2. Create and Activate Virtual Environment

#### On macOS/Linux

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

#### On Windows

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

#### Option A: Using .env file (Recommended)

1. Create a `.env` file in the project directory:

   ```bash
   touch .env
   ```

2. Add your OpenAI API key to the `.env` file:

   ```bash
   OPENAI_API_KEY=your-actual-api-key-here
   ```

#### Option B: Set environment variable directly

```bash
export OPENAI_API_KEY="your-actual-api-key-here"
```

### 5. Run the Application

```bash
python main.py
```

## 📦 Package Information

The project uses the following key packages:

- **openai** - Official OpenAI Python client for API interactions
- **gradio** - Package for creating web-based user interfaces for ML models
- **python-dotenv** - Package for loading environment variables from .env files

## 🔧 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure the virtual environment is activated and packages are installed:

   ```bash
   source venv/bin/activate  # On macOS/Linux
   pip install -r requirements.txt
   ```

2. **API Key Error**: Ensure your OpenAI API key is correctly set:
   - Check if the `.env` file exists and contains the correct key
   - Verify the key is valid and has sufficient credits

3. **Permission Errors**: Make sure you have proper permissions to install packages:

   ```bash
   pip install --user -r requirements.txt
   ```

### Expected Output

When everything is set up correctly, you should see:

```
Set ChatGPT API sucessfully!!
```

## 🛡️ Security Notes

- **Never commit your `.env` file** to version control
- The `.env` file is already added to `.gitignore` for security
- Keep your OpenAI API key private and secure

## 📁 Project Structure

```md
HW3/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .env                # Environment variables (create this)
├── venv/               # Virtual environment (created by you)
```

## 🆘 Getting Help

If you encounter any issues:

1. Check that all dependencies are installed correctly
2. Verify your OpenAI API key is valid
3. Ensure the virtual environment is activated
4. Check the troubleshooting section above

## 📚 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Gradio Documentation](https://gradio.app/docs/)
- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)
