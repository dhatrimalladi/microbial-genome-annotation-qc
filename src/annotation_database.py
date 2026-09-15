import sqlite3


def create_annotation_table(connection):
    """Create the annotation features table."""
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS annotations (
            database_id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature_id TEXT NOT NULL,
            feature_type TEXT NOT NULL,
            sequence_id TEXT NOT NULL,
            start INTEGER NOT NULL,
            end INTEGER NOT NULL,
            strand TEXT,
            parent_id TEXT,
            gene_symbol TEXT
        )
        """
    )

    connection.commit()


def load_gff3_annotations(connection, gff3_file):
    """Load GFF3 annotation features into SQLite."""
    records = []

    with open(gff3_file, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split("\t")

            if len(parts) != 9:
                continue

            sequence_id = parts[0]
            feature_type = parts[2]
            start = int(parts[3])
            end = int(parts[4])
            strand = parts[6]
            attributes = parts[8]

            attribute_dict = {}

            for attribute in attributes.split(";"):
                if "=" in attribute:
                    key, value = attribute.split("=", 1)
                    attribute_dict[key] = value

            feature_id = attribute_dict.get("ID")

            if feature_id is None:
                continue

            parent_id = attribute_dict.get("Parent")
            gene_symbol = attribute_dict.get("gene")

            records.append(
                (
                    feature_id,
                    feature_type,
                    sequence_id,
                    start,
                    end,
                    strand,
                    parent_id,
                    gene_symbol,
                )
            )

    connection.executemany(
        """
        INSERT INTO annotations (
            feature_id,
            feature_type,
            sequence_id,
            start,
            end,
            strand,
            parent_id,
            gene_symbol
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        records,
    )

    connection.commit()

    return len(records)


if __name__ == "__main__":
    database_file = "src/data/curated_genes.db"
    gff3_file = "src/data/example_annotation.gff3"

    connection = sqlite3.connect(database_file)

    create_annotation_table(connection)

    loaded = load_gff3_annotations(
        connection,
        gff3_file,
    )

    print("Annotation table created successfully")
    print(f"Annotations loaded: {loaded}")

    connection.close()
