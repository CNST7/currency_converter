import pytest
from task.errors import UhnandledRunModeError
from task.options import RunModeEnum
from task.utils.db_connector import db_connector_factory
from task.connectors.database import (
    JsonFileDatabaseConnector,
    Sqlite3DatabaseConnector,
)


def test_db_connector_factory_returns_SQLITE3_connector_on_PROD_runmode():
    assert isinstance(db_connector_factory(RunModeEnum.PROD), Sqlite3DatabaseConnector)


def test_db_connector_factory_returns_JSON_connector_on_DEV_runmode():
    assert isinstance(db_connector_factory(RunModeEnum.DEV), JsonFileDatabaseConnector)


def test_db_connector_factory_raises_UhnandledRunModeError_on_unregistered_run_mode():
    with pytest.MonkeyPatch.context() as m:
        m.setattr(
            RunModeEnum,
            "UNREGISTERED_RUN_MODE",
            "UNREGISTERED_RUN_MODE",
            raising=False,
        )
        assert RunModeEnum.UNREGISTERED_RUN_MODE == "UNREGISTERED_RUN_MODE"
        with pytest.raises(UhnandledRunModeError):
            _ = db_connector_factory(RunModeEnum.UNREGISTERED_RUN_MODE)
