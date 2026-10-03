import asyncio
import asyncpg
import os

async def test_connection():
    # Get the DB URL from the same logic as the tests
    # Using a hardcoded one for a quick check, but we'll use the env/settings logic
    try:
        # Attempting with the known credentials from the error logs
        user = 'postgres'
        password = 'ilyasseraja'
        database = 'marrakech_drive_test'
        host = 'localhost'
        port = 5432

        print(f"Attempting to connect to {database} at {host}:{port}...")

        conn = await asyncpg.connect(
            user=user,
            password=password,
            database=database,
            host=host,
            port=port
        )
        print("Successfully connected!")

        # Try a simple query
        val = await conn.fetchval('SELECT 1')
        print(f"Query successful, result: {val}")

        await conn.close()
        print("Connection closed cleanly.")

    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
