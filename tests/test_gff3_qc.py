from src.gff3_qc import parse_gff3, validate_gff3


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
