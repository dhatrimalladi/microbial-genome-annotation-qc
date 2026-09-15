from src.curation_qc import load_curated_genes, validate_curated_genes


def test_load_curated_genes():
    records = load_curated_genes(
        "src/data/curated_genes.csv"
    )

    assert len(records) == 5
    assert records[0]["gene_symbol"] == "thrL"


def test_validate_curated_genes():
    result = validate_curated_genes(
        "src/data/curated_genes.csv"
    )

    assert result["is_valid"] is True
    assert result["record_count"] == 5
    assert result["errors"] == []


def test_validate_invalid_curated_genes():
    result = validate_curated_genes(
        "src/data/invalid_curated_genes.csv"
    )

    assert result["is_valid"] is False
    assert result["record_count"] == 3
    assert len(result["errors"]) == 3

    assert "missing value in 'product'" in result["errors"][0]
    assert "duplicate gene ID 'gene2'" in result["errors"][1]
    assert "unexpected feature type 'unknown'" in result["errors"][2]
