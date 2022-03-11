from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from environs import Env


@dataclass
class TgBot:
    token: str
    fsm_type: str
    admins: list
    issue_chat: str


@dataclass
class RedisConfig:
    host: str
    port: int
    db: int
    password: str


@dataclass
class InfluxDBConfig:
    host: str
    port: int
    database: str 
    username: str
    password: str


@dataclass
class Database:
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
    locales_path: Path
    default_language: str
    use_default_language_on_missing: bool
    allow_missing_translation: bool
    allow_missing_placeholder: bool
    allow_missing_plural: bool


@dataclass
class Middlewares:
    i18n: I18nConfig

@dataclass
class Config:
    bot: TgBot
    redis: RedisConfig
    influxdb: InfluxDBConfig
    db: Database
    logging: Logging
    i18n: I18nConfig
    project_phase: str # 'dev' | 'prod'


env = Env()
env.read_env()
logs_path: Optional[Path] = Path.joinpath(Path(__file__).cwd(), f'logs_{env.str("BOT_USERNAME")}') if env.bool("SAVE_LOGS") else None

config: Config = Config(
    bot=TgBot(
        token=env.str("BOT_TOKEN"),
        fsm_type=env.str("FSM_MODE"),
        admins=env.list("BOT_ADMINS", subcast=int),
        issue_chat=env.str("ISSUE_CHAT")
    ),
    redis=RedisConfig(
        host=env.str("REDIS_HOST"),
        port=env.int("REDIS_PORT"),
        db=env.int("REDIS_DB_FSM"),
        password=env.str("REDIS_PASSWORD")
    ),
    influxdb=InfluxDBConfig(
        host=env.str('INFLUXDB_HOST'),
        port=env.int('INFLUXDB_PORT'),
        database=env.str("INFLUXDB_DATABASE"),
        username=env.str("INFLUXDB_USERNAME"),
        password=env.str("INFLUXDB_PASSWORD")
    ),
    db=Database(
        host=env.str("DB_HOST"),
        port=env.int("DB_PORT"),
        name=env.str("DB_NAME"),
        user=env.str("DB_USER"),
        password=env.str("DB_PASSWORD")
    ),
    logging=Logging(
        path=logs_path,
        level=env.str("LOG_LEVEL"),
        ignored=["aiogram.bot.api"]
    ),
    i18n=I18nConfig(
        locales_path=Path.joinpath(
            Path(__file__).parent.parent, 'locales'),
        default_language="ru",
        use_default_language_on_missing=True,
        allow_missing_translation=True,
        allow_missing_placeholder=True,
        allow_missing_plural=True
    ),
    project_phase=env.str("PROJECT_PHASE")
)
