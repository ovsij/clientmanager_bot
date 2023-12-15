from dataclasses import dataclass

from environs import Env


@dataclass
class Bot:
    token: str
    admin_ids: list
    bot_url: str
    app_url: str


@dataclass
class Postgres:
    user: str
    password: str
    host: str
    port: str
    database: str


@dataclass
class Config:
    bot: Bot
    postgres: Postgres


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        bot=Bot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            bot_url=env.str("BOT_URL"),
            app_url=env.str("APP_URL"),
        ),
        postgres=Postgres(
            user=env.str("DB_USER"),
            password=env.str("DB_PASSWORD"),
            host=env.str("DB_HOST"),
            port=env.str("DB_PORT"),
            database=env.str("DB_DATABASE"),
        ),
    )


config: Config = load_config(".env")
