from src.database import create_database, load_genes_from_csv
from src.database_queries import (
    get_all_genes,
    get_gene_by_symbol,
    count_genes,
)


def create_test_database(tmp_path):
    database_file = tmp_path / "test.db"

    connection = create_database(database_file)

    load_genes_from_csv(
        connection,
        "src/data/curated_genes.csv",
    )

    connection.close()

    return database_file


def test_count_genes(tmp_path):
    database_file = create_test_database(tmp_path)

    assert count_genes(database_file) == 5


def test_get_gene_by_symbol(tmp_path):
    database_file = create_test_database(tmp_path)

    result = get_gene_by_symbol(
        database_file,
        "thrA",
    )

    assert result[0] == "gene2"
    assert result[1] == "thrA"
    assert result[2] == "homoserine dehydrogenase"


def test_get_missing_gene(tmp_path):
    database_file = create_test_database(tmp_path)

    result = get_gene_by_symbol(
        database_file,
        "does_not_exist",
    )

    assert result is None


def test_get_all_genes(tmp_path):
    database_file = create_test_database(tmp_path)

    result = get_all_genes(database_file)

    assert len(result) == 5
    assert result[0][1] == "thrL"
