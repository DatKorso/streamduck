import os
import duckdb
from dotenv import load_dotenv


def get_motherduck_connection(db: str | None = None) -> duckdb.DuckDBPyConnection:
    """Connect to MotherDuck using token from .env (MOTHERDUCK_TOKEN).

    If `db` is provided, connects to that database name (e.g., "mydb").
    Requires the `motherduck` extension and DuckDB >= 1.3.
    """
    # Load environment from .env so MOTHERDUCK_TOKEN is available
    load_dotenv()

    token = os.getenv("MOTHERDUCK_TOKEN")
    if not token:
        raise RuntimeError("MOTHERDUCK_TOKEN is not set. Add it to your .env.")

    # Prefer passing the token in the connection string to avoid env issues.
    try:
        conn_str = f"md:{db or ''}?motherduck_token={token}"
        return duckdb.connect(conn_str)
    except Exception as direct_err:
        # Fallback: install/load the extension explicitly and attach
        try:
            con = duckdb.connect()
            con.execute("INSTALL motherduck")
            con.execute("LOAD motherduck")
            # Set token via config to avoid leaking in logs
            con.execute("SET motherduck_token=?", [token])
            attach_target = f"md:{db or ''}"
            con.execute(f"ATTACH '{attach_target}' AS md")
            # Make the attached MotherDuck database the active one
            con.execute("USE md")
            return con
        except Exception as ext_err:
            # Surface both error paths to aid debugging
            raise RuntimeError(
                "Failed to connect to MotherDuck. "
                "Details: direct-connect error='{}'; extension/attach error='{}'".format(
                    str(direct_err), str(ext_err)
                )
            )


def main():
    # Example usage: try a simple query to validate the connection
    try:
        con = get_motherduck_connection()
        result = con.execute("select current_user();").fetchone()
        print("Connected to MotherDuck as:", result[0])
    except Exception as e:
        # Print a concise, actionable error
        print("MotherDuck connection failed:")
        print(" - Ensure your DuckDB version supports the motherduck extension")
        print(" - Verify the token in .env under MOTHERDUCK_TOKEN")
        print(" - If behind a proxy, allow extension downloads")
        raise


if __name__ == "__main__":
    main()
