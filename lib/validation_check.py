import json
import openai
from pathlib import Path
import os, dotenv

# Load environment variables from .env file
env_path = Path('.') / '.env'
if env_path.exists():
    dotenv.load_dotenv(dotenv_path=env_path)

    MY_KEY = os.getenv("MY_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
else:
    MY_KEY = ""


def response_format(answer):
    """
    Formats a string response by removing specific characters and converting to JSON.
    
    Args:
        answer (str): The response string to format.
    
    Returns:
        dict or None: The formatted response as a JSON object, or None if conversion fails.
    """
    try:
        return json.loads(answer.replace('```', '').replace('json', ''))
    except:
        return None


def check_openai_api_key(input_api_key):
    """
    Validates an input API key against the stored API key or attempts to use it with OpenAI.
    
    Args:
        input_api_key (str): The API key to validate.
    
    Returns:
        str or None: The valid API key if the key is correct or None if validation fails.
    """
    if MY_KEY:
        if input_api_key == MY_KEY:
            api_key = OPENAI_API_KEY
        else:
            api_key = input_api_key

    try:
        # Attempt to use the API key to list OpenAI models as a validation step
        openai.OpenAI(api_key=api_key).models.list()
        return api_key  # Return the valid API key
    except openai.AuthenticationError:
        return None  # Authentication with OpenAI failed
    except openai.APIConnectionError:
        return None  # Connection to OpenAI API failed
    except UnicodeEncodeError:
        return None  # Issue with encoding the API key
