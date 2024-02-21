from pydantic import BaseModel


class DiscordBot(BaseModel):
    BotToken: str
    ChanelID: int