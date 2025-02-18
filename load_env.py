from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Print environment variables
print("Environment variables from os.environ:")
print(f"OPENAI_API_KEY: {os.environ.get('OPENAI_API_KEY')}")
print(f"LANGSMITH_API_KEY: {os.environ.get('LANGSMITH_API_KEY')}")
print(f"Current working directory: {os.getcwd()}")
print(f"Env file exists: {os.path.exists('.env')}")

# Try to read the .env file directly
try:
    with open('.env', 'r') as f:
        print("\nContents of .env file:")
        print(f.read())
except Exception as e:
    print(f"Error reading .env file: {e}")
