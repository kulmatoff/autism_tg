from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str

@dataclass
class OpenaiToken:
    token: str

@dataclass
class Config:
    tg_bot: TgBot,
    openai_token: OpenaiToken

def load_config():
    env = Env()
    env.read_env()
    return Config(
        tg_bot=TgBot(token=env.str("BOT_TOKEN")),
        openai_token=OpenaiToken(token=env.str("OPENAI_TOKEN"))
    )