from src.gff3_qc import (
    parse_gff3,
    validate_gff3,
    validate_sequence_ids,
)


def test_parse_gff3():
    result = parse_gff3("src/data/example_annotation.gff3")

    assert result["total_features"] == 4
    assert result["feature_types"]["gene"] == 2
    assert result["feature_types"]["CDS"] == 2


def test_validate_gff3():
    result = validate_gff3("src/data/example_annotation.gff3")

    assert result["is_valid"] is True
    assert result["errors"] == []


def test_validate_invalid_gff3():
    result = validate_gff3("src/data/invalid_annotation.gff3")

    assert result["is_valid"] is False
    assert len(result["errors"]) == 1
    assert "start coordinate is greater than end" in result["errors"][0]


def test_validate_duplicate_ids():
    result = validate_gff3("src/data/duplicate_ids.gff3")

    assert result["is_valid"] is False
    assert len(result["errors"]) == 1
    assert "duplicate feature ID 'gene_1'" in result["errors"][0]
def test_validate_missing_id():
    result = validate_gff3("src/data/missing_id.gff3")

    assert result["is_valid"] is False
    assert len(result["errors"]) == 1
    assert "missing feature ID" in result["errors"][0]
def test_validate_sequence_ids():
    result = validate_sequence_ids(
        "src/data/example_genome.fasta",
        "src/data/example_annotation.gff3",
    )

    assert result["is_valid"] is True
    assert result["errors"] == []


def test_validate_sequence_ids_missing_sequence():
    result = validate_sequence_ids(
        "src/data/example_genome.fasta",
        "src/data/missing_sequence.gff3",
    )

    assert result["is_valid"] is False
    assert "not found in FASTA" in result["errors"][0]
