from app_config import db_connection_string
from teams.data.database import Database
from alembic.config import Config
from alembic import command

#Database.init_db(db_connection_string)

alembic_cfg = Config("alembic.ini")
command.stamp(alembic_cfg, "head")
