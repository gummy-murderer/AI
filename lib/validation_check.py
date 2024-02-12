import json
import openai
from pathlib import Path
import os, dotenv

dotenv_file = dotenv.find_dotenv(str(Path("./").absolute().joinpath(".env")))
dotenv.load_dotenv()
MY_KEY = os.environ["MY_KEY"]


def response_format(answer):
    try:
        return json.loads(answer.replace('```', '').replace('json', ''))
    except:
        return None


def check_openai_api_key(input_api_key):
    MY_KEY = os.getenv("MY_KEY")

    if input_api_key == MY_KEY:
        api_key = os.getenv("OPENAI_API_KEY")
    else:
        api_key = input_api_key

    try:
        openai.OpenAI(api_key=api_key).models.list()
        return api_key
    except openai.AuthenticationError:
        return None
    except openai.APIConnectionError:
        return None