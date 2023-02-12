from dataclasses import dataclass


@dataclass
class Config:
    tokenBot: str = "BOT_TOKEN"
    tokenOpenAi: str = "OPENAIAPIKEY"
    adminIds: int = 1
