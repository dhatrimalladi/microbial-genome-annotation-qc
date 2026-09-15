from src.database import create_database, load_genes_from_csv
from src.database_queries import (
    get_all_genes,
    get_gene_by_symbol,
    count_genes,
    get_cds_for_gene,
)


def create_test_database(tmp_path):
    database_file = tmp_path / "test.db"

    connection = create_database(database_file)

    from src.annotation_database import (
        create_annotation_table,
        load_gff3_annotations,
    )

    create_annotation_table(connection)

    load_genes_from_csv(
        connection,
        "src/data/curated_genes.csv",
    )

    load_gff3_annotations(
        connection,
        "src/data/example_annotation.gff3",
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


def test_get_cds_for_gene(tmp_path):
    database_file = create_test_database(tmp_path)

    result = get_cds_for_gene(
        database_file,
        "thrL",
    )

    assert len(result) == 2
    assert result[0][0] == "cds1"
    assert result[0][1] == "contig_1"
    assert result[0][2] == 3
    assert result[0][3] == 15
    assert result[0][4] == "+"


def test_get_cds_for_gene_without_cds(tmp_path):
    database_file = create_test_database(tmp_path)

    result = get_cds_for_gene(
        database_file,
        "thrA",
    )

    assert result == []
