from behave import fixture
from behave.runner import Context


@fixture
def setup_db(context: Context, *args, **kwargs):
    """
    Setup the database for tests.

    Steps:
        - Create all database tables.
        - Initialize and add to context the database session.
        - yield
        - Close all database sessions.
        - Drop all database tables.
    """
    from drivr.db.base import Entity
    from tests.integration.modules.db import (
        create_db_engine,
        create_db_session,
    )

    engine = create_db_engine(context.config.userdata.get("database_url"))
    session = create_db_session()
    try:
        Entity.metadata.create_all(engine)
        context.db = session
        yield
    finally:
        session.close_all()
        Entity.metadata.drop_all(engine)


@fixture
def setup_app(context: Context, *args, **kwargs):
    """
    Setup the application for tests.

    Steps:
        - Bootstrap the uvicorn server with the FastAPI app running.
        - Add the 'url_root' to context.
        - yield
        - Finish the server
    """
    import uvicorn

    from drivr import app

    from ..modules.server_app import Server

    app_port = context.config.userdata.get("app_port")
    app_host = context.config.userdata.get("app_host")

    config = uvicorn.Config(
        app,
        host=app_host,
        port=int(app_port),
        log_level=context.config.userdata.get("uvicorn_debug"),
        loop="asyncio",
    )
    context.url_root = f"http://{app_host}:{app_port}"

    server = Server(config=config)
    with server.run_in_thread():
        yield
