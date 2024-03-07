from src.database.postgres.handler import PostgreSQLHandler as DatabaseHandler


async def get_database_dependency() -> DatabaseHandler:
    """
    Provides a database handler dependency for use in FastAPI routes or other dependency-injection contexts.

    Returns:
        DatabaseHandler: An instance of `DatabaseHandler` for interacting with the database.
    """
    return DatabaseHandler()
