from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database connection URI
DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql://username:password@localhost/dbname')

# OpenAI API Key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-openai-api-key')

# Other configuration settings can be added here as needed
