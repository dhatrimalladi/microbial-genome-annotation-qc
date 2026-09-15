from src.annotation_database import create_annotation_table, load_gff3_annotations
from src.curation_report import build_gene_report
from src.database import create_database, load_genes_from_csv


REAL_GFF3 = (
    "real_data/ecoli_k12/ncbi_dataset/data/"
    "GCF_000005845.2/genomic.gff"
)


def build_test_database(database_file):
    connection = create_database(database_file)

    load_genes_from_csv(
        connection,
        "src/data/curated_genes.csv",
    )

    create_annotation_table(connection)

    load_gff3_annotations(
        connection,
        REAL_GFF3,
    )

    connection.close()


def test_build_gene_report(tmp_path):
    database_file = tmp_path / "test.db"

    build_test_database(database_file)

    report = build_gene_report(
        database_file,
        "thrA",
    )

    assert report["gene"] is not None
    assert report["gene"][1] == "thrA"
    assert len(report["annotations"]) > 0


def test_gene_report_contains_expected_ncbi_annotation(tmp_path):
    database_file = tmp_path / "test.db"

    build_test_database(database_file)

    report = build_gene_report(
        database_file,
        "thrA",
    )

    annotations = report["annotations"]

    assert any(
        annotation[3] == "CDS"
        and annotation[4] == "NC_000913.3"
        for annotation in annotations
    )


def test_gene_report_for_missing_gene(tmp_path):
    database_file = tmp_path / "test.db"

    connection = create_database(database_file)

    load_genes_from_csv(
        connection,
        "src/data/curated_genes.csv",
    )

    create_annotation_table(connection)

    connection.close()

    report = build_gene_report(
        database_file,
        "not_a_real_gene",
    )

    assert report["gene"] is None
    assert report["annotations"] == []
