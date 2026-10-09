from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def get_gpt_response(prompt: str, max_tokens: int = 100) -> str:
    response = client.chat.completions.create(
        model="gpt-6-luna",
        messages=[
            {"role": "system", "content": "You are an NPC in a murder mystery game. Provide concise and relevant responses to help the player gather clues and solve the mystery."},
            {"role": "user", "content": prompt}
        ],
        # gpt-6-luna는 max_tokens 대신 max_completion_tokens만 지원
        # 4o-mini보다 답변이 길어 문장이 잘리지 않도록 여유를 두고, 길이는 verbosity로 조절
        max_completion_tokens=max_tokens * 3 + 300,
        reasoning_effort="none",
        verbosity="low",
        n=1,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
