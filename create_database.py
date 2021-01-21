from app_config import db_connection_string
from teams.data.database import Database
from alembic.config import Config
from alembic import command

configs = {
    "sqlite_local": "sqlite:///C:\\temp\\team_data.db",
    "postres_local": "postgresql://test_user:password@localhost/testdb"
}

config = "sqlite_local"

Database.init_db(configs[config])

alembic_cfg = Config("alembic.ini", config)
command.stamp(alembic_cfg, "head")
