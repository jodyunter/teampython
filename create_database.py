from teams.data.database import Database
from alembic.config import Config
from alembic import command

# running this file should create a database with the desired configuration up to the most recent revision

alembic_file = "alembic.ini"
alembic_section = "alembic_section"
conn_string = "db_string"
revision_name = "head"

configs = {
    "sqlite_local": {alembic_section: "sqlite_local", conn_string: "sqlite:///C:\\temp\\team_data.db"},
    "postres_local": {alembic_section: "postres_local",
                      conn_string: "postgresql://test_user:password@localhost/testdb"}

}

config_name = "sqlite_local"


Database.init_db(configs[config_name][conn_string])

alembic_cfg = Config(alembic_file, configs[config_name][alembic_section])
command.stamp(alembic_cfg, revision_name)
