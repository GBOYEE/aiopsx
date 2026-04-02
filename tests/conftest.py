import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from aiopsx.state.models import Base, init_db
import tempfile
import os

@pytest.fixture(scope="session")
def temp_db_path():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield path
    try:
        os.unlink(path)
    except OSError:
        pass

@pytest.fixture(scope="function")
def db_session(temp_db_path):
    url = f"sqlite:///{temp_db_path}"
    Session = init_db(url)
    session = Session()
    yield session
    session.rollback()
    session.close()
    Base.metadata.drop_all(bind=session.bind)
    Base.metadata.create_all(bind=session.bind)
