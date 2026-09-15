import sqlite3


def get_all_genes(database_file):
    """Return all curated gene records."""
    connection = sqlite3.connect(database_file)

    cursor = connection.execute(
        """
        SELECT gene_id, gene_symbol, product,
               feature_type, organism, evidence_source
        FROM genes
        ORDER BY gene_id
        """
    )

    records = cursor.fetchall()

    connection.close()

    return records


def get_gene_by_symbol(database_file, gene_symbol):
    """Return a gene record matching the gene symbol."""
    connection = sqlite3.connect(database_file)

    cursor = connection.execute(
        """
        SELECT gene_id, gene_symbol, product,
               feature_type, organism, evidence_source
        FROM genes
        WHERE gene_symbol = ?
        """,
        (gene_symbol,),
    )

    record = cursor.fetchone()

    connection.close()

    return record


def count_genes(database_file):
    """Return the total number of genes in the database."""
    connection = sqlite3.connect(database_file)

    cursor = connection.execute(
        "SELECT COUNT(*) FROM genes"
    )

    count = cursor.fetchone()[0]

    connection.close()

    return count


def get_cds_for_gene(database_file, gene_symbol):
    """Return CDS features associated with a gene."""
    connection = sqlite3.connect(database_file)

    cursor = connection.execute(
        """
        SELECT
            cds.feature_id,
            cds.sequence_id,
            cds.start,
            cds.end,
            cds.strand
        FROM genes AS gene
        JOIN annotations AS cds
            ON cds.parent_id = gene.gene_id
        WHERE gene.gene_symbol = ?
          AND cds.feature_type = 'CDS'
        ORDER BY cds.start
        """,
        (gene_symbol,),
    )

    records = cursor.fetchall()

    connection.close()

    return records


if __name__ == "__main__":
    database_file = "src/data/curated_genes.db"

    print("Total genes:", count_genes(database_file))

    print("\nGene: thrA")
    print(get_gene_by_symbol(database_file, "thrA"))

    print("\nCDS features for thrL:")
    for cds in get_cds_for_gene(database_file, "thrL"):
        print(cds)

    print("\nAll genes:")
    for gene in get_all_genes(database_file):
        print(gene)
