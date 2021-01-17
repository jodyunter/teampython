from alembic.config import Config
from alembic import command

from app_config import db_connection_string
from teams.data.database import Database

alembic_cfg = Config("alembic.ini")
command.upgrade(alembic_cfg, "head")

Database.init_db(db_connection_string)

with Database.get_engine().connect() as connection:
    alembic_cfg.attributes['connection'] = connection
    command.upgrade(alembic_cfg, "head")
