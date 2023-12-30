from task import errors
from task.options import RunModeEnum
from task.connectors.database import (
    DatabaseConnector,
    JsonFileDatabaseConnector,
    Sqlite3DatabaseConnector,
)


def db_connector_factory(run_mode: RunModeEnum) -> DatabaseConnector:
    try:
        available_db_connectors: dict[RunModeEnum, DatabaseConnector] = {
            RunModeEnum.PROD: Sqlite3DatabaseConnector,
            RunModeEnum.DEV: JsonFileDatabaseConnector,
        }

        return available_db_connectors[run_mode]()
    except KeyError:
        raise errors.UhnandledRunModeError
