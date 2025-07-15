import logging
from typing import Dict, Any, List, Set

import psycopg2
from psycopg2.extras import RealDictCursor

from server_mcp.config import settings
from server_mcp.schemas import TableDetailsParams

logger = logging.getLogger(__name__)

class PostgreSQLTool:
    """Tool for retrieving PostgreSQL database schema information."""

    def __init__(self) -> None:
        self._conn = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize PostgreSQL connection."""
        if self._initialized:
            logger.debug("Already initialized.")
            return
        self._conn = psycopg2.connect(settings.postgres_dsn)
        self._initialized = True
        logger.info("PostgreSQL connection established.")

    async def close(self) -> None:
        """Close PostgreSQL connection."""
        if self._conn:
            self._conn.close()
            logger.info("PostgreSQL connection closed.")

    def _get_primary_keys(self, table: str, cursor) -> Set[str]:
        cursor.execute(
            """
            SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
            WHERE tc.table_schema = 'public'
              AND tc.table_name = %s
              AND tc.constraint_type = 'PRIMARY KEY'
            """,
            (table, ),
        )
        return {row["column_name"] for row in cursor.fetchall()}

    def get_database_structure(self) -> Dict[str, Any]:
        """Return structure of the whole database."""
        if not self._initialized:
            raise RuntimeError("Tool not initialized")
        result: Dict[str, Any] = {"tables": {}, "relations": []}
        with self._conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
                """
            )
            tables = [row["table_name"] for row in cur.fetchall()]
            for table in tables:
                cur.execute(
                    """
                    SELECT column_name AS name,
                           data_type AS type,
                           is_nullable
                    FROM information_schema.columns
                    WHERE table_schema = 'public' AND table_name = %s
                    ORDER BY ordinal_position
                    """,
                    (table,),
                )
                columns = []
                pk_cols = self._get_primary_keys(table, cur)
                for row in cur.fetchall():
                    columns.append(
                        {
                            "name": row["name"],
                            "type": row["type"],
                            "nullable": row["is_nullable"],
                            "is_primary_key": row["name"] in pk_cols,
                        }
                    )
                result["tables"][table] = {"columns": columns}

            cur.execute(
                """
                SELECT tc.table_name AS from_table,
                       kcu.column_name AS from_column,
                       ccu.table_name AS to_table,
                       ccu.column_name AS to_column
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                  ON ccu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY'
                  AND tc.table_schema = 'public'
                """
            )
            for row in cur.fetchall():
                result["relations"].append(
                    {
                        "from_table": row["from_table"],
                        "from_column": row["from_column"],
                        "to_table": row["to_table"],
                        "to_column": row["to_column"],
                    }
                )
        return result

    def get_table_details(self, table: str) -> Dict[str, Any]:
        """Return detailed information about a table."""
        if not self._initialized:
            raise RuntimeError("Tool not initialized")
        with self._conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT column_name,
                       data_type,
                       is_nullable,
                       column_default,
                       character_maximum_length,
                       numeric_precision,
                       numeric_scale
                FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = %s
                ORDER BY ordinal_position
                """,
                (table,),
            )
            columns = [dict(row) for row in cur.fetchall()]
        return {"table": table, "columns": columns}

postgresql_tool = PostgreSQLTool()

async def postgres_get_structure() -> Dict[str, Any]:
    return postgresql_tool.get_database_structure()

async def postgres_get_table_details(params: TableDetailsParams) -> Dict[str, Any]:
    return postgresql_tool.get_table_details(params.table_name)
