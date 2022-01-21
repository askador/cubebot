from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from environs import Env


@dataclass
class TgBot:
    token: str
    fsm_type: str


@dataclass
class Redis:
    host: str
    port: int
    db: int
    password: str


@dataclass
class DB:
    host: str
    port: int
    name: str
    user: str
    password: str

@dataclass
class Logging:
    path: Optional[Path]
    level: str
    ignored: List[str]


@dataclass
class I18nConfig:
    default_language: str
    locales_path: Path
    allow_missing_translation: bool
    allow_missing_placeholder: bool
    allow_missing_plural: bool


@dataclass
class Middlewares:
    i18n: I18nConfig


@dataclass
class Config:
    bot: TgBot
    redis: Redis
    db: DB
    logging: Logging
    middlewares: Middlewares


def load_config() -> Config:
    env = Env()
    env.read_env()

    return Config(
        bot=TgBot(
            token=env.str("BOT_TOKEN"),
            fsm_type=env.str("FSM_MODE")
        ),
        redis=Redis(
            host=env.str("REDIS_HOST"),
            port=env.int("REDIS_PORT"),
            db=env.int("REDIS_DB_FSM"),
            password=env.str("REDIS_PASSWORD")
        ),
        db=DB(
            host=env.str("DB_HOST"),
            port=env.int("DB_PORT"),
            name=env.str("DB_NAME"),
            user=env.str("DB_USER"),
            password=env.str("DB_PASSWORD")
        ),
        logging=Logging(
            path=Path.joinpath(Path(__file__).cwd(), f'logs_{env.str("BOT_USERNAME")}'),
            level="INFO",
            ignored=["aiogram.bot.api"]
        ),
        middlewares=Middlewares(
            i18n=I18nConfig(
                locales_path=Path.joinpath(
                    Path(__file__).parent.parent, 'locales'),
                default_language="ru",
                allow_missing_translation=True,
                allow_missing_placeholder=True,
                allow_missing_plural=True
            )
        )
    )
