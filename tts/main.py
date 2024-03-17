from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from tts import define_text_to_speech

app = FastAPI()


class Schema(BaseModel):
    content: str

@app.post("/")
async def read_root(schema: Schema):
    result = define_text_to_speech(schema.content)

    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9090, reload=False)