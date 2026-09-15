import csv
import sqlite3


def create_database(database_file):
    """Create the SQLite database and genes table."""
    connection = sqlite3.connect(database_file)

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS genes (
            gene_id TEXT PRIMARY KEY,
            gene_symbol TEXT NOT NULL,
            product TEXT NOT NULL,
            feature_type TEXT NOT NULL,
            organism TEXT NOT NULL,
            evidence_source TEXT NOT NULL
        )
        """
    )

    connection.commit()

    return connection


def load_genes_from_csv(connection, csv_file):
    """Load curated gene records from a CSV file."""
    with open(csv_file, "r", newline="") as file:
        reader = csv.DictReader(file)

        records = list(reader)

    connection.executemany(
        """
        INSERT OR REPLACE INTO genes (
            gene_id,
            gene_symbol,
            product,
            feature_type,
            organism,
            evidence_source
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (
                record["gene_id"],
                record["gene_symbol"],
                record["product"],
                record["feature_type"],
                record["organism"],
                record["evidence_source"],
            )
            for record in records
        ],
    )

    connection.commit()

    return len(records)


def count_genes(connection):
    """Return the number of genes in the database."""
    cursor = connection.execute(
        "SELECT COUNT(*) FROM genes"
    )

    return cursor.fetchone()[0]


if __name__ == "__main__":
    database_file = "src/data/curated_genes.db"
    csv_file = "src/data/curated_genes.csv"

    connection = create_database(database_file)

    loaded = load_genes_from_csv(
        connection,
        csv_file,
    )

    total = count_genes(connection)

    print("Database created successfully")
    print(f"Records loaded: {loaded}")
    print(f"Records in database: {total}")

    connection.close()
